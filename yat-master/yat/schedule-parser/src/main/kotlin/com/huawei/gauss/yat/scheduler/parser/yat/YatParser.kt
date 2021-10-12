/* 
 * Copyright (c) 2021 Huawei Technologies Co.,Ltd.
 *
 * openGauss is licensed under Mulan PSL v2.
 * You can use this software according to the terms and conditions of the Mulan PSL v2.
 * You may obtain a copy of Mulan PSL v2 at:
 *
 *           http://license.coscl.org.cn/MulanPSL2
 *        
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
 * EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
 * MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
 * See the Mulan PSL v2 for more details.
 */

package com.huawei.gauss.yat.scheduler.parser.yat

import com.huawei.gauss.yat.common.PathSearcher
import com.huawei.gauss.yat.scheduler.parser.Parser
import com.huawei.gauss.yat.scheduler.parser.ScheduleSyntaxError
import com.huawei.gauss.yat.scheduler.parser.ScheduleTree
import com.huawei.gauss.yat.scheduler.parser.TestDaemon
import com.huawei.gauss.yat.scheduler.parser.TestGroup
import com.huawei.gauss.yat.scheduler.parser.TestInterval
import com.huawei.gauss.yat.scheduler.parser.TestRun
import com.huawei.gauss.yat.scheduler.parser.TestSuite
import java.io.FileReader
import java.io.Reader

class YatParser(stream: Reader, private val importPaths: Array<String>) : Parser {
    private val cacheImport = mutableSetOf<String>()

    private val blockParser = YatBlockParser(stream)

    override fun parse(): ScheduleTree {
        val allBlocks = mutableListOf<BlockNode>()
        allBlocks.addAll(blockParser.allBlocks())
        val firstBlock = allBlocks.first()
        if (firstBlock.name == "import") {
            allBlocks.addAll(doImport(firstBlock))
        }

        return if (allBlocks.isEmpty()) {
            ScheduleTree()
        } else {
            buildTestSchedule(allBlocks)
        }
    }

    private fun doImport(block: BlockNode): List<BlockNode> {
        val res = mutableListOf<BlockNode>()

        block.body.forEach {
            if (it.name == "import") {
                val path = it.parseOneElement().value
                if (path !in cacheImport) {
                    val realPath = PathSearcher(*importPaths).search(path)
                            ?: throw ScheduleSyntaxError("given schedule file $path not found in schedule search path")
                    val importBlocks = YatBlockParser(FileReader(realPath)).allBlocks()
                    val firstBlock = importBlocks.first()
                    if (firstBlock.name == "import") {
                        res.addAll(doImport(firstBlock))
                    }
                    res.addAll(importBlocks)
                }
            } else {
                throw ScheduleSyntaxError("not support import item named ${it.name}")
            }
        }

        return res
    }

    private fun buildGroup(suite: TestSuite, nodes: List<ElementNode>): TestGroup {
        val group = TestGroup(suite)
        nodes.forEach {
            group.addTestCase(it.value, it.properties)
        }

        return group
    }

    private fun buildTestSuite(block: BlockNode): TestSuite {
        val nameItem = block.parseOneElement("name")

        val suite = TestSuite(nameItem.value)
        block.body.forEach {
            when (it.name) {
                "group" -> suite.add(buildGroup(suite, it.values))
                "setup" -> suite.setup = buildGroup(suite, it.values)
                "cleanup" -> suite.cleanup = buildGroup(suite, it.values)
            }
        }

        return suite
    }

    private fun parseRunType(block: BlockNode): TestRun.TestType {
        val typeItem = block.tryParseOneElement("type")

        return if (typeItem == null) {
            TestRun.TestType.SUITE
        } else {
            when (val typeValue = typeItem.value) {
                "suite" -> TestRun.TestType.SUITE
                "random-concurrent" -> TestRun.TestType.RANDOM_CONCURRENT
                else -> throw ScheduleSyntaxError("found unknown value $typeValue for item type")
            }
        }
    }

    private fun parseRunLevel(block: BlockNode): TestRun.ParallelLevel {
        val levelItem = block.tryParseOneElement("level")

        return if (levelItem == null) {
            TestRun.ParallelLevel.GROUP
        } else {
            when (val level = levelItem.value) {
                "group" -> TestRun.ParallelLevel.GROUP
                "case" -> TestRun.ParallelLevel.CASE
                "statement" -> TestRun.ParallelLevel.STATEMENT
                else -> throw ScheduleSyntaxError("found unknown value $level for item level")
            }
        }
    }

    private fun parseRandomSleep(block: BlockNode): IntArray {
        val sleepItem = block.trySearchBody("random-sleep")

        return if (sleepItem == null) {
            IntArray(1) { 0 }
        } else {
            when {
                sleepItem.values.size == 1 -> IntArray(1) { sleepItem.values[0].value.toInt() }
                sleepItem.values.size == 2 -> IntArray(2) { idx -> sleepItem.values[idx].value.toInt() }
                else -> throw ScheduleSyntaxError("random-sleep item allow only 1 or 2 values")
            }
        }
    }

    private fun parseRunCount(block: BlockNode): Int {
        val countItem = block.tryParseOneElement("each-run-count")
        return countItem?.value?.toInt() ?: 0
    }

    private fun buildRun(
            block: BlockNode,
            suites: Map<String, BlockNode>,
            intervals: Map<String, BlockNode>,
            daemons: Map<String, BlockNode>): TestRun {

        val itemSuite = block.parseOneElement("suite")
        val suiteBlock = suites[itemSuite.value]
                ?: throw ScheduleSyntaxError("suite with value ${itemSuite.value} is not defined")

        val itemName = block.parseOneElement("name")
        val suite = buildTestSuite(suiteBlock)

        val testRun = TestRun(itemName.value, suite)
        testRun.type = parseRunType(block)
        testRun.level = parseRunLevel(block)
        testRun.randomSleep = parseRandomSleep(block)
        testRun.eachRunCount = parseRunCount(block)

        block.body.forEach { item ->
            when (item.name) {
                "macro" -> {
                    if (item.values.size == 2) {
                        testRun.macros[item.values[0].value] = item.values[1].value
                    } else {
                        throw ScheduleSyntaxError("bad macro define found in run with suite value ${itemSuite.value}")
                    }
                }
                "interval" -> {
                    item.values.forEach { interval ->
                        val intervalBlock = intervals[interval.value]
                        if (intervalBlock == null) {
                            throw ScheduleSyntaxError("can not found interval with value $interval when create run ${itemName.value}")
                        } else {
                            testRun.intervals.add(buildInterval(intervalBlock))
                        }
                    }
                }
                "daemon" -> {
                    item.values.forEach { daemon ->
                        val daemonBlock = daemons[daemon.value]
                        if (daemonBlock == null) {
                            throw ScheduleSyntaxError("can not found daemon with value $daemon when create run ${itemName.value}")
                        } else {
                            testRun.daemons.add(buildDaemon(daemonBlock))
                        }
                    }
                }
            }

        }
        return testRun
    }

    private fun buildInterval(block: BlockNode): TestInterval {
        val nameItem = block.parseOneElement("name")
        val intervalItem = block.tryParseOneElement("interval")
        val interval = intervalItem?.value?.toInt() ?: 0

        return TestInterval(nameItem.value, buildTestSuite(block), interval)
    }

    private fun buildDaemon(block: BlockNode): TestDaemon {
        val nameItem = block.parseOneElement("name")
        return TestDaemon(nameItem.value, buildTestSuite(block))
    }

    private fun allBlocks(blockName: String, blocks: List<BlockNode>): Map<String, BlockNode> {
        val searchBlocks = mutableMapOf<String, BlockNode>()

        blocks.forEach {
            if (it.name == blockName) {
                val nameItem = it.parseOneElement("name")

                if (nameItem.value in searchBlocks) {
                    throw ScheduleSyntaxError("duplicate suite/interval/daemon struct with value $nameItem found")
                } else {
                    searchBlocks[nameItem.value] = it
                }
            }
        }

        return searchBlocks
    }

    private fun buildTestSchedule(blocks: List<BlockNode>): ScheduleTree {
        val suites = allBlocks("suite", blocks)
        val intervals = allBlocks("interval", blocks)
        val daemons = allBlocks("daemon", blocks)

        val schedule = ScheduleTree()

        blocks.forEach {
            if (it.name == "run") {
                schedule.addRun(buildRun(it, suites, intervals, daemons))
            }
        }

        return schedule
    }
}

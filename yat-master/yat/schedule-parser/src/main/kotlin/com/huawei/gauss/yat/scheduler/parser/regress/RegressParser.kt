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

package com.huawei.gauss.yat.scheduler.parser.regress

import com.huawei.gauss.yat.common.ArrayCycleQueue
import com.huawei.gauss.yat.common.PathSearcher
import com.huawei.gauss.yat.scheduler.parser.Parser
import com.huawei.gauss.yat.scheduler.parser.ScheduleSyntaxError
import com.huawei.gauss.yat.scheduler.parser.ScheduleTree
import com.huawei.gauss.yat.scheduler.parser.TestRun
import com.huawei.gauss.yat.scheduler.parser.TestSuite
import java.io.Reader

class RegressParser(private val stream: Reader, private val importPaths: Array<String>) : Parser {
    private val lexer = RegressLex(stream.buffered())
    private var line = 1
    private var column = 1
    private val imported = mutableSetOf<String>()

    override fun parse(): ScheduleTree {
        val schedule = ScheduleTree()
        var build = false
        val groups = mutableListOf<EntryNode>()
        var setup: EntryNode? = null
        var cleanup: EntryNode? = null
        var run = ""
        val macros = mutableMapOf<String, String>()

        while (hasNext()) {
            val token = peekToken()

            if (token!!.isSplit()) {
                addTestRun(schedule, run, setup, cleanup, groups, macros)

                build = true
                groups.clear()
                macros.clear()
                setup = null
                cleanup = null
            } else {
                build = false

                val entry = parseEntry()
                when (val name = entry.name) {
                    "test", "group" -> groups.add(entry)
                    "name" -> run = parseNameEntry(entry)
                    "setup" -> setup = entry
                    "cleanup" -> cleanup = entry
                    "import" -> groups.addAll(doImport(entry))
                    "macro" -> {
                        val macro = parseMacro(entry)
                        macros[macro.first] = macro.second
                    }
                    else -> throw ScheduleSyntaxError("not support entry value $name found")
                }
            }
        }

        if (!build) {
            addTestRun(schedule, run, setup, cleanup, groups, macros)
        }

        return schedule
    }

    private fun addTestRun(schedule: ScheduleTree, name: String, setup: EntryNode?, cleanup: EntryNode?, groups: List<EntryNode>, macros: Map<String, String>) {
        val testRunt = TestRun(name, buildTestSuite(name, setup, cleanup, groups))
        testRunt.macros.putAll(macros)
        schedule.addRun(testRunt)
    }

    private fun buildTestSuite(name: String, setup: EntryNode?, cleanup: EntryNode?, groups: List<EntryNode>): TestSuite {
        val testSuite = TestSuite(name)
        if (setup != null) {
            testSuite.setup = setup.toTestGroup(testSuite)
        }
        if (cleanup != null) {
            testSuite.cleanup = cleanup.toTestGroup(testSuite)
        }

        testSuite.addAll(groups.map { it.toTestGroup(testSuite) })

        return testSuite
    }

    private fun doImport(entry: EntryNode): List<EntryNode> {
        if (entry.values.size != 1) {
            throw ScheduleSyntaxError("value entry require only one value, but given ${entry.values.size}")
        }

        val value = entry.values[0]
        if (value.attrs.isNotEmpty()) {
            throw ScheduleSyntaxError("import entry value must not have attributes")
        }

        val searcher = PathSearcher(*importPaths)
        val path = searcher.search(value.value)
                ?: throw ScheduleSyntaxError("can not found import schedule file ${value.value} in schedule search path")

        if (path.absolutePath in imported) {
            throw ScheduleSyntaxError("duplicate import found: import: ${path.absolutePath}")
        } else {
            imported.add(path.absolutePath)
        }
        val parser = RegressParser(path.reader().buffered(), importPaths)

        val res = mutableListOf<EntryNode>()

        while (parser.hasNext()) {
            val token = parser.peekToken()
            if (token!!.isWord() && (token.value == "group" || token.value == "test")) {
                res.add(parser.parseEntry())
            } else if (token.isWord() && token.value == "import") {
                res.addAll(doImport(parser.parseEntry()))
            } else {
                throw ScheduleSyntaxError("sub-schedule only allow test/group entries")
            }
        }

        return res
    }

    private fun parseMacro(entry: EntryNode): Pair<String, String> {
        if (entry.values.size != 2) {
            throw ScheduleSyntaxError("macro entry require only tow value, but given ${entry.values.size}")
        }

        entry.values.forEach {
            if (it.attrs.isNotEmpty()) {
                throw ScheduleSyntaxError("macro entry value must not have attributes")
            }
        }

        val key = entry.values[0].value
        val value = entry.values[1].value

        return Pair(key, value)
    }

    private fun parseNameEntry(entry: EntryNode): String {
        if (entry.values.size != 1) {
            throw ScheduleSyntaxError("value entry require only one value, but given ${entry.values.size}")
        }
        val value = entry.values[0]
        if (value.attrs.isNotEmpty()) {
            throw ScheduleSyntaxError("value entry value must not have attributes")
        }

        return value.value
    }

    private fun parseEntry(): EntryNode {
        val name = expectWord().value
        expectSymbols(Token.COLON)
        return EntryNode(name, parseEntryValues())
    }

    private fun parseEntryValues(): List<EntryValue> {
        val entryValues = mutableListOf<EntryValue>()

        var entryValue = parseEntryValue()
        while (entryValue != null) {
            entryValues.add(entryValue)
            entryValue = parseEntryValue()
        }

        if (entryValues.isEmpty()) {
            throw ScheduleSyntaxError("parse entry, entry need at lest one entry value", line, column)
        }

        return entryValues
    }

    private fun parseEntryValue(): EntryValue? {
        if (!hasNext()) {
            return null
        }

        val token = peekToken()
        when {
            token!!.isSplit() -> {
                return null
            }
            token.isSymbol() -> throw ScheduleSyntaxError("parse entry, expect WORLD, found ${token.value}", line, column)
            token.isWord() -> {
                val value = token.value
                val mark = peekToken(1)
                if (mark == null) {
                    nextToken()
                    return EntryValue(value)
                }

                return if (mark.isSymbol()) {
                    when (mark.value) {
                        Token.L_BRACKET -> {
                            nextToken()
                            EntryValue(value, parseAttrs())
                        }
                        Token.COLON -> {
                            null
                        }
                        else -> throw ScheduleSyntaxError("parse entry, expect (, found ${token.value}", line, column)
                    }
                } else {
                    nextToken()
                    EntryValue(value)
                }
            }
            else -> throw ScheduleSyntaxError("parse entry value, expect WORLD or SPLIT, found ${token.value}", line, column)
        }
    }

    private fun parseAttrs(): Map<String, String> {
        expectSymbols(Token.L_BRACKET)
        var pair = parseAttr()
        val attrs = mutableMapOf<String, String>()

        while (pair != null) {
            attrs[pair.first] = pair.second
            pair = parseAttr()
        }

        return attrs
    }

    private fun parseAttr(): Pair<String, String>? {
        if (!hasNext()) {
            throw ScheduleSyntaxError("parse attribute value, expect WORLD or ), found EOF", line, column)
        }
        val token = nextToken()
        return if (token.isSymbol() && token.value == Token.R_BRACKET) {
            null
        } else if (token.isWord()) {
            val key = token.value
            expectSymbols(Token.COLON, Token.EQUAL)
            val value = expectWord().value
            Pair(key, value)
        } else {
            throw ScheduleSyntaxError("parse attribute, expect WORLD or ), found ${token.value}", line, column)
        }
    }

    private fun expectWord(): Token {
        if (!hasNext()) {
            throw ScheduleSyntaxError("parse entry, expect WORLD, fount EOF", line, column)
        }

        val token = nextToken()
        if (token.isWord()) {
            return token
        } else {
            throw ScheduleSyntaxError("parse entry, expect WORLD, found ${token.value}", line, column)
        }
    }

    private fun expectSymbols(vararg symbol: String) {
        if (!hasNext()) {
            throw ScheduleSyntaxError("parse entry, expect $symbol, fount EOF", line, column)
        }

        val token = nextToken()
        if (token.isSymbol()) {
            if (token.value !in symbol) {
                throw ScheduleSyntaxError("parse entry, found unexpect ${token.value}", line, column)
            }
        } else {
            throw ScheduleSyntaxError("parse entry, found unexpect ${token.value}", line, column)
        }
    }

    private fun expectToken(): Token {
        if (!hasNext()) {
            throw ScheduleSyntaxError("parse entry, expect WORLD, fount EOF", line, column)
        }

        return nextToken()
    }

    private fun nextToken(): Token {
        val token = if (tokenQueue.isEmpty) {
            lexer.nextToken()
        } else {
            tokenQueue.poll()
        }

        line = token!!.position.line
        column = token.position.column
        return token
    }

    private fun hasNext(): Boolean {
        return if (tokenQueue.isEmpty) {
            lexer.hasNext()
        } else {
            true
        }
    }

    private val tokenQueue = ArrayCycleQueue<Token>(2)

    private fun peekToken(index: Int = 0): Token? {
        val size = tokenQueue.size()
        if (size <= index) {
            val count = index - size + 1
            (0 until count).forEach { _ ->
                if (lexer.hasNext()) {
                    tokenQueue.add(lexer.nextToken())
                } else {
                    return null
                }
            }
        }
        return tokenQueue.peek(index)!!
    }
}
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

package com.huawei.gauss.yat

import com.huawei.gauss.yat.common.FileLocker
import com.huawei.gauss.yat.common.YatRuntimeError
import com.huawei.gauss.yat.report.CombineSummaryReport
import com.huawei.gauss.yat.report.DebugSummaryReport
import com.huawei.gauss.yat.report.JsonSummaryReport
import com.huawei.gauss.yat.report.LogSummaryReport
import com.huawei.gauss.yat.report.SummaryReport
import com.huawei.gauss.yat.report.PrinterSummaryReport
import com.huawei.gauss.yat.scheduler.Scheduler
import com.huawei.gauss.yat.scheduler.parser.Parser
import com.huawei.gauss.yat.scheduler.parser.ScheduleSyntaxError
import com.huawei.gauss.yat.scheduler.parser.ScheduleTree
import com.huawei.gauss.yat.setting.KEY_TEST_DIR
import com.huawei.gauss.yat.setting.SettingParseError
import com.huawei.gauss.yat.setting.YAT_HOME_ENV
import com.huawei.gauss.yat.setting.YatContext
import org.slf4j.LoggerFactory
import java.io.File
import java.io.PrintStream


class YatApplication {
    private val context = YatContext()

    private fun initLog() {
        System.setProperty(KEY_TEST_DIR, context.suite.vSuite.workDir.absolutePath)
    }

    private fun getReportStream(): PrintStream {
        return PrintStream(context.suite.vSuite.output.yatTextLog.outputStream())
    }

    private fun getReport(withConsole: Boolean = true): SummaryReport {
        val reports = mutableListOf<SummaryReport>()
        val suiteName = context.suite.name

        reports.add(PrinterSummaryReport(
                suiteName,
                getReportStream(),
                context.reporter.width,
                context.reporter.filling))

        if (withConsole) {
            reports.add(PrinterSummaryReport(
                    suiteName,
                    System.out,
                    context.reporter.width,
                    context.reporter.filling,
                    context.reporter.color,
                    context.reporter.bare))
        } else {
            reports.add(DebugSummaryReport(
                    context.suite.vSuite.testCaseDir,
                    context.suite.vSuite.expectDir,
                    context.suite.vSuite.output.resultDir,
                    context.case.outSuffix))
        }
        reports.add(JsonSummaryReport(suiteName, context.suite.vSuite.output.yatJsonLog))
        reports.add(LogSummaryReport(suiteName, context.suite.vSuite.output.yatRedoLog))
        return CombineSummaryReport(reports)
    }

    fun run(args: Array<String>) {
        try {
            val home = System.getenv(YAT_HOME_ENV) ?: throw YatRuntimeError("YAT_HOME env not found")
            context.load(home, args)
            // log initialize then the logger can be use
            initLog()
            context.dump()
        } catch (e: Exception) {
            when (e) {
                is YatRuntimeError, is SettingParseError -> {
                    println(e.message)
                    return
                }
                else -> throw e
            }
        }

        val logger = LoggerFactory.getLogger(YatApplication::class.java)

        logger.info("=========================== New Test Started ================================")

        FileLocker(context.suite.vSuite.output.lockFile).use { locker ->
            try {
                if (locker.lock()) {
                    runSuite()
                } else {
                    throw YatRuntimeError("Another yat is running on this suite maybe, stop now")
                }
            } catch (e: Exception) {
                when (e) {
                    is YatRuntimeError, is IllegalArgumentException, is ScheduleSyntaxError -> {
                        println("error: ${e.message}")
                        logger.error("exception found: ", e)
                    }
                    else -> throw e
                }
            }
        }
    }

    private fun runSuite() {
        val withConsole: Boolean
        val scheduleTree = if (context.action == "debug") {
            withConsole = false
            Parser.create(context.cases).parse()
        } else {
            val importPaths = arrayOf(".", context.suite.vSuite.scheduleDir.absolutePath)
            withConsole = true
            if (context.schedule.isEmpty()) {
                throw YatRuntimeError("can not found the default schedule file, please using -s/--schedule to specific the schedule file")
            }
            Parser.create(File(context.schedule), importPaths).parse()
        }

        CaseMetaMaker(context).makeCaseMeta(scheduleTree)

        when (context.action) {
            "info" -> printSuiteInfo(scheduleTree)
            "run", "debug" -> Scheduler(scheduleTree, context).schedule(getReport(withConsole))
            else -> throw YatRuntimeError("unknown action command found")
        }
    }

    private fun printSuiteInfo(scheduleTree: ScheduleTree) {
        val info = scheduleTree.info()

        println("Test Suite Name: ${context.suite.name}")
        println("Sub-Suite Count: ${info.subSuiteCount}")
        println("Test Case Count: ${info.caseCount}")
    }
}
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

package com.huawei.gauss.yat.report

import java.io.File
import java.io.IOException
import java.nio.file.Files
import java.nio.file.Paths
import java.time.Duration
import java.time.LocalDateTime

class DebugSummaryReport(private val testCasePath: File, private val expectPath: File, private val resultPath: File, private val outSuffix: String) : SummaryReport {

    inner class DebugGroupReport : GroupReport {
        override fun addTest(name: String, result: GroupReport.Result, start: LocalDateTime, time: Duration, meta: Map<String, String>) {
            when (result) {
                GroupReport.Result.FAILED -> {
                }
                GroupReport.Result.OK, GroupReport.Result.IGNORE, GroupReport.Result.NO_DIFF_OK, GroupReport.Result.NO_DIFF_FAILED, GroupReport.Result.NO_VALID -> {
                }
                else -> {
                }
            }
            println("[ Execute Test Case: $name ]")
            println("[ Test Case Output ]")
            val resPath = Paths.get(resultPath.absolutePath, name)
            try {
                if (resPath.toFile().exists()) {
                    for (line in Files.readAllLines(resPath)) {
                        println(line)
                    }
                } else {
                    println("*** output is empty ***")
                }
            } catch (e: IOException) {
                println("Error: $e")
            }
        }

        override fun finish() {}
    }

    inner class DebugSuiteReport : SuiteReport {
        override fun newGroupReport(): GroupReport {
            return DebugGroupReport()
        }

        override fun newSetupGroup(): GroupReport {
            return EmptyGroupReport()
        }

        override fun newCleanupGroup(): GroupReport {
            return EmptyGroupReport()
        }

        override fun finish() {}
    }

    override fun start() {}
    override fun newSuiteReport(name: String): SuiteReport {
        return DebugSuiteReport()
    }

    override fun newDaemonReport(name: String): SuiteReport {
        return EmptySuiteReport()
    }

    override fun newIntervalReport(name: String): SuiteReport {
        return EmptySuiteReport()
    }

    override fun finish() {}

}
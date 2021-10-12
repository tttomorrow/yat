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

import com.huawei.gauss.yat.common.Benchmark
import com.huawei.gauss.yat.common.ColorText
import com.huawei.gauss.yat.common.FixedWidthText
import java.io.PrintStream
import java.time.Duration
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.concurrent.atomic.AtomicInteger

class PrinterSummaryReport(
        private val name: String,
        private val printer: PrintStream,
        private val width: Int,
        private val filling: Char,
        private val color: Boolean = false,
        private val bare: Boolean = false) : SummaryReport {

    companion object {
        private val dataFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
        private fun printFlush(printer: PrintStream, text: String) {
            printer.println(text)
            printer.flush()
        }
    }

    private val bench = Benchmark()
    private val stat = Statistics()

    private inner class TextGroupReport(
            private val suiteName: String,
            private val subSuiteName: String,
            private val mark: Char) : GroupReport {

        override fun addTest(name: String, result: GroupReport.Result, start: LocalDateTime, time: Duration, meta: Map<String, String>) {
            stat.incAll()

            var validStatus = 'v'
            val res = when (result) {
                GroupReport.Result.FAILED -> "er"
                GroupReport.Result.OK -> {
                    stat.incSuccess()
                    "ok"
                }
                GroupReport.Result.IGNORE -> {
                    stat.incSuccess()
                    validStatus = 'i'
                    "ig"
                }
                GroupReport.Result.NO_DIFF_OK -> {
                    stat.incSuccess()
                    validStatus = 'd'
                    "ok"
                }
                GroupReport.Result.NO_DIFF_FAILED -> {
                    validStatus = 'd'
                    "er"
                }
                GroupReport.Result.NO_VALID -> {
                    stat.incSuccess()
                    validStatus = 'n'
                    "ok"
                }
                GroupReport.Result.TIMEOUT -> {
                    validStatus = 't'
                    "to"
                }
            }

            val timeString: String = when {
                time.seconds < 60 -> String.format("%06.3f s", time.toMillis() / 1000.0)
                time.toMinutes() < 60 -> String.format("%06.3f m", time.seconds / 60.0)
                time.toHours() < 24 -> String.format("%06.3f h", time.seconds / 3600.0)
                else -> String.format("%06.3f d", time.toMinutes() / 1440.0)
            }

            val realRes: String
            val testName: String
            val metaText: String
            val realWidth: Int

            if (color) {
                val temp = when (res) {
                    "ok" -> ColorText.green(res, true)
                    "er" -> ColorText.red(res, true)
                    "ig" -> ColorText.yellow(res, true)
                    else -> res
                }
                realRes = " : $temp"

                metaText = "[${ColorText.cyan(mark.toString(), true)}]" +
                        " [${ColorText.green(start.format(dataFormatter), true)}]" +
                        " [${ColorText.yellow(timeString, false)}]" +
                        " [${ColorText.red(validStatus.toString(), true)}] "
                realWidth = width + 11 * 5 + 9

                val noColorName = if (bare) {
                    if (subSuiteName.isEmpty()) {
                        "$suiteName:$name"
                    } else {
                        "$suiteName:$subSuiteName:$name"
                    }
                } else {
                    name
                }
                val leftWidth = realWidth - metaText.length - realRes.length - 11

                testName = if (noColorName.length > leftWidth) {
                    ColorText.purple(FixedWidthText(leftWidth).right(noColorName).build(), true)
                } else {
                    ColorText.purple("$noColorName ", true)
                }
            } else {
                realRes = " : $res"

                metaText = "[$mark] [${start.format(dataFormatter)}] [$timeString] [$validStatus] "
                realWidth = width

                val tempName = if (bare) {
                    if (subSuiteName.isEmpty()) {
                        "$suiteName:$name"
                    } else {
                        "$suiteName:$subSuiteName:$name"
                    }
                } else {
                    name
                }

                val leftWidth = realWidth - metaText.length - realRes.length
                testName = if (tempName.length > leftWidth) {
                    FixedWidthText(leftWidth).right(tempName).build()
                } else {
                    "$tempName "
                }
            }

            val text = FixedWidthText(realWidth, filling)
                    .left(metaText)
                    .left(testName, metaText.length, realWidth - realRes.length - 1)
                    .right(realRes)
                    .build()

            printFlush(printer, text)
        }

        override fun finish() {
            // do nothing
        }
    }

    private inner class TextSuiteReport(private val suiteName: String, private val name: String) : SuiteReport {

        private var index = AtomicInteger(0)

        override fun newGroupReport(): GroupReport {
            val mark = if (index.getAndIncrement() % 2 == 0) {
                '+'
            } else {
                '-'
            }
            return TextGroupReport(suiteName, name, mark)
        }

        override fun newSetupGroup(): GroupReport {
            return TextGroupReport(suiteName, name, '*')
        }

        override fun newCleanupGroup(): GroupReport {
            return TextGroupReport(suiteName, name, '=')
        }

        override fun finish() {
            // do nothing
        }
    }

    private inner class DaemonGroupReport : GroupReport {

        override fun addTest(name: String, result: GroupReport.Result, start: LocalDateTime, time: Duration, meta: Map<String, String>) {

        }

        override fun finish() {

        }
    }

    private inner class DaemonSuiteReport(private val name: String) : SuiteReport {

        override fun newGroupReport(): GroupReport {
            return DaemonGroupReport()
        }

        override fun newSetupGroup(): GroupReport {
            return DaemonGroupReport()
        }

        override fun newCleanupGroup(): GroupReport {
            return DaemonGroupReport()
        }

        override fun finish() {
            // do nothing
        }
    }

    private inner class IntervalGroupReport : GroupReport {

        override fun addTest(name: String, result: GroupReport.Result, start: LocalDateTime, time: Duration, meta: Map<String, String>) {

        }

        override fun finish() {

        }
    }

    private inner class IntervalSuiteReport(private val name: String) : SuiteReport {

        override fun newGroupReport(): GroupReport {
            return IntervalGroupReport()
        }

        override fun newSetupGroup(): GroupReport {
            return IntervalGroupReport()
        }

        override fun newCleanupGroup(): GroupReport {
            return IntervalGroupReport()
        }

        override fun finish() {
            // do nothing
        }
    }

    override fun newSuiteReport(name: String): SuiteReport {
        if (name.isNotEmpty()) {
            if (!bare) {
                printFlush(printer, FixedWidthText(width, ' ').center(" Suite: $name ").build())
            }
        }
        return TextSuiteReport(this.name, name)
    }

    override fun newDaemonReport(name: String): SuiteReport {
        return DaemonSuiteReport(name)
    }

    override fun newIntervalReport(name: String): SuiteReport {
        return IntervalSuiteReport(name)
    }

    override fun finish() {
        if (bare) {
            return
        }

        val success = stat.successCount()
        val all = stat.allCount()
        val time = bench.finish()
        val now = LocalDateTime.now().format(dataFormatter)
        val text = FixedWidthText(width, '#').center(" Testing Result $success/$all Using Time $time At $now ").build()
        val realText = if (color) {
            ColorText.green(text, false)
        } else {
            text
        }

        printFlush(printer, realText)
    }

    override fun start() {
        if (bare) {
            return
        }

        val now = LocalDateTime.now().format(dataFormatter)
        val headText = FixedWidthText(width, '#').center(" $now ").build()
        val realHeadText = if (color) {
            ColorText.green(headText, false)
        } else {
            headText
        }

        printFlush(printer, realHeadText)
        val text = FixedWidthText(width, ' ').center("Test Suite: $name").build()
        printFlush(printer, text)
    }

    fun getStatistics(): Statistics {
        return stat
    }
}
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
import java.io.File
import java.time.Duration
import java.time.LocalDateTime
import java.util.concurrent.atomic.AtomicInteger

/**
 * Thread safe run test report with redo-log
 */
class LogSummaryReport(private val suite: String, private val log: File) : SummaryReport {
    private val redo = RedoLog(log)

    internal class LogGroupReport(private val suite: String, private val group: Int, private val redo: RedoLog) : GroupReport {
        private val bench = Benchmark()

        override fun addTest(name: String, result: GroupReport.Result, start: LocalDateTime, time: Duration, meta: Map<String, String>) {
            val ok = when (result) {
                GroupReport.Result.FAILED -> RedoLog.Result.FAILED
                GroupReport.Result.IGNORE -> RedoLog.Result.IGNORE
                GroupReport.Result.NO_DIFF_FAILED -> RedoLog.Result.NO_DIFF_FAILED
                GroupReport.Result.NO_DIFF_OK -> RedoLog.Result.NO_DIFF_OK
                GroupReport.Result.OK -> RedoLog.Result.SUCCESS
                GroupReport.Result.NO_VALID -> RedoLog.Result.NO_VALID
                GroupReport.Result.TIMEOUT -> RedoLog.Result.TIMEOUT
            }
            redo.addRecord(RedoLog.CaseRecord(suite, group, name, time, start, ok))
        }

        override fun finish() {
            redo.addRecord(RedoLog.GroupRecord(suite, group, bench.finish(), bench.begin))
        }
    }

    internal class LogSuiteReport(private val suite: String, private val type: String, private val redo: RedoLog) : SuiteReport {
        private val group = AtomicInteger(0)
        private val bench = Benchmark()

        override fun newGroupReport(): GroupReport {
            return LogGroupReport(suite, group.getAndIncrement(), redo)
        }

        override fun newSetupGroup(): GroupReport {
            return LogGroupReport(suite, group.getAndIncrement(), redo)
        }

        override fun newCleanupGroup(): GroupReport {
            return LogGroupReport(suite, group.getAndIncrement(), redo)
        }

        override fun finish() {
            when (type) {
                "suite" -> redo.addRecord(RedoLog.SuiteRecord(suite, bench.finish(), bench.begin))
                "daemon" -> redo.addRecord(RedoLog.DaemonSuiteRecord(suite, bench.finish(), bench.begin))
                else -> throw RuntimeException("found unknown type $type")
            }
        }
    }

    internal class LogIntervalGroupReport(private val counter: AtomicInteger) : GroupReport {
        override fun addTest(name: String, result: GroupReport.Result, start: LocalDateTime, time: Duration, meta: Map<String, String>) {
            counter.incrementAndGet()
        }

        override fun finish() {
        }
    }

    internal class LogIntervalSuiteReport(private val suite: String, private val redo: RedoLog) : SuiteReport {
        private val bench = Benchmark()
        private val counter = AtomicInteger(0)

        override fun newGroupReport(): GroupReport {
            return LogIntervalGroupReport(counter)
        }

        override fun newSetupGroup(): GroupReport {
            return LogIntervalGroupReport(counter)
        }

        override fun newCleanupGroup(): GroupReport {
            return LogIntervalGroupReport(counter)
        }

        override fun finish() {
            redo.addRecord(RedoLog.IntervalSuiteRecord(suite, bench.finish(), bench.begin, counter.get()))
        }
    }

    private val bench = Benchmark()

    override fun newSuiteReport(name: String): SuiteReport {
        return LogSuiteReport(name, "suite", redo)
    }

    override fun newDaemonReport(name: String): SuiteReport {
        return LogSuiteReport(name, "daemon", redo)
    }

    override fun newIntervalReport(name: String): SuiteReport {
        return LogIntervalSuiteReport(name, redo)
    }

    override fun start() {

    }

    override fun finish() {
        redo.addRecord(RedoLog.ScheduleRecord(suite, bench.finish(), bench.begin))
    }
}
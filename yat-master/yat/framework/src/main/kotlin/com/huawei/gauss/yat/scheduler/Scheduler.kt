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
 
package com.huawei.gauss.yat.scheduler

import com.huawei.gauss.yat.checker.Checker
import com.huawei.gauss.yat.checker.SchedulerChecker
import com.huawei.gauss.yat.common.WorkPool
import com.huawei.gauss.yat.common.YatRuntimeError
import com.huawei.gauss.yat.executor.*
import com.huawei.gauss.yat.report.GroupReport
import com.huawei.gauss.yat.report.SuiteReport
import com.huawei.gauss.yat.report.SummaryReport
import com.huawei.gauss.yat.scheduler.parser.*
import com.huawei.gauss.yat.setting.CONST_RUN_SUITE
import com.huawei.gauss.yat.setting.YatContext
import org.slf4j.LoggerFactory
import java.util.concurrent.Future
import java.util.concurrent.Semaphore
import java.util.concurrent.TimeUnit
import java.util.concurrent.TimeoutException

class Scheduler(private var schedule: ScheduleTree, private val context: YatContext) {
    private val panic: Boolean = context.panic
    private val caseNamePattern = context.checking.limit.caseNamePattern
    private val caseMaxCount = context.checking.limit.caseMaxCount
    private val caseMaxDepth = context.checking.limit.caseMaxDepth
    private val caseMaxSize = context.checking.limit.caseMaxSize

    private fun getExecutor(case: TestCase): Executor {
        return when (val mode = context.scheduleMode) {
            "single" -> SingleExecutor(case, context, context.target.target)
            "compare" -> CompareExecutor(case, context, context.target.left, context.target.right)
            "regress" -> RegressionExecutor(case, context, context.target.target)
            "diff" -> DiffExecutor(case, context)
            else -> {
                logger.error("unknown run mode found: $mode")
                throw YatRuntimeError("unknown run mode found: $mode")
            }
        }
    }

    fun schedule(report: SummaryReport) {
        if (schedule.runList.isEmpty()) {
            println("No runs defined found, do nothing and exit.")
            return
        }

        val checker = SchedulerChecker.Builder(schedule)
            .casePattern(caseNamePattern)
            .maxCaseCount(caseMaxCount)
            .maxCaseSize(caseMaxSize)
            .maxCaseDepth(caseMaxDepth)
            .build()

        Checker.assert(checker.check())

        report.start()
        schedule.runList.forEach {
            it.macros.forEach { (k, v) ->
                context.macro.set(k, v)
            }
            context.macro.set(CONST_RUN_SUITE, it.name)

            when (it.type) {
                TestRun.TestType.SUITE -> runSchedule(it, report)
                TestRun.TestType.RANDOM_CONCURRENT -> randomConcurrentSchedule(it, report)
            }

        }
        report.finish()
    }

    private fun randomConcurrentSchedule(@Suppress("UNUSED_PARAMETER") testRun: TestRun, @Suppress("UNUSED_PARAMETER") report: SummaryReport) {

    }

    private fun daemonSchedule(daemon: TestDaemon, report: SuiteReport): Future<*> {
        return WorkPool.pool.submit {
            suiteSchedule(daemon.suite, report)
        }
    }

    private fun intervalSchedule(interval: TestInterval, report: SuiteReport): Future<*> {
        return WorkPool.pool.submit {
            while (true) {
                Thread.sleep(interval.interval.toLong())
                suiteSchedule(interval.suite, report)
            }
        }
    }

    private fun runSchedule(run: TestRun, report: SummaryReport) {
        val daemons = run.daemons.map {
            daemonSchedule(it, report.newDaemonReport(run.name))
        }

        val intervals = run.intervals.map {
            intervalSchedule(it, report.newIntervalReport(run.name))
        }

        suiteSchedule(run.suite, report.newSuiteReport(run.name))

        daemons.forEach { it.cancel(true) }
        intervals.forEach { it.cancel(true) }

    }

    private fun suiteSchedule(suite: TestSuite, suiteReport: SuiteReport) {
        if (suite.setup != null) {
            setupSchedule(suite.setup!!, suiteReport.newSetupGroup())
        }

        for (group in suite) {
            groupSchedule(group, suiteReport.newGroupReport())
        }

        if (suite.cleanup != null) {
            cleanupSchedule(suite.cleanup!!, suiteReport.newCleanupGroup())
        }
        suiteReport.finish()
    }

    private fun getTimeout(case: TestCase): Long {
        return if (case.properties.timeout > 0) {
            case.properties.timeout
        } else {
            context.case.timeout
        }
    }

    private fun groupSchedule(group: TestGroup, groupReport: GroupReport) {
        val semaphore = Semaphore(group.size)

        for (case in group) {
            semaphore.acquire()
            val thread = WorkPool.pool.submit {
                try {
                    val executor = getExecutor(case)
                    executor.execute(groupReport)
                    logger.info("execute a executor with testcase ${case.name}")
                } catch (e: Exception) {
                    logger.error(e.message)
                    e.printStackTrace()
                    if (panic) {
                        logger.info("panic with error", e)
                        throw YatRuntimeError(e)
                    }
                } finally {
                    semaphore.release()
                }
            }

            val timeout = getTimeout(case)

            if (timeout > 0) {
                WorkPool.pool.execute {
                    try {
                        thread.get(timeout, TimeUnit.SECONDS)
                    } catch (e: TimeoutException) {
                        thread.cancel(true)
                    }
                }
            }
        }

        semaphore.acquire(group.size)

        groupReport.finish()
    }

    private fun cleanupSchedule(cleanup: TestGroup, groupReport: GroupReport) {
        cleanup.forEach {
            val executor = getExecutor(it)
            try {
                executor.execute(groupReport)
            } catch (e: Exception) {
                e.printStackTrace()
                if (panic) {
                    throw YatRuntimeError(e)
                }
            }
        }
        groupReport.finish()
    }

    private fun setupSchedule(setup: TestGroup, groupReport: GroupReport) {
        setup.forEach {
            getExecutor(it).execute(groupReport)
        }
        groupReport.finish()
    }

    companion object {
        private val logger = LoggerFactory.getLogger(Scheduler::class.java)

    }
}
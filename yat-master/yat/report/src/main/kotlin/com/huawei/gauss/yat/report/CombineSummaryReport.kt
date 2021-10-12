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

import java.time.Duration
import java.time.LocalDateTime

class CombineSummaryReport(private val reports: List<SummaryReport>) : SummaryReport {
    internal class CombineGroupReport(private val groupReports: List<GroupReport>) : GroupReport {
        override fun addTest(name: String, result: GroupReport.Result, start: LocalDateTime, time: Duration, meta: Map<String, String>) {
            groupReports.forEach { it.addTest(name, result, start, time, meta) }
        }

        override fun finish() {
            groupReports.forEach { it.finish() }
        }
    }

    internal class CombineSuiteReport(private val suiteReports: List<SuiteReport>) : SuiteReport {
        override fun newGroupReport(): GroupReport {
            return CombineGroupReport(suiteReports.map { it.newGroupReport() })
        }

        override fun newSetupGroup(): GroupReport {
            return CombineGroupReport(suiteReports.map { it.newSetupGroup() })
        }

        override fun newCleanupGroup(): GroupReport {
            return CombineGroupReport(suiteReports.map { it.newCleanupGroup() })
        }

        override fun finish() {
            suiteReports.forEach { it.finish() }
        }
    }

    override fun newSuiteReport(name: String): SuiteReport {
        return CombineSuiteReport(reports.map { it.newSuiteReport(name) })
    }

    override fun newDaemonReport(name: String): SuiteReport {
        return CombineSuiteReport(reports.map { it.newDaemonReport(name) })
    }

    override fun newIntervalReport(name: String): SuiteReport {
        return CombineSuiteReport(reports.map { it.newIntervalReport(name) })
    }

    override fun start() {
        reports.forEach { it.start() }
    }

    override fun finish() {
        reports.forEach { it.finish() }
    }

    fun getSubReport(index: Int): SummaryReport {
        return reports[index]
    }
}
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
 
package com.huawei.gauss.yat.checker

import com.huawei.gauss.yat.scheduler.parser.ScheduleTree

class SchedulerChecker private constructor(
        private val schedule: ScheduleTree,
        private val maxCaseCount: Int,
        private val maxCaseSize: Int,
        private val maxCaseDepth: Int,
        private val casePattern: Regex) : Checker {

    override fun check(): List<String> {
        val errors = mutableListOf<String>()
        var totalCount = 0
        schedule.runList.forEach { run ->
            totalCount += run.suite.testCaseCount()
        }

        if (totalCount > maxCaseCount) {
            errors.add("The number of test cases in the test schedule should not exceed $maxCaseCount")
        }

        schedule.runList.forEach { run ->
            errors.addAll(TestSuiteChecker(run.suite, maxCaseSize, maxCaseDepth, casePattern).check())
        }

        return errors
    }

    data class Builder(
            val schedule: ScheduleTree,
            var maxCaseCount: Int = 500,
            var maxCaseSize: Int = 30000,
            var maxCaseDepth: Int = 1,
            var casePattern: Regex = Regex("[a-zA-Z0-9_]+")
    ) {
        fun maxCaseCount(count: Int) = apply { this.maxCaseCount = count }
        fun maxCaseSize(size: Int) = apply { this.maxCaseSize = size }
        fun maxCaseDepth(depth: Int) = apply { this.maxCaseDepth = depth }
        fun casePattern(pattern: Regex) = apply { this.casePattern = pattern }
        fun build() = SchedulerChecker(schedule, maxCaseCount, maxCaseSize, maxCaseDepth, casePattern)
    }
}
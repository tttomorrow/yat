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

package com.huawei.gauss.yat.scheduler.parser

class ScheduleTree {
    data class SuiteInfo(val caseCount: Int, val subSuiteCount: Int)

    val runList = mutableListOf<TestRun>()
    val runs = mutableMapOf<String, TestRun>()

    fun addRun(run: TestRun) {
        if (run.name in runs) {
            throw ScheduleSyntaxError("duplicate run struct with value ${run.name} found")
        }

        runList.add(run)
        runs[run.name] = run
    }

    fun info(): SuiteInfo {
        var testCaseCount = 0

        runList.forEach { testRun ->
            testRun.suite.forEach { testGroup ->
                testCaseCount += testGroup.size
            }
        }

        val subSuiteCount = if (runList.size == 1 && runList.first().name.isEmpty()) {
            0
        } else {
            runList.size
        }

        return SuiteInfo(testCaseCount, subSuiteCount)
    }
}
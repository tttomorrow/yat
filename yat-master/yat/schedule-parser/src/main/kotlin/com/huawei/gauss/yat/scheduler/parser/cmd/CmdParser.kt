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

package com.huawei.gauss.yat.scheduler.parser.cmd

import com.huawei.gauss.yat.scheduler.parser.Parser
import com.huawei.gauss.yat.scheduler.parser.ScheduleTree
import com.huawei.gauss.yat.scheduler.parser.TestGroup
import com.huawei.gauss.yat.scheduler.parser.TestRun
import com.huawei.gauss.yat.scheduler.parser.TestSuite

class CmdParser(private val line: String) : Parser {
    override fun parse(): ScheduleTree {
        val schedule = ScheduleTree()
        val suite = TestSuite("")
        for (testCase in line.split(",").toTypedArray()) {
            val testGroup = TestGroup(suite)
            testGroup.addTestCase(testCase)
            suite.add(testGroup)
        }
        schedule.addRun(TestRun("", suite))
        return schedule
    }

}
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

import com.huawei.gauss.yat.scheduler.parser.ScheduleTree
import com.huawei.gauss.yat.scheduler.parser.TestGroup
import com.huawei.gauss.yat.setting.YatContext

class CaseMetaMaker(private val context: YatContext) {
    fun makeCaseMeta(tree: ScheduleTree) {
        for (run in tree.runList) {
            val suite = run.suite
            val setup = suite.setup
            setup?.let { makeGroupCaseMeta(it) }
            for (group in suite) {
                makeGroupCaseMeta(group)
            }
            val cleanup = suite.cleanup
            cleanup?.let { makeGroupCaseMeta(it) }
        }
    }

    private fun makeGroupCaseMeta(group: TestGroup) {
        for (testCase in group) {
            testCase.meta = context.suite.vSuite.getCaseMeta(
                    testCase.name,
                    group.suite.run.name,
                    context.case.outSuffix
            )
        }
    }

}
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
 
package com.huawei.gauss.yat.executor

import com.huawei.gauss.yat.common.Benchmark
import com.huawei.gauss.yat.report.GroupReport
import com.huawei.gauss.yat.scheduler.parser.TestCase
import com.huawei.gauss.yat.setting.YatContext

class RegressionExecutor(
        case: TestCase,
        context: YatContext,
        hostName: String = "default") : SingleExecutor(case, context, hostName) {

    override fun execute(groupReport: GroupReport) {
        val bench = Benchmark()
        val meta = mapOf(
                Pair("caseType", case.meta.type.typeName()),
                Pair("suffix", case.meta.type.suffixName()))

        try {
            val preResult: Boolean
            var needDiff = when (super.executeScript()) {
                ExecuteResult.SUCCESS -> {
                    preResult = true
                    true
                }
                ExecuteResult.FAILED -> {
                    preResult = false
                    true
                }
                ExecuteResult.IGNORE -> return
                ExecuteResult.NO_DIFF_FAILED -> {
                    preResult = false
                    false
                }
                ExecuteResult.NO_DIFF_SUCCESS -> {
                    preResult = true
                    false
                }
            }

            needDiff = needDiff && case.properties.diff

            val isOk = if (case.properties.valid) {
                if (needDiff) {
                    if (CaseDiffer(context, case).diff()) {
                        GroupReport.Result.OK
                    } else {
                        GroupReport.Result.FAILED
                    }
                } else {
                    if (preResult) {
                        GroupReport.Result.NO_DIFF_OK
                    } else {
                        GroupReport.Result.NO_DIFF_FAILED
                    }
                }
            } else {
                GroupReport.Result.NO_VALID
            }

            val time = bench.finish()

            groupReport.addTest(case.name, isOk, bench.begin, time, meta)
        } catch (e: InterruptedException) {
            groupReport.addTest(case.name, GroupReport.Result.TIMEOUT, bench.begin, bench.finish(), meta)
        }
    }
}
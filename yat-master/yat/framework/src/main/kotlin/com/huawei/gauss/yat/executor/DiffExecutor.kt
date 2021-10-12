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
import com.huawei.gauss.yat.common.TestCaseSearcher.Type
import com.huawei.gauss.yat.report.GroupReport
import com.huawei.gauss.yat.scheduler.parser.TestCase
import com.huawei.gauss.yat.setting.YatContext

class DiffExecutor(private val case: TestCase, private val context: YatContext) : Executor {
    override fun execute(groupReport: GroupReport) {
        val bench = Benchmark()

        val isOk = when (case.meta.type) {
            Type.UNIT_GROOVY, Type.UNIT_PYTHON, Type.UNIT_SQL -> GroupReport.Result.IGNORE
            else -> {
                if (CaseDiffer(context, case).diff()) {
                    GroupReport.Result.OK
                } else {
                    GroupReport.Result.FAILED;
                }
            }
        }

        val time = bench.finish()

        val meta = mapOf(
                Pair("caseType", case.meta.type.typeName()),
                Pair("suffix", case.meta.type.suffixName()))

        groupReport.addTest(case.name, isOk, bench.begin, time, meta)
    }
}
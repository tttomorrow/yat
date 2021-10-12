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
import com.huawei.gauss.yat.common.TestCaseSearcher
import com.huawei.gauss.yat.diff.JDiffer
import com.huawei.gauss.yat.report.GroupReport
import com.huawei.gauss.yat.scheduler.parser.TestCase
import com.huawei.gauss.yat.script.BaseSqlScript
import com.huawei.gauss.yat.script.FileSqlOutput
import com.huawei.gauss.yat.script.SqlScriptBuilder
import com.huawei.gauss.yat.setting.YatContext
import org.slf4j.LoggerFactory
import java.io.File

class CompareExecutor(
        private val case: TestCase,
        private val context: YatContext,
        private val leftNode: String = "left",
        private val rightNode: String = "right") : Executor {

    companion object {
        val logger = LoggerFactory.getLogger(CompareExecutor::class.java)
    }

    private val leftOutput = FileSqlOutput(File("${case.meta.output.absolutePath}-L"))
    private val rightOutput = FileSqlOutput(File("${case.meta.output.absolutePath}-R"))

    private val leftScript = SqlScriptBuilder()
            .nodeName(leftNode)
            .connectionPool(context.connectionPool)
            .env(context.macro.all())
            .output(leftOutput)
            .build(BaseSqlScript.SqlScriptType.SQLX)

    private val rightScript = SqlScriptBuilder()
            .nodeName(rightNode)
            .connectionPool(context.connectionPool)
            .env(context.macro.all())
            .output(rightOutput)
            .build(BaseSqlScript.SqlScriptType.SQLX)

    override fun execute(groupReport: GroupReport) {
        if (case.meta.type == TestCaseSearcher.Type.SQL) {

            val bench = Benchmark()
            val caseText = case.meta.file.bufferedReader().readText()
            leftScript.execute(caseText)
            rightScript.execute(caseText)

            val time = bench.finish()
            val differ = JDiffer.builder()
                    .leftLines(leftOutput.output.bufferedReader().readLines())
                    .rightLines(rightOutput.output.bufferedReader().readLines())
                    .build()
            val res = differ.diff()

            val diffRes = if (res) {
                GroupReport.Result.OK
            } else {
                File("${case.meta.output.absolutePath}.diff").writeText(differ.diffToReadable())
                GroupReport.Result.FAILED
            }

            val meta = mapOf(
                    Pair("caseType", case.meta.type.typeName()),
                    Pair("suffix", case.meta.type.suffixName())
            )

            groupReport.addTest(case.name, diffRes, bench.begin, time, meta)
        } else {
            logger.warn("compare mode only run sql script, but found script type ${case.meta.type.typeName()}")
        }
    }
}

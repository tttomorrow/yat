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
import com.huawei.gauss.yat.common.YatRuntimeError
import com.huawei.gauss.yat.report.GroupReport
import com.huawei.gauss.yat.scheduler.parser.TestCase
import com.huawei.gauss.yat.script.*
import com.huawei.gauss.yat.setting.YatContext
import java.io.File

open class SingleExecutor(
        protected val case: TestCase,
        protected val context: YatContext,
        protected val nodeName: String = "default") : Executor {

    enum class ExecuteResult { SUCCESS, FAILED, IGNORE, NO_DIFF_SUCCESS, NO_DIFF_FAILED }

    private val host = context.nodes[nodeName] ?: throw YatRuntimeError("Do not found host with value $nodeName")

    override fun execute(groupReport: GroupReport) {
        val meta = mapOf(
                Pair("caseType", case.meta.type.typeName()),
                Pair("suffix", case.meta.type.suffixName())
        )

        val bench = Benchmark() // benchmark time begin
        try {
            val isOk = when (executeScript()) {
                ExecuteResult.SUCCESS -> true
                ExecuteResult.FAILED -> false
                ExecuteResult.IGNORE -> return
                ExecuteResult.NO_DIFF_FAILED -> false
                ExecuteResult.NO_DIFF_SUCCESS -> true
            }
            val time = bench.finish()

            val totalRes = if (case.properties.valid) {
                if (isOk) GroupReport.Result.OK else GroupReport.Result.FAILED
            } else {
                GroupReport.Result.NO_VALID
            }

            groupReport.addTest(case.name, totalRes, bench.begin, time, meta)
        } catch (e: InterruptedException) {
            groupReport.addTest(case.name, GroupReport.Result.TIMEOUT, bench.begin, bench.finish(), meta)
        }
    }

    protected fun executeScript(): ExecuteResult {
        return when (case.meta.type) {
            TestCaseSearcher.Type.SQL -> executeSqlScript()
            TestCaseSearcher.Type.Z_SQL -> executeZSqlScript()
            TestCaseSearcher.Type.SHELL -> executeShellScript()
            TestCaseSearcher.Type.IZ_SQL -> executeIzSqlScript()
            TestCaseSearcher.Type.PYTHON -> executePythonScript()
            TestCaseSearcher.Type.UNIT_PYTHON -> executeUnitPythonScript()
            TestCaseSearcher.Type.UNIT_GROOVY -> executeUnitGroovyScript()
            TestCaseSearcher.Type.GO -> executeGoScript()
            TestCaseSearcher.Type.UNIT_SQL -> executeUnitSqlScript()
            TestCaseSearcher.Type.RANDOM_SQL -> executeRandomSqlScript()
            TestCaseSearcher.Type.G_SQL -> executeGSqlScript()
            TestCaseSearcher.Type.CBO_SQL -> executeCboScript()
            TestCaseSearcher.Type.CBO_SPIDER -> executeGSpider()
            TestCaseSearcher.Type.SPOCK -> executeSopck()
        }
    }

    private fun executeSopck(): ExecuteResult {
        val groovyScript = SpockScript(case.meta.output)

        return if (groovyScript.execute(case.meta.file)) {
            ExecuteResult.NO_DIFF_SUCCESS
        } else {
            ExecuteResult.NO_DIFF_FAILED
        }
    }

    private fun executeGSpider(): ExecuteResult {
        val gSpiderScript = GSpiderScript(
                host.db.type,
                host.db.host,
                host.db.port,
                host.db.user,
                host.db.password,
                case.meta.output,
                context.macro.all())
        return if (gSpiderScript.execute(case.meta.file)) {
            ExecuteResult.NO_DIFF_SUCCESS
        } else {
            ExecuteResult.NO_DIFF_FAILED
        }
    }

    private fun commonSqlBuilder(): SqlScriptBuilder {
        val output = FileSqlOutput(case.meta.output)
        output.echoStatement = context.echoSql
        output.outMode = context.case.outMode

        val timing = FileSqlOutput(File("${case.meta.output.canonicalFile}.timing"))
        val log = FileSqlOutput(File("${case.meta.output.canonicalFile}.log"))

        val builder = SqlScriptBuilder();
        builder.nodeName(nodeName)
                .connectionPool(context.connectionPool)
                .env(context.macro.all())
                .output(output)
                .timing(timing)
                .log(log)
        return builder
    }

    private fun executeCboScript(): ExecuteResult {
        val sqlXScript = commonSqlBuilder().build(BaseSqlScript.SqlScriptType.SQLX)
        val res = sqlXScript.execute(case.meta.file.bufferedReader().readText())

        return if (res) {
            ExecuteResult.NO_DIFF_SUCCESS
        } else {
            ExecuteResult.NO_DIFF_FAILED
        }
    }

    private fun executePythonScript(): ExecuteResult {
        val python = PythonScript(case.meta.output, context.macro.all())
        return if (python.execute(case.meta.file)) {
            ExecuteResult.SUCCESS
        } else {
            ExecuteResult.FAILED
        }
    }

    private fun executeUnitPythonScript(): ExecuteResult {
        val python = UnitPythonScript(
                case.meta.output,
                context.suite.vSuite.testCaseDir.absolutePath,
                context.suite.vSuite.libraryDir.absolutePath,
                context.macro.all())
        return if (python.execute(case.name)) {
            ExecuteResult.NO_DIFF_SUCCESS
        } else {
            ExecuteResult.NO_DIFF_FAILED
        }
    }

    private fun executeIzSqlScript(): ExecuteResult {
        val zSqlScript = makeCmdSqlScript(BaseCmdSqlScript.CmdScriptType.TYPE_ZSQL)
        return if (zSqlScript.iexecute(case.meta.file.bufferedReader().readText())) {
            ExecuteResult.SUCCESS
        } else {
            ExecuteResult.FAILED
        }
    }

    private fun executeZSqlScript(): ExecuteResult {
        val zSqlScript = makeCmdSqlScript(BaseCmdSqlScript.CmdScriptType.TYPE_ZSQL)

        return if (zSqlScript.execute(case.meta.file)) {
            ExecuteResult.SUCCESS
        } else {
            ExecuteResult.FAILED
        }
    }

    private fun executeGSqlScript(): ExecuteResult {
        val gSqlScript = makeCmdSqlScript(BaseCmdSqlScript.CmdScriptType.TYPE_GSQL)

        return if (gSqlScript.execute(case.meta.file)) {
            ExecuteResult.SUCCESS
        } else {
            ExecuteResult.FAILED
        }
    }

    private fun makeCmdSqlScript(type: BaseCmdSqlScript.CmdScriptType): BaseCmdSqlScript {
        val builder = BaseCmdSqlScript.Builder()

        builder.output(case.meta.output)
                .testDir(context.suite.vSuite.workDir.absolutePath)
                .tempDir(context.suite.vSuite.output.tempDir.absolutePath)
                .echo(context.echoSql)
                .env(context.macro.all())
                .user(host.db.user)
                .dbname(host.db.name)
                .password(host.db.password)
                .host(host.db.host)
                .port(host.db.port)
        when (type) {
            BaseCmdSqlScript.CmdScriptType.TYPE_ZSQL -> builder.cmdPath(context.zsql)
            BaseCmdSqlScript.CmdScriptType.TYPE_GSQL -> builder.cmdPath(context.gsql)
        }
        return builder.build(type)
    }

    private fun executeSqlScript(): ExecuteResult {
        val sqlXScript = commonSqlBuilder().build(BaseSqlScript.SqlScriptType.SQLX)

        val res = sqlXScript.execute(case.meta.file.bufferedReader().readText())

        return if (res) {
            ExecuteResult.SUCCESS
        } else {
            ExecuteResult.FAILED
        }
    }

    private fun executeRandomSqlScript(): ExecuteResult {
        val sqlXScript = commonSqlBuilder().build(BaseSqlScript.SqlScriptType.PARALL_SQLX)

        val res = sqlXScript.execute(case.meta.file.bufferedReader().readText())

        return if (res) {
            ExecuteResult.NO_DIFF_SUCCESS
        } else {
            ExecuteResult.NO_DIFF_FAILED
        }
    }

    private fun executeUnitSqlScript(): ExecuteResult {
        val output = FileSqlOutput(case.meta.output)
        output.echoStatement = context.echoSql
        val timing = FileSqlOutput(File("${case.meta.output.canonicalFile}.timing"))
        val log = FileSqlOutput(File("${case.meta.output.canonicalFile}.log"))

        val sqlXScript = SqlScriptBuilder()
                .nodeName(nodeName)
                .connectionPool(context.connectionPool)
                .env(context.macro.all())
                .output(output)
                .timing(timing)
                .log(log)
                .build(BaseSqlScript.SqlScriptType.UNIT_SQLX)

        val res = sqlXScript.execute(case.meta.file.bufferedReader().readText())

        return if (res) {
            ExecuteResult.NO_DIFF_SUCCESS
        } else {
            ExecuteResult.NO_DIFF_FAILED
        }
    }

    private fun executeShellScript(): ExecuteResult {
        val shellScript = ShellScript(case.meta.output, context.macro.all())

        return if (shellScript.execute(case.meta.file)) {
            ExecuteResult.SUCCESS
        } else {
            ExecuteResult.FAILED
        }
    }

    private fun executeUnitGroovyScript(): ExecuteResult {
        val groovyScript = UnitGroovyScript(case.meta.output)

        return if (groovyScript.execute(case.meta.file)) {
            ExecuteResult.NO_DIFF_SUCCESS
        } else {
            ExecuteResult.NO_DIFF_FAILED
        }
    }

    private fun executeGoScript(): ExecuteResult {
        val goScript = GoScript(case.meta.output, context.macro.all())

        return if (goScript.execute(case.meta.file)) {
            ExecuteResult.SUCCESS
        } else {
            ExecuteResult.FAILED
        }
    }
}
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

package com.huawei.gauss.yat.script

import com.huawei.gauss.yat.diff.JDiffer
import com.huawei.gauss.yat.sql.parser.SqlLexError
import com.huawei.gauss.yat.sql.parser.SqlParseError
import com.huawei.gauss.yat.sql.parser.UnitTestSqlParser
import com.huawei.gauss.yat.sql.parser.statement.BlockStatement
import com.huawei.gauss.yat.sql.parser.statement.CommentStatement
import com.huawei.gauss.yat.sql.parser.statement.ConnectStatement
import com.huawei.gauss.yat.sql.parser.statement.DescStatement
import com.huawei.gauss.yat.sql.parser.statement.FreeBlockStatement
import com.huawei.gauss.yat.sql.parser.statement.SetStatement
import com.huawei.gauss.yat.sql.parser.statement.ShellStatement
import com.huawei.gauss.yat.sql.parser.statement.SqlStatement
import com.huawei.gauss.yat.sql.parser.statement.UnitTestStatement
import java.io.ByteArrayOutputStream
import java.io.StringReader

class UnitSqlScript internal constructor(builder: SqlScriptBuilder) : BaseSqlScript(builder) {
    override fun execute(script: String): Boolean {
        try {
            val parser = UnitTestSqlParser(StringReader(script))

            var res = true
            while (parser.hasNext()) {
                when (val statement = parser.nextStatement()) {
                    is FreeBlockStatement -> {
                    }
                    is UnitTestStatement -> res = execUnitTest(statement) && res
                    is CommentStatement -> {
                    }
                    else -> {
                        output.echo("Not support command found")
                        return false
                    }
                }
            }
            return res
        } catch (e: SqlLexError) {
            output.echo("Sql lex error: ${e.message}")
        } catch (e: SqlParseError) {
            output.echo("Sql parse error: ${e.message}")
        } finally {
            close()
        }
        return false
    }

    override fun close() {
        super.close()
    }

    private val originOutput = output

    private fun execUnitTest(statement: UnitTestStatement): Boolean {
        echoTest(statement)

        val out = StreamSqlOutput(ByteArrayOutputStream())
        switchOutput(out)
        execTest(statement.test)

        val unitOut = out.toString()
        out.close()

        switchOutput(originOutput)
        output.echo("#result\n{")
        output.echo(addPrefix(unitOut))
        output.echo("}")

        if (statement.expect.content.isEmpty()) {
            return true
        }

        val differ = JDiffer.builder()
                .leftLines(statement.expect.content.split(Regex("[\r\n]+")))
                .rightLines(unitOut.split(Regex("[\r\n]+")))
                .build()
        return if (differ.diff()) {
            true
        } else {
            output.echo("#diff\n{")
            output.echo(addPrefix(differ.diffToReadable()))
            output.echo("}")
            false
        }
    }

    private fun echoTest(statement: UnitTestStatement) {
        output.echo("${statement.test.name}\n{")
        statement.test.statements.forEach {
            output.echo(it, prefix = "    ")
        }
        output.echo("}")

        if (statement.expect.content.isNotEmpty()) {
            output.echo("${statement.expect.name}\n{")
            output.echo("    ${statement.expect.content}")
            output.echo("}")
        }
    }

    private fun execTest(statement: BlockStatement) {
        statement.statements.forEach {
            when (it) {
                is SqlStatement -> execSql(it)
                is ShellStatement -> execShell(it)
                is ConnectStatement -> execConnect(it)
                is SetStatement -> execSetStatement(it)
                is DescStatement -> execDescStatement(it)
                else -> throw SqlExecuteError("found no support statement: $it")
            }
        }
    }

    private fun addPrefix(str: String): String {
        val buffer = mutableListOf<String>()
        str.split(Regex("[\r\n]+")).forEach {
            buffer.add("    $it")
        }
        return buffer.joinToString("\n")
    }
}
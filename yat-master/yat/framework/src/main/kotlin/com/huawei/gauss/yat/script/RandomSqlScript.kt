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

import com.huawei.gauss.yat.sql.parser.RandomSqlParser
import com.huawei.gauss.yat.sql.parser.SqlLexError
import com.huawei.gauss.yat.sql.parser.SqlParseError
import com.huawei.gauss.yat.sql.parser.statement.BlockStatement
import com.huawei.gauss.yat.sql.parser.statement.RandomSqlStatement
import java.io.StringReader
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import kotlin.random.Random
import kotlin.random.nextLong

class RandomSqlScript internal constructor(private val builder: SqlScriptBuilder) : BaseSqlScript(builder) {
    companion object {
        private val random = Random(System.currentTimeMillis())
    }
    override fun execute(script: String): Boolean {
        try {
            val parser = RandomSqlParser(StringReader(script))

            if (parser.hasNext()) {
                val statement = parser.nextStatement()

                if (parser.hasNext()) {
                    output.echo("only one parallel block allow")
                    return false
                }

                return if (statement is RandomSqlStatement) {
                    execParallelStatement(statement)
                } else {
                    output.echo("Not support command found")
                    false
                }
            }
            return true
        } catch (e: SqlLexError) {
            output.echo("Sql lex error: ${e.message}")
        } catch (e: SqlParseError) {
            output.echo("Sql parse error: ${e.message}")
        } finally {
            close()
        }

        return false
    }

    private fun execParallelStatement(random: RandomSqlStatement): Boolean {
        if (random.setup != null) {
            if (!execCurrentBlock(random.setup!!)) {
                return false
            }
        }

        execParallelAndInject(random.parallel, random.inject)

        return if (random.checker == null) {
            true
        } else {
            execCurrentBlock(random.checker!!)
        }
    }

    private fun execParallelAndInject(parallel: BlockStatement, inject: BlockStatement?) {
        val pool = Executors.newCachedThreadPool()

        try {
            val count = parallel.properties.getInt("count", 10)
            var statementIndex = 0
            parallel.statements.forEach { statement ->
                pool.execute {
                    val newScript = SqlScriptBuilder().connectionPool(connectionPool)
                        .env(env)
                        .nodeName(nodeName)
                        .output(output.newWithSuffix(".parallel.${statementIndex++}"))
                        .timing(timing)
                        .log(log)
                        .build(SqlScriptType.SQLX)
                    (1..count).forEach { _ ->
                        newScript.execXStatement(statement)
                    }
                    newScript.close()
                }
            }

            if (inject != null) {
                val sleep = if (inject.properties.contains("sleep")) {
                    if (inject.properties.isLongRange("sleep")) {
                        random.nextLong(inject.properties.getLongRange("sleep")!!)
                    } else {
                        inject.properties.getLong("sleep", 0)
                    }
                } else {
                    0
                }

                val injectCount = inject.properties.getInt("count", 10)

                pool.execute {
                    if (sleep > 0) {
                        Thread.sleep(sleep)
                    }

                    val newScript = SqlScriptBuilder()
                        .connectionPool(connectionPool)
                        .env(env)
                        .nodeName(nodeName)
                        .output(output.newWithSuffix(".inject"))
                        .log(log)
                        .timing(timing)
                        .build(SqlScriptType.SQLX)
                    (1..injectCount).forEach { _ ->
                        inject.statements.forEach { statement ->
                            newScript.execXStatement(statement)
                        }
                    }
                    newScript.close()
                }
            }
        } finally {
            pool.shutdown()
            pool.awaitTermination(Long.MAX_VALUE, TimeUnit.SECONDS)
        }
    }

    private fun execCurrentBlock(block: BlockStatement): Boolean {
        var res = true
        block.statements.forEach {
            res = execXStatement(it) && res
        }

        return res
    }
}
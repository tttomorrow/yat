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

import com.huawei.gauss.yat.sql.parser.SqlLexError
import com.huawei.gauss.yat.sql.parser.SqlParseError
import com.huawei.gauss.yat.sql.parser.SqlParser
import java.io.StringReader


class SqlScript internal constructor(builder: SqlScriptBuilder) : BaseSqlScript(builder) {
    override fun execute(script: String): Boolean {
        try {
            val parser = SqlParser(StringReader(script))

            var res = true
            while (parser.hasNext()) {
                res = execXStatement(parser.nextStatement()) && res
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
}
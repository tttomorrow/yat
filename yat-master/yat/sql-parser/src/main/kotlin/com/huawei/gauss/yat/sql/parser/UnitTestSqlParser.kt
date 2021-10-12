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

package com.huawei.gauss.yat.sql.parser

import com.huawei.gauss.yat.sql.parser.statement.FreeBlockStatement
import com.huawei.gauss.yat.sql.parser.statement.UnitTestStatement
import com.huawei.gauss.yat.sql.parser.statement.XStatement
import java.io.Reader

class UnitTestSqlParser(reader: Reader) : AbstractSqlParser(reader) {
    override fun parse(): XStatement? {
        val token = skip()
        return if (token == null) {
            null
        } else {
            when {
                token.equalsIgnoreCase(KEY_SETUP) -> parseUnitTestStatement()
                token.equalsIgnoreCase(KEY_CLEANUP) -> parseUnitTestStatement()
                token.equalsIgnoreCase(KEY_TEST) -> parseUnitTestStatement()
                token.equalsIgnoreCase(KEY_COMMENT) -> parseFreeBlock()
                else -> throw parseError("parse statement found unexpect token ${token.value}")
            }
        }
    }

    private fun parseUnitTestStatement(): UnitTestStatement {
        val test = parseBlock()

        val expectToken = skip()

        val expect = if (expectToken == null) {
            nextToken()
            FreeBlockStatement(KEY_EXPECT, "")
        } else {
            when {
                expectToken.equals(KEY_EXPECT) -> parseFreeBlock()
                else -> {
                    FreeBlockStatement(KEY_EXPECT, "")
                }
            }
        }

        return UnitTestStatement(test, expect)
    }
}

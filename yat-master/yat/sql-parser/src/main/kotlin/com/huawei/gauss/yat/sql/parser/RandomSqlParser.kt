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

import com.huawei.gauss.yat.sql.parser.statement.BlockStatement
import com.huawei.gauss.yat.sql.parser.statement.RandomSqlStatement
import com.huawei.gauss.yat.sql.parser.statement.XStatement
import java.io.Reader


class RandomSqlParser(reader: Reader) : AbstractSqlParser(reader) {
    override fun parse(): XStatement? {
        val token = skip()
        return if (token == null) {
            null
        } else {
            parseParallelBlock()
        }
    }

    private fun parseParallelBlock(): RandomSqlStatement {
        var theBlock = parseBlock()
        var setup: BlockStatement? = null

        if (theBlock.name == KEY_SETUP) {
            setup = theBlock
            theBlock = parseBlock()
            if (theBlock.name != KEY_RANDOM) {
                throw parseError("parse random statement found unexpect token ${theBlock.name}")
            }
        }

        if (skip() == null) {
            return RandomSqlStatement(setup, theBlock, null, null)
        }

        var inject: BlockStatement? = null
        var checker: BlockStatement? = null

        var block = parseBlock()
        if (block.name == KEY_INJECT) {
            inject = block
        } else if (block.name == KEY_CHECKER) {
            checker = block
        }

        if (skip() == null) {
            return RandomSqlStatement(setup, theBlock, inject, checker)
        }

        block = parseBlock()
        if (block.name == KEY_INJECT) {
            if (inject != null) {
                throw parseError("parse parallel statement, duplicate inject found")
            }
            inject = block
        } else if (block.name == KEY_CHECKER) {
            if (checker != null) {
                throw parseError("parse parallel statement, duplicate checker found")
            }
            checker = block
        }
        return RandomSqlStatement(setup, theBlock, inject, checker)
    }
}
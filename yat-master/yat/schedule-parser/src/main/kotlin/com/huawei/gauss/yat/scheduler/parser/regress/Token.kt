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

package com.huawei.gauss.yat.scheduler.parser.regress

import com.huawei.gauss.yat.common.lex.Position

class Token(val type: Type, val value: String, val position: Position) {
    enum class Type {
        WORD,
        SYMBOL,
        SPLIT
    }

    companion object {
        const val COLON = ":"
        const val L_BRACKET = "("
        const val R_BRACKET = ")"
        const val EQUAL = "="
        const val SPLIT = "------"

        fun symbol(value: String, position: Position): Token {
            return Token(Type.SYMBOL, value, position)
        }

        fun word(value: String, position: Position): Token {
            return Token(Type.WORD, value, position)
        }

        fun split(position: Position): Token {
            return Token(Type.SPLIT, SPLIT, position)
        }
    }

    init {
        position.column = position.column - value.length
    }

    override fun toString(): String {
        return "Token { type: $type, value: \"$value\", line: ${position.line}, column: ${position.column} }"
    }

    fun isSymbol(): Boolean {
        return type == Type.SYMBOL
    }

    fun isWord(): Boolean {
        return type == Type.WORD
    }

    fun isSplit(): Boolean {
        return type == Type.SPLIT
    }
}
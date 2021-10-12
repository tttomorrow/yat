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

package com.huawei.gauss.yat.scheduler.parser.yat

class Token(val type: Type, val value: String, val line: Int, val column: Int) {
    enum class Type {
        WORD,
        SYMBOL
    }

    companion object {
        const val COLON = ":"
        const val L_PARENTH = "{"
        const val R_PARENTH = "}"
        const val L_BRACE = "("
        const val R_BRACE = ")"
    }

    override fun toString(): String {
        return "Token { type: $type, value: $value, line: $line, column: $column }"
    }

    fun isSymbol(): Boolean {
        return type == Type.SYMBOL
    }

    fun isWord(): Boolean {
        return type == Type.WORD
    }
}
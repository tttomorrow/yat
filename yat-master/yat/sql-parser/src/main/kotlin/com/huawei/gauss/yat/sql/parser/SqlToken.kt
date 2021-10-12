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


class SqlToken private constructor(val type: Type, val value: String, val position: Position) {
    enum class Type {
        WHITE_SPACE,
        CR,
        LF,
        TAB,
        BACK_SLASH,
        SLASH,
        SEMICOLON,
        LEFT_BRACE,
        RIGHT_BRACE,
        LEFT_BRACKET,
        RIGHT_BRACKET,
        COLON,
        SINGLE_QUOTE_VALUE,
        DOUBLE_QUOTE_VALUE,
        GRAVE_VALUE,
        WORLD,
        LINE_COMMENT,
        MULTILINE_COMMENT,
        MACRO_VALUE,
        EQUAL,
        DOLLAR,
        STAR,
        COMMA,
        MINUS,
        QUESTION
    }

    data class Position(val line: Int, val col: Int)

    fun isWhiteSpace(): Boolean {
        return type == Type.WHITE_SPACE
    }

    fun isBlank(): Boolean {
        return type == Type.WHITE_SPACE || type == Type.TAB
    }

    fun isSemicolon(): Boolean {
        return type == Type.SEMICOLON
    }

    fun isColon(): Boolean {
        return type == Type.COLON
    }

    fun isSlash(): Boolean {
        return type == Type.SLASH
    }

    fun isQuestion(): Boolean {
        return type == Type.QUESTION;
    }

    fun isBackSlash(): Boolean {
        return type == Type.BACK_SLASH
    }

    fun isTab(): Boolean {
        return type == Type.TAB
    }

    fun isCR(): Boolean {
        return type == Type.CR
    }

    fun isLF(): Boolean {
        return type == Type.LF
    }

    fun isFeed(): Boolean {
        return type == Type.LF || type == Type.CR
    }

    fun isBrace(): Boolean {
        return type == Type.LEFT_BRACE || type == Type.RIGHT_BRACE
    }

    fun isLeftBrace(): Boolean {
        return type == Type.LEFT_BRACE
    }

    fun isRightBrace(): Boolean {
        return type == Type.RIGHT_BRACE
    }

    fun isBracket(): Boolean {
        return type == Type.LEFT_BRACKET || type == Type.RIGHT_BRACKET
    }

    fun isLeftBracket(): Boolean {
        return type == Type.LEFT_BRACKET
    }

    fun isRightBracket(): Boolean {
        return type == Type.RIGHT_BRACKET
    }

    fun isWord(): Boolean {
        return type == Type.WORLD
    }

    fun isMultilineComment(): Boolean {
        return type == Type.MULTILINE_COMMENT
    }

    fun isLineComemnt(): Boolean {
        return type == Type.LINE_COMMENT
    }

    fun isComment(): Boolean {
        return type == Type.LINE_COMMENT || type == Type.MULTILINE_COMMENT
    }

    fun isDoubleQuote(): Boolean {
        return type == Type.DOUBLE_QUOTE_VALUE
    }

    fun isSingleQuote(): Boolean {
        return type == Type.SINGLE_QUOTE_VALUE
    }

    fun isGrave(): Boolean {
        return type == Type.GRAVE_VALUE
    }

    fun isStart(): Boolean {
        return type == Type.STAR
    }

    fun isMinus(): Boolean {
        return type == Type.MINUS
    }

    fun isComma(): Boolean {
        return type == Type.COMMA
    }

    fun isValue(): Boolean {
        return type == Type.WORLD || type == Type.GRAVE_VALUE || type == Type.SINGLE_QUOTE_VALUE || type == Type.DOUBLE_QUOTE_VALUE
    }

    fun isSymbol(): Boolean {
        return type in symbol2String
    }

    fun isEqual(): Boolean {
        return type == Type.EQUAL
    }

    fun equalsIgnoreCase(other: String): Boolean {
        return other.equals(value, true)
    }

    fun equals(other: String): Boolean {
        return value == other
    }

    fun originValue(): String {
        return when (type) {
            Type.DOUBLE_QUOTE_VALUE -> "\"$value\""
            Type.SINGLE_QUOTE_VALUE -> "'$value'"
            Type.GRAVE_VALUE -> "`$value`"
            Type.LINE_COMMENT -> "--$value"
            Type.MULTILINE_COMMENT -> "/*$value*/"
            Type.MACRO_VALUE -> "\${$value}"
            else -> value
        }
    }

    companion object {
        private val symbol2String = mapOf(
                Pair(Type.SLASH, "/"),
                Pair(Type.BACK_SLASH, "\\"),
                Pair(Type.COLON, ":"),
                Pair(Type.CR, "\r"),
                Pair(Type.LF, "\n"),
                Pair(Type.LEFT_BRACE, "{"),
                Pair(Type.RIGHT_BRACE, "}"),
                Pair(Type.LEFT_BRACKET, "("),
                Pair(Type.RIGHT_BRACKET, ")"),
                Pair(Type.SEMICOLON, ";"),
                Pair(Type.TAB, "\t"),
                Pair(Type.WHITE_SPACE, " "),
                Pair(Type.EQUAL, "="),
                Pair(Type.DOLLAR, "$"),
                Pair(Type.STAR, "*"),
                Pair(Type.MINUS, "-"),
                Pair(Type.COMMA, ","),
                Pair(Type.QUESTION, "?")
        )

        fun symbol(type: Type, position: Position): SqlToken {
            val str = symbol2String[type]
            if (str == null) {
                throw RuntimeException("symbol method require symbol types, found $type")
            } else {
                return SqlToken(type, str, position)
            }
        }

        fun world(value: String, position: Position): SqlToken {
            return SqlToken(Type.WORLD, value, position)
        }

        fun singleQuote(value: String, position: Position): SqlToken {
            return SqlToken(Type.SINGLE_QUOTE_VALUE, value, position)
        }

        fun doubleQuote(value: String, position: Position): SqlToken {
            return SqlToken(Type.DOUBLE_QUOTE_VALUE, value, position)
        }

        fun lineComment(value: String, position: Position): SqlToken {
            return SqlToken(Type.LINE_COMMENT, value, position)
        }

        fun multilineComment(value: String, position: Position): SqlToken {
            return SqlToken(Type.MULTILINE_COMMENT, value, position)
        }

        fun grave(value: String, position: Position): SqlToken {
            return SqlToken(Type.GRAVE_VALUE, value, position)
        }

        fun macro(value: String, position: Position): SqlToken {
            return SqlToken(Type.MACRO_VALUE, value, position)
        }
    }
}
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

import com.huawei.gauss.yat.common.lex.PeekReader
import java.io.Reader

class SqlLex(reader: Reader) {
    private val reader = PeekReader(reader, 3)

    private fun position(): SqlToken.Position {
        val pos = reader.position();
        return SqlToken.Position(pos.line, pos.column)
    }

    fun nextToken(): SqlToken? {
        return lexCommon()
    }

    private fun lexCommon(): SqlToken? {
        return when (val ch = reader.peek()) {
            SINGLE_QUOTE -> lexQuoteValue(SINGLE_QUOTE)
            DOUBLE_QUOTE -> lexQuoteValue(DOUBLE_QUOTE)
            GRAVE -> lexQuoteValue(GRAVE)
            MINUS -> lexPossibleLineComment()
            SLASH -> lexPossibleMultiLineComment()
            DOLLAR -> lexPossibleMacroValue()
            EOF -> null
            else -> {
                val tokenType = symbolMap[ch]
                if (tokenType == null) {
                    lexWorldValue()
                } else {
                    reader.next()
                    SqlToken.symbol(tokenType, position())
                }
            }
        }
    }

    private fun lexPossibleMacroValue(): SqlToken {
        return when (reader.peek(1)) {
            EOF -> {
                reader.next()
                SqlToken.symbol(SqlToken.Type.DOLLAR, position())
            }
            LEFT_BRACE -> lexMacroValue()
            else -> {
                reader.next()
                SqlToken.symbol(SqlToken.Type.DOLLAR, position())
            }
        }
    }

    private fun lexMacroValue(): SqlToken {
        val buffer = mutableListOf<Char>()

        var ch = reader.next()
        if (ch != DOLLAR || reader.next() != LEFT_BRACE) {
            throw SqlLexError("expect \${, found ${ch.toChar()}", reader.position())
        }
        ch = reader.next()
        while (ch in macroValueLexSet) {
            buffer.add(ch.toChar())
            ch = reader.next()
        }

        if (ch == RIGHT_BRACE) {
            return SqlToken.macro(String(buffer.toCharArray()), position())
        }

        throw SqlLexError("found broken macro value define", reader.position())
    }

    private fun lexPossibleMultiLineComment(): SqlToken {
        return when (reader.peek(1)) {
            STAR -> lexMultiLineComment()
            else -> {
                reader.next()
                SqlToken.symbol(SqlToken.Type.SLASH, position())
            }
        }
    }

    private fun lexPossibleLineComment(): SqlToken {
        return when (reader.peek(1)) {
            MINUS -> lexLineComment()
            else -> {
                reader.next()
                SqlToken.symbol(SqlToken.Type.MINUS, position())
            }
        }
    }

    private fun lexMultiLineComment(): SqlToken {
        val buffer = mutableListOf<Char>()

        var ch = reader.next()
        if (ch != SLASH || reader.next() != STAR) {
            throw SqlLexError("expect /*, found ${ch.toChar()}", reader.position())
        }
        ch = reader.next()
        while (true) {
            if (ch == EOF) {
                throw SqlLexError("not complete multiline comment found", reader.position())
            }

            if (ch == STAR) {
                ch = reader.next()
                if (ch == SLASH) {
                    return SqlToken.multilineComment(String(buffer.toCharArray()), position())
                } else {
                    buffer.add(STAR.toChar())
                }
            }
            buffer.add(ch.toChar())
            ch = reader.next()
        }
    }

    private fun lexLineComment(): SqlToken {
        val buffer = mutableListOf<Char>()

        var ch = reader.next()
        if (ch != MINUS || reader.next() != MINUS) {
            throw SqlLexError("expect --, found ${ch.toChar()}", reader.position())
        }

        ch = reader.next()
        while (ch != LF && ch != CR && ch != EOF) {
            buffer.add(ch.toChar())
            ch = reader.next()
        }

        return SqlToken.lineComment(String(buffer.toCharArray()), position())
    }

    private fun lexQuoteValue(quote: Int): SqlToken {
        val value = if (quote == SINGLE_QUOTE) {
            lexSingleQuoteString()
        } else {
            lexQuoteString(quote)
        }

        return when (quote) {
            SINGLE_QUOTE -> SqlToken.singleQuote(value, position())
            DOUBLE_QUOTE -> SqlToken.doubleQuote(value, position())
            GRAVE -> SqlToken.grave(value, position())
            else -> throw RuntimeException("error when call lexQuoteValue")
        }
    }

    private fun lexWorldValue(): SqlToken {
        val buffer = mutableListOf<Char>()

        var ch = reader.peek()
        while (ch !in workBreaker) {
            reader.next()
            buffer.add(ch.toChar())
            ch = reader.peek()
        }

        return if (ch == EOF) {
            SqlToken.world(String(buffer.toCharArray()), position())
        } else {
            SqlToken.world(String(buffer.toCharArray()), position())
        }
    }

    private fun lexSingleQuoteString(): String {
        val buffer = mutableListOf<Char>()
        var ch = reader.next()
        if (ch != SINGLE_QUOTE) {
            throw SqlLexError("expect ${SINGLE_QUOTE.toChar()}, found ${ch.toChar()}", reader.position())
        }

        ch = reader.next()

        while (ch != EOF) {
            if (ch == SINGLE_QUOTE ) {
                ch = reader.peek()
                if (ch == SINGLE_QUOTE) {
                    buffer.add(ch.toChar())
                    buffer.add(ch.toChar())
                    reader.next()
                } else {
                    break
                }
            } else {
                buffer.add(ch.toChar())
            }
            ch = reader.next()
        }

        if (ch == EOF) {
            throw SqlLexError("not complete quoted value found", reader.position())
        }

        return String(buffer.toCharArray())
    }

    private fun lexQuoteString(quote: Int): String {
        val buffer = mutableListOf<Char>()

        var ch = reader.next()
        if (ch != quote) {
            throw SqlLexError("expect $quote, found $ch", reader.position())
        }
        ch = reader.next()

        while (ch != quote && ch != EOF) {
            buffer.add(ch.toChar())
            ch = reader.next()
        }

        if (ch == EOF) {
            throw SqlLexError("not complete quoted value found", reader.position())
        }

        return String(buffer.toCharArray())
    }

    companion object {
        private const val WHITE_SPACE = ' '.code
        private const val TAB = '\t'.code
        private const val CR = '\r'.code
        private const val LF = '\n'.code
        private const val COLON = ':'.code
        private const val SEMICOLON = ';'.code
        private const val LEFT_BRACE = '{'.code
        private const val RIGHT_BRACE = '}'.code
        private const val LEFT_BRACKET = '('.code
        private const val RIGHT_BRACKET = ')'.code
        private const val SLASH = '/'.code
        private const val BACK_SLASH = '\\'.code
        private const val SINGLE_QUOTE = '\''.code
        private const val DOUBLE_QUOTE = '"'.code
        private const val GRAVE = '`'.code
        private const val MINUS = '-'.code
        private const val EOF = -1
        private const val STAR = '*'.code
        private const val DOLLAR = '$'.code
        private const val EQUAL = '='.code
        private const val COMMA = ','.code
        private const val QUESTION = '?'.code

        private val symbolMap = mapOf(
                Pair(WHITE_SPACE, SqlToken.Type.WHITE_SPACE),
                Pair(TAB, SqlToken.Type.TAB),
                Pair(CR, SqlToken.Type.CR),
                Pair(LF, SqlToken.Type.LF),
                Pair(COLON, SqlToken.Type.COLON),
                Pair(SEMICOLON, SqlToken.Type.SEMICOLON),
                Pair(LEFT_BRACE, SqlToken.Type.LEFT_BRACE),
                Pair(RIGHT_BRACE, SqlToken.Type.RIGHT_BRACE),
                Pair(LEFT_BRACKET, SqlToken.Type.LEFT_BRACKET),
                Pair(RIGHT_BRACKET, SqlToken.Type.RIGHT_BRACKET),
                Pair(BACK_SLASH, SqlToken.Type.BACK_SLASH),
                Pair(EQUAL, SqlToken.Type.EQUAL),
                Pair(STAR, SqlToken.Type.STAR),
                Pair(COMMA, SqlToken.Type.COMMA),
                Pair(QUESTION, SqlToken.Type.QUESTION)
        )

        private val workBreaker = setOf(
                WHITE_SPACE,
                TAB,
                CR,
                LF,
                COLON,
                SEMICOLON,
                LEFT_BRACE,
                RIGHT_BRACE,
                LEFT_BRACKET,
                RIGHT_BRACKET,
                SLASH,
                BACK_SLASH,
                SINGLE_QUOTE,
                DOUBLE_QUOTE,
                GRAVE,
                MINUS,
                STAR,
                DOLLAR,
                EQUAL,
                COMMA,
                EOF,
                QUESTION
        )

        private val macroValueLexSet = setOf(*"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_".map { it.code }.toTypedArray())
    }
}
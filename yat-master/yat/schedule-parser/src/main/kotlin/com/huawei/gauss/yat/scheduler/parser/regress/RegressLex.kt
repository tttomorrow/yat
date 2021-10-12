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

import com.huawei.gauss.yat.common.lex.PeekReader
import com.huawei.gauss.yat.scheduler.parser.ScheduleSyntaxError
import java.io.Reader

class RegressLex(stream: Reader) {
    companion object {
        private const val WHITE_SPACE = ' '.code
        private const val TAB = '\t'.code
        private const val CR = '\r'.code
        private const val LF = '\n'.code
        private const val EOF = -1
        private const val COLON = ':'.code
        private const val EQUAL = '='.code
        private const val L_BRACKET = '('.code
        private const val R_BRACKET = ')'.code
        private const val QUOTE = '\''.code
        private const val MINUS = '-'.code
        private const val LINE_COMMENT_MARK = '#'.code
        private const val backSlash = '\\'.code

        private val blanks = setOf(WHITE_SPACE, TAB, CR, LF)
        private val wordSplit = setOf(WHITE_SPACE, TAB, CR, LF, EOF, COLON, QUOTE, EQUAL, L_BRACKET, R_BRACKET)
    }

    private val reader = PeekReader(stream, 7);
    private var tokenCache: Token? = null

    fun nextToken(): Token {
        return if (tokenCache == null) {
            lexOne() ?: throw NoSuchElementException("there is no token exists")
        } else {
            val res = tokenCache
            tokenCache = null
            res!!
        }
    }

    fun hasNext(): Boolean {
        return if (tokenCache != null) {
            true
        } else {
            tokenCache = lexOne()
            tokenCache != null
        }
    }

    private fun lexOne(): Token? {
        var ch = skipBlank()
        while (ch == LINE_COMMENT_MARK) {
            skipComment()
            ch = skipBlank()
        }
        return when (ch) {
            EOF -> null
            COLON -> {
                reader.next()
                Token.symbol(":", reader.position())
            }
            EQUAL -> {
                reader.next()
                Token.symbol("=", reader.position())
            }
            L_BRACKET -> {
                reader.next()
                Token.symbol("(", reader.position())
            }
            R_BRACKET -> {
                reader.next()
                Token.symbol(")", reader.position())
            }
            QUOTE -> lexQuoteWord()
            MINUS -> lexSplit()
            else -> {
                lexWord()
            }
        }
    }

    private fun skipComment() {
        var ch = reader.next()
        if (ch != LINE_COMMENT_MARK) {
            throw ScheduleSyntaxError("comment must begin with ${LINE_COMMENT_MARK.toChar()}")
        }
        ch = reader.next()
        while (ch != LF && ch != EOF) {
            ch = reader.next()
        }
    }

    private fun skipBlank(): Int {
        var ch = reader.peek()
        while (ch in blanks) {
            reader.next()
            ch = reader.peek()
        }

        return ch
    }


    private fun lexWord(): Token {
        var ch = reader.peek()
        val buffer = mutableListOf<Char>()

        while (ch !in wordSplit) {
            reader.next()
            buffer.add(ch.toChar())
            ch = reader.peek()
        }

        return Token.word(String(buffer.toCharArray()), reader.position())
    }

    private fun lexQuoteWord(): Token {
        var ch = reader.next()
        if (ch != QUOTE) {
            throw ScheduleSyntaxError("expect ', found ${ch.toChar()}")
        }

        val buffer = mutableListOf<Char>()
        ch = reader.next()

        while (ch != EOF && ch != QUOTE) {
            if (ch == backSlash) {
                ch = reader.next()
                if (ch != backSlash && ch != QUOTE) {
                    throw ScheduleSyntaxError("found not support escape charset \\$ch", reader.position())
                }
            }

            buffer.add(ch.toChar())
            ch = reader.next()
        }

        if (ch == EOF) {
            throw ScheduleSyntaxError("not complete quote value found", reader.position())
        }

        return Token.word(String(buffer.toCharArray()), reader.position())
    }

    private fun lexSplit(): Token {
        var isSplit = true
        for (i in (0..5)) {
            if (reader.peek(i) != MINUS) {
                isSplit = false
                break
            }
        }

        return if (isSplit) {
            Token.split(reader.position())
        } else {
            lexWord()
        }
    }
}
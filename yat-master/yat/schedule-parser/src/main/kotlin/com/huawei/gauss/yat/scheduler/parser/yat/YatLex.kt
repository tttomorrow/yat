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

import com.huawei.gauss.yat.scheduler.parser.ScheduleSyntaxError
import java.io.Reader

class YatLex(private val reader: Reader) {
    private var line = 1
    private var column = 1
    private val tokens = mutableListOf<Token>()

    fun lex(): List<Token> {
        var ch = skipBlank()

        while (ch != -1) {
            when (ch) {
                COLON -> tokens.add(newToken(Token.Type.SYMBOL, ":"))
                L_BRACE -> tokens.add(newToken(Token.Type.SYMBOL, "{"))
                R_BRACE -> tokens.add(newToken(Token.Type.SYMBOL, "}"))
                L_BRACKET -> tokens.add(newToken(Token.Type.SYMBOL, "("))
                R_BRACKET -> tokens.add(newToken(Token.Type.SYMBOL, ")"))
                QUOTE -> tokens.add(lexQuoteWord())
                COMMENT -> skipSingleLineComment()
                PERCENT -> skipMultiLineComment()
                else -> tokens.addAll(lexWord(ch))

            }

            ch = skipBlank()
        }

        return tokens
    }

    private fun skipSingleLineComment() {
        do {
            val ch = read()
        } while (ch != ENTER && ch != -1)
    }

    private fun skipMultiLineComment() {
        do {
            val ch = read()
            if (ch == -1) {
                throw ScheduleSyntaxError("broken multiline comment found", line, column)
            }
        } while (ch != PERCENT)
    }

    private fun lexQuoteWord(): Token {
        var ch = read()
        val buffer = mutableListOf<Char>()

        while (ch != QUOTE && ch != EOF) {
            if (ch == backSlash) {
                ch = read()
                if (ch != backSlash && ch != QUOTE) {
                    throw ScheduleSyntaxError("found not support escape charset \\$ch", line, column)
                }
            }

            buffer.add(ch.toChar())
            ch = read()
        }

        if (ch == EOF) {
            throw ScheduleSyntaxError("not complete quote value found", line, column)
        }
        val word = String(buffer.toCharArray())
        return newToken(Token.Type.WORD, word)
    }

    private fun lexWord(pre: Int): Array<Token> {
        val buffer = mutableListOf<Char>()
        buffer.add(pre.toChar())
        var ch = read()

        while (true) {
            if (ch in blanks || ch == -1) {
                val word = String(buffer.toCharArray())
                return arrayOf(newToken(Token.Type.WORD, word))
            } else if (ch in symbols) {
                val word = String(buffer.toCharArray())
                return arrayOf(newToken(Token.Type.WORD, word), symbol2Token(ch))
            } else {
                buffer.add(ch.toChar())
            }

            ch = read()
        }
    }

    private fun skipBlank(): Int {
        var ch = read()

        while (ch in blanks) {
            ch = read()
        }
        return ch
    }

    private fun read(): Int {
        val ch = reader.read()
        if (ch == ENTER) {
            line++
            column = 0
        }

        column++
        return ch
    }

    private fun newToken(type: Token.Type, value: String): Token {
        return Token(type, value, line, column)
    }

    private fun symbol2Token(symbol: Int): Token {
        return when (symbol) {
            COLON -> newToken(Token.Type.SYMBOL, ":")
            L_BRACE -> newToken(Token.Type.SYMBOL, "{")
            R_BRACE -> newToken(Token.Type.SYMBOL, "}")
            L_BRACKET -> newToken(Token.Type.SYMBOL, "(")
            R_BRACKET -> newToken(Token.Type.SYMBOL, ")")
            else -> {
                throw ScheduleSyntaxError("unknown symbols to translate")
            }
        }
    }

    companion object {
        private val blanks = arrayListOf(' '.code, '\r'.code, '\t'.code, '\n'.code)

        private const val COLON = ':'.code
        private const val L_BRACE = '{'.code
        private const val R_BRACE = '}'.code
        private const val L_BRACKET = '('.code
        private const val R_BRACKET = ')'.code
        private const val QUOTE = '\''.code
        private const val ENTER = '\n'.code
        private const val COMMENT = '#'.code
        private const val PERCENT = '%'.code
        private const val backSlash = '\\'.code
        private const val EOF = -1

        private val symbols = arrayListOf(COLON, L_BRACE, R_BRACE, L_BRACKET, R_BRACKET)
    }
}
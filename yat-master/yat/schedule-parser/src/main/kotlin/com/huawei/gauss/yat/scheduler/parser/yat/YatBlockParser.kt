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

internal class YatBlockParser(stream: Reader) {

    private val iterator: Iterator<Token> = YatLex(stream).lex().iterator()
    private var line = 0
    private var column = 0

    fun allBlocks(): List<BlockNode> {
        val blocks = mutableListOf<BlockNode>()
        var block = nextBlock()

        while (block != null) {
            blocks.add(block)
            block = nextBlock()
        }

        return blocks
    }

    fun nextBlock(): BlockNode? {
        return if (iterator.hasNext()) {
            parseBlock()
        } else {
            null
        }
    }

    private fun parseBlock(): BlockNode {
        var token = next()

        if (token.type != Token.Type.WORD) {
            throw ScheduleSyntaxError("parse block: expect a word, but get ${token.type} value ${token.value}", line, column)
        }

        val block = BlockNode(token.value)

        token = next()

        when (token.value) {
            Token.L_PARENTH -> block.body.addAll(parseItemsNode())
            else -> throw ScheduleSyntaxError("parse block: expect {, but get ${token.type} value ${token.value}", line, column)
        }

        return block
    }

    private fun parseItemsNode(): List<ItemsNode> {
        var token = next()

        if (token.value == Token.R_PARENTH) {
            return arrayListOf()
        }

        if (token.type != Token.Type.WORD) {
            throw ScheduleSyntaxError("parse item: expect a word, but get ${token.type} value ${token.value}", line, column)
        }
        var name = token.value

        token = next()

        if (token.value != Token.COLON) {
            throw ScheduleSyntaxError("parse item: expect :, but get ${token.type} value ${token.value}", line, column)
        }

        val items = mutableListOf<ItemsNode>()
        do {
            val pair = parseItemNode(name)
            items.add(pair.second)
            name = pair.first
        } while (pair.first.isNotEmpty())

        return items
    }

    private fun parseItemNode(name: String): Pair<String, ItemsNode> {
        val item = ItemsNode(name)

        var token = next()
        val values = mutableListOf<ElementNode>()

        while (token.value != Token.R_PARENTH) {
            if (token.isSymbol() && token.value == Token.COLON) {
                if (values.size < 2) {
                    throw ScheduleSyntaxError("parse item node: bad item found with ${item.name}", line, column)
                }

                item.values.addAll(values.slice(IntRange(0, values.size - 2)))
                return Pair(values.last().value, item)
            }

            if (token.isWord()) {
                val element = ElementNode(token.value)
                values.add(element)
                token = next()
                if (token.isSymbol() && token.value == Token.L_BRACE) {
                    element.properties.putAll(parseProperties())
                } else {
                    continue
                }
            } else {
                throw ScheduleSyntaxError("parse item node: expect a word, but get ${token.type} value ${token.value}", line, column)
            }

            token = next()
        }

        if (values.size < 1) {
            throw ScheduleSyntaxError("parse item node: broken item found with ${item.name}", line, column)
        }

        item.values.addAll(values)
        return Pair("", item)
    }

    private fun parseProperties(): Map<String, String> {
        var token = next()

        val res = mutableMapOf<String, String>()

        while (token.value != Token.R_BRACE) {
            val key = token.value
            token = next()
            if (token.value == Token.COLON) {
                token = next()
                if (token.type == Token.Type.WORD) {
                    val value = token.value
                    res[key] = value
                } else {
                    throw ScheduleSyntaxError("parse item properties: expect a word, ${token.value} found", line, column)
                }
            } else {
                throw ScheduleSyntaxError("parse item properties: expect :, ${token.value} found", line, column)
            }
            token = next()
        }

        return res
    }

    private fun next(): Token {
        if (hasNext()) {
            val token = iterator.next()
            line = token.line
            column = token.column

            return token
        } else {
            throw ScheduleSyntaxError("unexpected EOF found", line, column)
        }
    }

    private fun hasNext(): Boolean {
        return iterator.hasNext()
    }
}
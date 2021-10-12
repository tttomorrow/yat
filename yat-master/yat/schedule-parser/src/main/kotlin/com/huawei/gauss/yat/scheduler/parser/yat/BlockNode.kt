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

class BlockNode(val name: String) {
    val body = mutableListOf<ItemsNode>()

    fun trySearchBody(name: String): ItemsNode? {
        return body.find { it.name == name }
    }

    fun searchBody(name: String): ItemsNode {
        return trySearchBody(name) ?: throw ScheduleSyntaxError("${this.name} struct should have $name item")
    }

    private fun getOneElement(item: ItemsNode): ElementNode {
        if (item.values.size != 1) {
            throw ScheduleSyntaxError("$name struct ${item.name} item only allow 1 value")
        }
        return item.values[0]
    }

    private fun getTwoElement(item: ItemsNode): Pair<ElementNode, ElementNode> {
        if (item.values.size != 2) {
            throw ScheduleSyntaxError("$name struct ${item.name} item only allow 2 value")
        }
        return Pair(item.values[0], item.values[1])
    }

    fun parseOneElement(propName: String): ElementNode {
        val prop = trySearchBody(propName) ?: throw ScheduleSyntaxError("$name struct need item $propName")
        return getOneElement(prop)
    }

    fun parseTwoELement(propName: String): Pair<ElementNode, ElementNode> {
        val prop = trySearchBody(propName) ?: throw ScheduleSyntaxError("$name struct need item $propName")
        return getTwoElement(prop)
    }

    fun tryParseOneElement(propName: String): ElementNode? {
        val prop = trySearchBody(propName)
        return if (prop == null) {
            null
        } else {
            getOneElement(prop)
        }
    }

    fun tryParseTwoElement(propName: String): Pair<ElementNode, ElementNode>? {
        val prop = trySearchBody(propName)
        return if (prop == null) {
            null
        } else {
            getTwoElement(prop)
        }
    }
}
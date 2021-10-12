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

class ItemsNode(val name: String) {
    val values = mutableListOf<ElementNode>()

    fun parseOneElement(): ElementNode {
        if (values.size != 1) {
            throw ScheduleSyntaxError("item node $name only require 1 element")
        }
        return values[0]
    }

    fun parseTwoElement(): Pair<ElementNode, ElementNode> {
        if (values.size != 2) {
            throw ScheduleSyntaxError("item node $name only require 2 element")
        }
        return Pair(values[0], values[1])
    }
}
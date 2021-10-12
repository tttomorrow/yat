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

package com.huawei.gauss.yat.common

class MacroReplacer(private val text: String) {
    fun replace(map: Map<String, String>): String {
        val builder = StringBuilder()

        val matchers = Regex("\\$\\{ *([a-zA-Z0-9_]+) *}").findAll(text)
        var index = 0
        matchers.forEach {
            val key = it.groupValues[1]
            if (map.containsKey(key)) {
                builder.append(text.subSequence(index, it.range.first))
                builder.append(map[key])
            } else {
                builder.append(text.subSequence(index, it.range.last + 1))
            }
            index = it.range.last + 1
        }

        builder.append(text.subSequence(index, text.length))

        return builder.toString()
    }
}
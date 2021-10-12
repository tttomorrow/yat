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

package com.huawei.gauss.yat.sql.parser.statement

import com.huawei.gauss.yat.sql.parser.BlockProperties

class BlockStatement(val name: String, properties: Map<String, String>, val statements: List<XStatement>) : XStatement {
    val properties = BlockProperties(properties)

    override fun toString(): String {
        val buffer = StringBuilder("$name { \n\tproperties: {\n")

        properties.forEach { (k, v) ->
            buffer.append("\t\t{ key: \"$k\", value: \"$v\" }\n")
        }

        buffer.append("\t}\n\tstatements: {\n")

        statements.forEach {
            it.toString().split(Regex("[\\r\\n]{1,2}")).forEach { line ->
                if (line.isNotEmpty()) {
                    buffer.append("\t\t$line\n")
                }
            }
        }
        buffer.append("\t}\n}")

        return buffer.toString()
    }
}
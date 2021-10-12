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


class BlockProperties(private val properties: Map<String, String>) : Iterable<Map.Entry<String, String>> {
    fun get(name: String): String? {
        return properties[name]
    }

    fun get(name: String, default: String): String {
        return if (properties[name] == null) {
            default
        } else {
            properties[name] ?: error("can not found key $name")
        }
    }

    fun getDouble(name: String): Double? {
        try {
            return properties[name]?.toDouble()
        } catch (e: NumberFormatException) {
            throw SqlParseError("expect integer string")
        }
    }

    fun getDouble(name: String, default: Double): Double {
        return if (properties[name] == null) {
            default
        } else {
            try {
                (properties[name] ?: error("can not found key $name")).toDouble()
            } catch (e: NumberFormatException) {
                throw SqlParseError("expect integer string")
            }
        }
    }

    fun getInt(name: String): Int? {
        try {
            return properties[name]?.toInt()
        } catch (e: NumberFormatException) {
            throw SqlParseError("expect integer string")
        }
    }

    fun getInt(name: String, default: Int): Int {
        return if (properties[name] == null) {
            default
        } else {
            try {
                (properties[name] ?: error("can not found key $name")).toInt()
            } catch (e: NumberFormatException) {
                throw SqlParseError("expect integer string")
            }
        }
    }

    fun getLong(name: String): Long? {
        try {
            return properties[name]?.toLong()
        } catch (e: NumberFormatException) {
            throw SqlParseError("expect integer string")
        }
    }

    fun getLong(name: String, default: Long): Long {
        return if (properties[name] == null) {
            default
        } else {
            try {
                (properties[name] ?: throw SqlParseError("can not found key $name")).toLong()
            } catch (e: NumberFormatException) {
                throw SqlParseError("expect integer string")
            }
        }
    }

    fun getLongRange(name: String): LongRange? {
        try {
            val splits = properties[name]?.split(',') ?: return null
            val range = splits.map { it.trim().toLong() }
            if (range.size != 2) {
                throw SqlParseError("invalid range text of key $name")
            } else {
                return LongRange(range[0], range[1])
            }
        } catch (e: java.lang.NumberFormatException) {
            throw SqlParseError("expect integer string")
        }
    }

    fun getLongRange(name: String, default: LongRange): LongRange {
        return if (properties[name] == null) {
            default
        } else {
            getLongRange(name)!!
        }
    }

    fun isLongRange(name: String): Boolean {
        return ',' in properties[name]!!
    }

    fun getBoolean(name: String): Boolean ? {
        return properties[name]?.toBoolean()
    }

    fun getBoolean(name: String, default: Boolean): Boolean {
        return if (properties[name] == null) {
            default
        } else {
            (properties[name] ?: error("can not found key $name")).toBoolean()
        }
    }

    fun contains(name: String): Boolean {
        return properties.containsKey(name)
    }

    override fun iterator(): Iterator<Map.Entry<String, String>> {
        return properties.iterator()
    }
}

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

package com.huawei.gauss.yat.setting

import java.io.File


class DataParser(private val settingFile: File) {
    fun parseInt(@Suppress("UNUSED_PARAMETER") key: String, value: String): Int {
        return value.toInt()
    }

    fun parseFilling(key: String, value: String): Char {
        if (value.length == 1) {
            return value[0]
        } else {
            throw SettingParseError("Parsing configure file ${settingFile.absoluteFile} failed with key $key, require one charset but get $value")
        }
    }

    fun parseBool(key: String, value: String): Boolean {
        return when (value) {
            "true", "1" -> true
            "false", "0" -> false
            else -> throw SettingParseError("Parsing configure file ${settingFile.absoluteFile} failed with key $key, required boolean value but found $value")
        }
    }

    fun parseSize(key: String, value: String): Int {
        val matcher = longSizeRegex.matchEntire(value)
        if (matcher == null) {
            throw SettingParseError("Parsing configure file ${settingFile.absoluteFile} failed with key $key, input value is not a legal size syntax: $value")
        } else {
            val size = matcher.groupValues[1].toInt()
            val measureString = matcher.groupValues[2]
            val measure = measureMap[measureString]

            if (measure == null) {
                throw IllegalArgumentException("Parsing configure file ${settingFile.absoluteFile} failed with key $key, input value is not a legal size syntax: $value")
            } else {
                return size * measure
            }
        }
    }

    companion object {

        private val measureMap = mapOf(
            Pair("K", 1000),
            Pair("KB", 1000),
            Pair("M", 1000000),
            Pair("MB", 1000000),
            Pair("B", 1),
            Pair("G", 1000000000),
            Pair("GB", 1000000000)
        )

        private val longSizeRegex = Regex("([0-9]+) *(KB|K|MB|M|G|GB|B)")
    }
}
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

import com.huawei.gauss.yat.common.MacroReplacer
import com.huawei.gauss.yat.common.YatRuntimeError
import org.yaml.snakeyaml.Yaml
import java.io.File

class Macro {
    private val properties = mutableMapOf<String, String>()

    init {
        System.getenv().forEach { (k, v) ->
            properties[k] = v
        }
    }

    fun set(key: String, value: String) {
        properties[key] = value
    }

    fun load(file: File) {
        if (file.name.endsWith(".yaml") || file.name.endsWith(".yml")) {
            loadFromYml(file)
        } else {
            throw YatRuntimeError("macro file ${file.absoluteFile} is illegal")
        }
    }

    private fun loadFromYml(file: File) {
        val yml = Yaml()
        val loadMacros: Map<String, Any>? = yml.load(file.reader())

        loadMacros?.forEach { (k, v) ->
            properties[k] = v.toString()
        }
    }

    fun get(name: String, default: String): String {
        val v = properties[name]
        return if (v == null) {
            MacroReplacer(default).replace(properties)
        } else {
            MacroReplacer(v).replace(properties)
        }
    }

    fun get(name: String): String? {
        val v = properties[name]
        return if (v == null) {
            null
        } else {
            MacroReplacer(v).replace(properties)
        }
    }

    fun all(): Map<String, String> {
        val res = mutableMapOf<String, String>()
        properties.forEach { (k, v) ->
            res[k] = MacroReplacer(v).replace(properties)
        }

        return res
    }
}
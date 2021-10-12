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

import com.huawei.gauss.yat.common.YatRuntimeError
import org.yaml.snakeyaml.Yaml
import java.io.File

class YmlSettingsParser(private val settingFile: File, private val context: YatContext) {
    private val dataParser = DataParser(settingFile)

    fun parse() {
        val yml = Yaml()
        val settings: Map<String, Any> = yml.load(settingFile.reader()) ?: return
        try {
            parseSettings(settings)
        } catch (e: ClassCastException) {
            throw YatRuntimeError("parse configure file: ${settingFile.absolutePath} failed with error: ${e.message}", e)
        }
    }

    private fun parseSettings(settings: Map<String, Any>) = settings.forEach { (k, v) ->
        when (k) {
            KEY_COMPARE_TYPE -> context.compare.type = v as String
            KEY_COMPARE_IGNORE_CASE -> context.compare.ignoreCase = v as Boolean
            KEY_COMPARE_DISORDER -> context.compare.disorder = v as Boolean
            KEY_COMPARE_HASH -> context.compare.hash = v as Boolean

            KEY_TESTCASE_OUT_SUFFIX -> context.case.outSuffix = v as String
            KEY_OUTPUT_MODE -> context.case.outMode = v as String
            KEY_FILLING -> context.reporter.filling = dataParser.parseFilling(k, v as String)
            KEY_TEXT_REPORT_WIDTH -> context.reporter.width = v as Int
            KEY_LIMIT_CASE_COUNT_MAX -> context.checking.limit.caseMaxCount = v as Int
            KEY_LIMIT_CASE_DEPTH_MAX -> context.checking.limit.caseMaxDepth = v as Int
            KEY_LIMIT_CASE_NAME_PATTERN -> context.checking.limit.caseNamePattern = Regex(v as String)
            KEY_LIMIT_CASE_SIZE_MAX -> context.checking.limit.caseMaxSize = dataParser.parseSize(k, v as String)

            KEY_CHECK_SQL -> context.jdbc.checkingSQL = v as String
            KEY_CONN_AUTOCOMMIT -> context.jdbc.autocommit = v as Boolean

            KEY_ZSQL_PATH -> context.zsql = v as String
            KEY_GSQL_PATH -> context.gsql = v as String
            KEY_CASE_TIMEOUT -> context.case.timeout = v as Long

            else -> throw SettingParseError("Parsing configure file: ${settingFile.absolutePath} failed: get unknown key $k")
        }
    }


}
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
 
package com.huawei.gauss.yat.convert

import com.huawei.gauss.yat.setting.SettingParseError
import com.huawei.gauss.yat.sql.Result


abstract class ResultConvert(protected val target: Result) {
    abstract fun convert(): String

    companion object {
        fun makeResultConvert(mode: String, result: Result): ResultConvert {
            return when (mode) {
                "pretty" -> PrettyResultConvert(result)
                "simple" -> SimpleResultConvert(result)
                else -> throw SettingParseError("found unknown output mode $mode")
            }
        }
    }
}
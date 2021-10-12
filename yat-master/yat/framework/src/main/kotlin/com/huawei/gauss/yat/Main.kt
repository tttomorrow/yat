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

package com.huawei.gauss.yat

import com.huawei.gauss.yat.common.WorkPool
import com.huawei.gauss.yat.common.YatExitNormal
import com.huawei.gauss.yat.common.YatRuntimeError
import com.huawei.gauss.yat.setting.SettingParseError
import kotlin.system.exitProcess


fun main(args: Array<String>) {
    try {
        YatApplication().run(args)
    } catch (e: Exception) {
        when (e) {
            is YatRuntimeError, is SettingParseError -> {
                println(e.message)
                exitProcess(1)
            }
            is YatExitNormal -> {/* do nothing */
            }
            else -> throw e
        }
    } finally {
        WorkPool.pool.shutdown()
    }
}
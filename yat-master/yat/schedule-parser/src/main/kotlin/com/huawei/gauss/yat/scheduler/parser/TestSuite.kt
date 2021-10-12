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

package com.huawei.gauss.yat.scheduler.parser

import java.util.*

class TestSuite(val name: String) : ArrayList<TestGroup>() {
    fun testCaseCount(): Int {
        var sum = 0
        this.forEach {
            sum += it.size
        }
        return sum
    }

    lateinit var run: TestRun

    var setup: TestGroup? = null
        set(value) {
            value?.forEach {
                it.setSetup()
            }
            field = value
        }
    var cleanup: TestGroup? = null
        set(value) {
            value?.forEach {
                it.setCleanup()
            }
            field = value
        }
}

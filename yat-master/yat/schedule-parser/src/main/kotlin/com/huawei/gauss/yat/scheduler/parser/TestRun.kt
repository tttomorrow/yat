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

class TestRun(val name: String, val suite: TestSuite) {
    init {
        suite.run = this
    }

    enum class ParallelLevel {
        GROUP,
        CASE,
        STATEMENT
    }

    enum class TestType {
        SUITE,
        RANDOM_CONCURRENT
    }

    val macros = mutableMapOf<String, String>()

    val intervals = mutableListOf<TestInterval>()
    val daemons = mutableListOf<TestDaemon>()

    var type = TestType.SUITE
    var level = ParallelLevel.GROUP
    var randomSleep = IntArray(1) { 0 }
    var eachRunCount = 0
}
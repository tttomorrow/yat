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


class TestGroup(val suite: TestSuite) : Iterable<TestCase> {

    private val testCases = mutableListOf<TestCase>()
    val size: Int
        get() {
            return testCases.size
        }


    override fun iterator(): Iterator<TestCase> {
        return testCases.iterator()
    }

    fun addTestCase(case: String, properties: Map<String, String>) {
        val testCase = TestCase(this, case)

        properties.forEach { (k, v) ->
            when (k) {
                "valid" -> testCase.properties.valid = getBoolean(k, v)
                "diff" -> testCase.properties.diff = getBoolean(k, v)
                "timeout" -> testCase.properties.timeout = getLong(k, v)
            }
        }

        testCases.add(testCase)
    }

    fun addTestCase(case: String) {
        addTestCase(case, mapOf())
    }

    private fun getBoolean(key: String, value: String): Boolean {
        return when (value) {
            "true" -> true
            "false" -> false
            else -> throw ScheduleSyntaxError("case properties $key expect true/false, but found $value")
        }
    }

    private fun getLong(key: String, value: String): Long {
        try {
            return value.toLong()
        } catch (e: NumberFormatException) {
            throw ScheduleSyntaxError("case properties $key expect number value, but found $value")
        }
    }
}

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
 
package com.huawei.gauss.yat.checker

import com.huawei.gauss.yat.common.TestCaseSearcher
import com.huawei.gauss.yat.scheduler.parser.TestSuite
import java.nio.file.Paths

class TestSuiteChecker(
        private val testSuite: TestSuite,
        private val maxCaseSize: Int,
        private val maxDepth: Int,
        private val casePattern: Regex) : Checker {

    override fun check(): List<String> {
        val errors = mutableListOf<String>()

        errors.addAll(checkSuite(testSuite))

        return errors
    }

    private fun checkSuite(testSuite: TestSuite): List<String> {
        val errors = mutableListOf<String>()
        testSuite.forEach { suite ->
            suite.forEach {
                val path = Paths.get(it.name)

                if (path.nameCount > maxDepth) {
                    errors.add("Test case ${it.name}'s depth should not exceed $maxDepth")
                }

                if (!it.meta.file.exists()) {
                    errors.add("Test case file ${it.meta.file} is not exists")
                } else if (it.meta.file.length() > maxCaseSize) {
                    errors.add("Test case file ${it.meta.file}'s size should not exceed $maxCaseSize")
                }
                path.forEach { p ->
                    if (!casePattern.matches(p.toString())) {
                        errors.add("Test case ${it.name} is illegal, require pattern ${casePattern.pattern}")
                    }
                }
            }
        }
        return errors
    }


}

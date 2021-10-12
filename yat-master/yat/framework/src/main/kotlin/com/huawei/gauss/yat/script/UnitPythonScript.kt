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

package com.huawei.gauss.yat.script

import com.huawei.gauss.yat.common.commander.ProcessCommander
import java.io.File
import java.io.IOException

class UnitPythonScript(
        private val output: File,
        private val testSuiteDir: String,
        private val libDir: String,
        private val env: Map<String, String> = mapOf()) : FileOutputScript() {

    private val commander = ProcessCommander()

    fun execute(testName: String): Boolean {
        makeParentPathExists(output)

        return try {
            0 == commander.sfexec("python3", "-m", "yat.runner",
                    "--test-suite", testSuiteDir,
                    "--test-case", testName,
                    "--library", libDir,
                    output = output, env = env)
        } catch (e: IOException) {
            output.writeText(e.message!!)
            false
        }
    }
}
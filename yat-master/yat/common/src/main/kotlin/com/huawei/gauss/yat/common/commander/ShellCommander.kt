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

package com.huawei.gauss.yat.common.commander

import java.io.File

class ShellCommander {
    private val commander = ProcessCommander()

    fun iiexec(script: String, env: Map<String, String>? = null): Int {
        return commander.exec("bash", "-c", script, env = env)
    }

    fun sfexec(cmd: String, output: File? = null, env: Map<String, String>? = null): Int {
        return if (output == null) {
            commander.exec("bash", "-c", cmd, env = env)
        } else {
            commander.sfexec("bash", "-c", cmd, output = output, env = env)
        }
    }

    fun ffexec(scriptFile: File, output: File? = null, env: Map<String, String>? = null): Int {
        return if (output == null) {
            commander.exec("bash", scriptFile.absolutePath, env = env)
        } else {
            commander.sfexec("bash", scriptFile.absolutePath, output = output, env = env)
        }
    }

    fun exec(script: String, env: Map<String, String>? = null): Int {
        return commander.exec("bash", "-c", script, env = env)
    }

    fun exec(scriptFile: File, env: Map<String, String>? = null): Int {
        return commander.exec("bash", "-f", scriptFile.absolutePath, env = env)
    }

    fun fsexec(scriptFile: File, env: Map<String, String>? = null): CommandResult {
        return commander.fsexec("bash", scriptFile.absolutePath, env = env)
    }

    fun ssexec(cmd: String, env: Map<String, String>? = null): CommandResult {
        return commander.ssexec("bash", "-c", cmd, env = env)
    }
}

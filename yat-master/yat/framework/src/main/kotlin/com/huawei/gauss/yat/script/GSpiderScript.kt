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

import com.huawei.gauss.yat.common.commander.ShellCommander
import java.io.File
import java.io.IOException


class GSpiderScript(
        private val type: String,
        private val host: String,
        private val port: Int,
        private val user: String,
        private val password: String,
        private val output: File,
        private val env: Map<String, String>) : FileOutputScript() {

    private val commander = ShellCommander()

    fun execute(script: File): Boolean {
        if (type.isEmpty()) {
            output.writeText("not support db type $type found")
            return false
        }

        val cmd = "gspider crawl -g ${script.absolutePath} " +
                "-o db:${type}:${user}/${password}@${host}:${port}?mode=cbo"
        try {
            if (0 != commander.sfexec(cmd, output, env)) {
                return false
            }
        } catch (e: IOException) {
            output.writeText("${e.message}")
            return false
        }
        return true
    }
}
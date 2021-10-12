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

import java.io.File
import java.nio.file.Path
import java.nio.file.Paths


class ZSqlScript(builder: Builder) : BaseCmdSqlScript(builder) {
    override fun getCmdPathFromMacro(): String? {
        return env["ZSQL_PATH"]
    }

    override fun cmdSetting(cmd: MutableList<String>) {
        if (echo) {
            cmd.add("-a")
        }
    }

    override fun makeMirrorFile(relative: Path): File {
        return Paths.get(tempDir, "zsql", relative.subpath(1, relative.nameCount).toString()).toFile()
    }

    override fun makeCommander(): CmdCommander {
        return CmdCommander("zsql", "$user/$password@$host:$port")
    }

    override fun buildCmdExecFromFile(cmd: MutableList<String>, sqlFile: File) {
        cmd.addAll(arrayOf("-f", sqlFile.absolutePath))
    }

    override fun buildCmdExecFromParams(cmd: MutableList<String>, sql: String) {
        cmd.addAll(arrayOf("-c", sql))
    }
}
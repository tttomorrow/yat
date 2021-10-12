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

package com.huawei.gauss.yat.setting

import com.huawei.gauss.yat.common.YatRuntimeError
import com.huawei.gauss.yat.vfs.VFS
import java.io.File
import java.nio.file.Paths

class YatOutputDir(root: String?) {
    private val vfs: VFS
    private fun init() {
        mkdir(tempDir, "temp")
        mkdir(logDir, "log")
        mkdir(resultDir, "result")
    }

    private fun mkdir(path: File, mark: String) {
        if (!path.exists() && !path.mkdirs()) {
            throw YatRuntimeError("make $mark directory failed")
        }
    }

    fun newFile(path: String?): File {
        return vfs.newFile(path).toFile()
    }

    val outputDir: File
        get() = vfs.root()

    val tempDir: File
        get() = vfs.newFile(CONST_TEMP_DIR).toFile()

    val logDir: File
        get() = vfs.newFile(Paths.get(CONST_LOG_DIR)).toFile()

    val resultDir: File
        get() = vfs.newFile(Paths.get(CONST_RESULT_DIR)).toFile()

    val yatTextLog: File
        get() = vfs.newFile(Paths.get(CONST_LOG_DIR, CONST_LOG_TEXT_NAME)).toFile()

    val yatJsonLog: File
        get() = vfs.newFile(Paths.get(CONST_LOG_DIR, CONST_LOG_JSON_NAME)).toFile()

    val yatRedoLog: File
        get() = vfs.newFile(Paths.get(CONST_LOG_DIR, CONST_LOG_REDO_NAME)).toFile()

    val lockFile: File
        get() = vfs.newFile(Paths.get(CONST_LOG_DIR, CONST_LOCK_FILE)).toFile()

    fun getCaseOutput(name: String, subSuite: String?, ext: String): File {
        return vfs.newFile(Paths.get(CONST_RESULT_DIR, subSuite, name + ext)).toFile()
    }

    val contextLog: File
        get() = vfs.newFile(Paths.get(CONST_LOG_DIR, CONST_CONTEXT_NAME)).toFile()

    init {
        vfs = VFS(root)
        init()
    }
}
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

package com.huawei.gauss.yat.vfs

import java.io.File
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths

class VFS {
    private var rootDir: File

    constructor(rootDir: File) {
        this.rootDir = rootDir
    }

    constructor(rootDir: String?) {
        this.rootDir = File(rootDir)
    }

    fun getRealFile(path: String?): File {
        return Paths.get(rootDir.toString(), path).toFile()
    }

    fun newFile(path: String?): VFile {
        return VFile(this, path!!)
    }

    fun newFile(path: Path?): VFile {
        return VFile(this, path!!)
    }

    fun root(): File {
        return rootDir
    }

    fun exists(path: String?): Boolean {
        return getRealFile(path).exists()
    }

    fun isDirectory(path: String?): Boolean {
        return Files.isDirectory(getRealFile(path).toPath())
    }
}
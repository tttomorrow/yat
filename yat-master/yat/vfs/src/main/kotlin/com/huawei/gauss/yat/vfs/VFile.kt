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

import java.io.BufferedInputStream
import java.io.BufferedOutputStream
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.io.InputStream
import java.io.OutputStream
import java.nio.file.Path

class VFile internal constructor(private val vfs: VFS, private val path: String) {
    internal constructor(vfs: VFS, path: Path) : this(vfs, path.toString())

    fun toFile(): File {
        return vfs.getRealFile(path)
    }

    private val outputStream: OutputStream
        get() = FileOutputStream(toFile())

    private val inputStream: InputStream
        get() = FileInputStream(toFile())

    private val bufferedOutputStream: OutputStream
        get() = BufferedOutputStream(outputStream)

    private val bufferedInputStream: InputStream
        get() = BufferedInputStream(inputStream)

    fun exists(): Boolean {
        return toFile().exists()
    }
}
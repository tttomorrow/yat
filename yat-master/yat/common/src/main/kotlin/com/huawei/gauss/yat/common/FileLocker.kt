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

package com.huawei.gauss.yat.common

import java.io.Closeable
import java.io.File
import java.io.FileOutputStream
import java.nio.channels.FileLock

class FileLocker(private val filename: File) : Closeable {
    private var lock: FileLock? = null
    private var stream: FileOutputStream? = null

    fun lock(): Boolean {
        stream = FileOutputStream(filename)
        lock = stream!!.channel.tryLock()
        return lock != null
    }

    fun unlock() {
        lock?.release()
        stream?.close()
    }

    override fun close() {
        unlock()
    }
}
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

import java.io.StringWriter
import java.io.Writer

abstract class MemoryOutputScript {

    protected var writer: Writer = StringWriter()
    protected var originWriter: Writer = StringWriter()

    fun setOutput(writer: Writer) {
        this.writer = writer
    }

    fun output(): String {
        return writer.toString()
    }

    fun setOriginOutput(writer: Writer) {
        this.originWriter = writer
    }

    fun originOutput(): String {
        return originWriter.toString()
    }

    protected fun writeAll(string: String) {
        writer.write(string)
        originWriter.write(string)
    }

    protected fun writelnAll(string: String) {
        writeAll("$string\n")
    }
}
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

package com.huawei.gauss.yat.scheduler.parser

import com.huawei.gauss.yat.common.TestCaseSearcher
import java.io.File

class CaseMeta private constructor(
        val name: String, val file: File,
        val output: File, val expects: List<File>,
        val type: TestCaseSearcher.Type) {

    companion object {
        fun builder(): Builder {
            return Builder()
        }
    }

    class Builder {
        var name: String = ""
            private set
        var file: File = File("")
            private set
        var output: File = File("")
            private set
        var expects: List<File> = emptyList()
            private set
        var type: TestCaseSearcher.Type = TestCaseSearcher.Type.SQL
            private set

        fun name(name: String) = apply { this.name = name }
        fun file(file: File) = apply { this.file = file }
        fun output(output: File) = apply { this.output = output }
        fun expects(expects: List<File>) = apply { this.expects = expects }
        fun type(type: TestCaseSearcher.Type) = apply { this.type = type }
        fun build(): CaseMeta {
            return CaseMeta(name, file, output, expects, type)
        }
    }
}
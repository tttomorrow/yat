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

import com.huawei.gauss.yat.common.TestCaseSearcher
import com.huawei.gauss.yat.common.YatRuntimeError
import com.huawei.gauss.yat.scheduler.parser.CaseMeta
import com.huawei.gauss.yat.vfs.VFS
import java.io.File
import java.nio.file.Paths

class YatWorkDir(root: File, private var expect: String = "") {
    private val vfs: VFS = VFS(root.absoluteFile)
    val output: YatOutputDir

    constructor(root: String) : this(File(root))

    fun setExpect(expect: String) {
        this.expect = expect
    }

    private fun check(): Boolean {
        var res = isDirectory(CONST_CONFIG_DIR)
        res = isDirectory(CONST_TESTCASE_DIR) && res
        res = isDirectory(CONST_SCHEDULE_DIR) && res
        return res
    }

    private fun isDirectory(path: String): Boolean {
        if (!vfs.isDirectory(path)) {
            throw YatRuntimeError("directory " + path + " is not exists at suite: " + vfs.root().toString())
        }
        return true
    }

    val confDir: File
        get() = vfs.newFile(CONST_CONFIG_DIR).toFile()

    val testCaseDir: File
        get() = vfs.newFile(CONST_TESTCASE_DIR).toFile()

    val libraryDir: File
        get() = vfs.newFile(CONST_LIBRARY_DIR).toFile()

    val expectDir: File
        get() = vfs.newFile(Paths.get(CONST_EXPECT_DIR, expect)).toFile()

    val scheduleDir: File
        get() = vfs.newFile(CONST_SCHEDULE_DIR).toFile()

    val workDir: File
        get() = vfs.root()

    fun getCaseMeta(name: String, subSuite: String?, ext: String): CaseMeta {
        val searcher = TestCaseSearcher(testCaseDir, expectDir)
        val (case, type) = searcher.searchCase(name)
        val expects = searcher.searchExpect(name, subSuite!!, ext)
        return CaseMeta.builder()
                .name(name)
                .file(case)
                .type(type)
                .output(output.getCaseOutput(name, subSuite, ext))
                .expects(expects)
                .build()
    }

    init {
        if (!check()) {
            throw YatRuntimeError("given yat suite work space is illegal")
        }
        output = YatOutputDir(workDir.absolutePath)
    }
}
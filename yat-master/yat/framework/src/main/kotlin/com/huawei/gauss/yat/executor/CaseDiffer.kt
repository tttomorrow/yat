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

package com.huawei.gauss.yat.executor

import com.huawei.gauss.yat.diff.JDiffer
import com.huawei.gauss.yat.scheduler.parser.TestCase
import com.huawei.gauss.yat.setting.YatContext
import java.io.File
import java.nio.file.Path
import java.nio.file.Paths


class CaseDiffer(private val context: YatContext, private val case: TestCase) {
    companion object {
        private fun getDiffPath(expect: Path, output: Path): Path {
            return Paths.get(output.parent.toAbsolutePath().toString(), "${expect.getName(expect.nameCount - 1)}.diff")
        }
        private const val MAX_DIFF_SIZE = 1500;
    }

    fun diff(): Boolean {
        if (!case.meta.output.exists()) {
            return false
        }

        val target = case.meta.output.bufferedReader().readLines()

        if (target.size > MAX_DIFF_SIZE) {
            File(getDiffPath(case.meta.output.toPath(), case.meta.output.toPath()).toString()).writeText(
                "Warning: diff file line count is bigger than max line count ${MAX_DIFF_SIZE}, reject to diff")
            return false
        }

        for (it in case.meta.expects) {
            if (it.exists()) {
                val differ = JDiffer.builder()
                        .leftLines(it.bufferedReader().readLines())
                        .rightLines(target)
                        .leftPath(it.absolutePath)
                        .rightPath(case.meta.output.absolutePath)
                        .macro(context.macro.all())
                        .build()
                if (differ.diff()) {
                    return true
                } else {
                    File(getDiffPath(it.toPath(), case.meta.output.toPath()).toString()).writeText(differ.diffToReadable())
                }
            }
        }

        return false
    }
}
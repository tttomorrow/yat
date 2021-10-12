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
 
package com.huawei.gauss.yat.diff

import com.github.difflib.DiffUtils
import com.github.difflib.patch.DeleteDelta
import com.github.difflib.patch.InsertDelta
import java.util.*
import java.util.function.BiPredicate

data class DiffRow<T>(val tag: Tag, val oldLine: T, val newLine: T) {
    enum class Tag {
        INSERT, DELETE, CHANGE, EQUAL
    }
}

class DiffRowMaker {
    fun generateDiffRows(original: List<LineWithNumber>, newline: List<LineWithNumber>, equalizer: BiPredicate<LineWithNumber, LineWithNumber>?): List<DiffRow<LineWithNumber>> {
        val patch = DiffUtils.diff(original, newline, equalizer)
        val diffRows: MutableList<DiffRow<LineWithNumber>> = ArrayList()
        var origEndPos = 0
        var revEndPos = 0
        val deltaList = patch.deltas
        for (delta in deltaList) {
            val orig = delta.source
            val rev = delta.target
            val newIter = newline.subList(revEndPos, rev.position).iterator()
            for (line in original.subList(origEndPos, orig.position)) {
                diffRows.add(DiffRow(DiffRow.Tag.EQUAL, line, newIter.next()))
            }
            // Inserted DiffRow
            if (delta is InsertDelta<*>) {
                origEndPos = orig.last() + 1
                revEndPos = rev.last() + 1
                for (line in rev.lines) {
                    diffRows.add(DiffRow(DiffRow.Tag.INSERT, LineWithNumber(), line))
                }
                continue
            }
            // Deleted DiffRow
            if (delta is DeleteDelta<*>) {
                origEndPos = orig.last() + 1
                revEndPos = rev.last() + 1
                for (line in orig.lines) {
                    diffRows.add(DiffRow(DiffRow.Tag.DELETE, line, LineWithNumber()))
                }
                continue
            }
            for (j in 0 until Math.max(orig.size(), rev.size())) {
                diffRows.add(DiffRow(DiffRow.Tag.CHANGE,
                        if (j < orig.lines.size) orig.lines[j] else LineWithNumber(),
                        if (j < rev.lines.size) rev.lines[j] else LineWithNumber()))
            }
            origEndPos = orig.last() + 1
            revEndPos = rev.last() + 1
        }
        val revIter = newline.subList(revEndPos, newline.size).iterator()
        // Copy the final matching chunk if any.
        for (line in original.subList(origEndPos, original.size)) {
            diffRows.add(DiffRow(DiffRow.Tag.EQUAL, line, revIter.next()))
        }
        return diffRows
    }
}
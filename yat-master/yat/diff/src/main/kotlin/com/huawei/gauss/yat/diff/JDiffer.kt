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
import com.huawei.gauss.yat.common.MacroReplacer
import java.util.*
import java.util.function.BiPredicate
import java.util.regex.PatternSyntaxException
import kotlin.collections.ArrayList

data class LineWithNumber(val line: String, val num: Int) {
    fun trim(): LineWithNumber {
        return LineWithNumber(line.trim(), num)
    }

    constructor() : this("", -1)

    override fun toString(): String {
        return line
    }

    fun isNotEmpty(): Boolean {
        return line.isNotEmpty()
    }
}

/**
 * Diff with pure java code
 * Based on java-diff-utils
 */
class JDiffer private constructor(builder: Builder) {
    companion object {
        fun builder() = Builder()
    }

    private val leftLines: List<LineWithNumber>
    private val rightLines: List<LineWithNumber>
    private val leftPath: String = builder.leftPath
    private val rightPath: String = builder.rightPath
    private val count: Int = builder.count
    private val ignoreWhiteSpace: Boolean = builder.ignoreWhiteSpace
    private val ignoreBlankLine: Boolean = builder.ignoreBlankLine
    private val spaceRegex = Regex("^[\\s\\t]*$")
    private val leftHandler = DifferHandler<LineWithNumber>()
    private val rightHandler = DifferHandler<LineWithNumber>()
    private val equalizer: BiPredicate<LineWithNumber, LineWithNumber>

    init {
        if (ignoreBlankLine) {
            leftHandler.registerFilter { line ->
                !spaceRegex.matches(line.line)
            }
            rightHandler.registerFilter { line ->
                !spaceRegex.matches(line.line)
            }
        }

        leftLines = leftHandler.handle(builder.leftLines)
        rightLines = rightHandler.handle(builder.rightLines)

        equalizer = BiPredicate { a, b ->
            var realA: LineWithNumber = a
            var realB: LineWithNumber = b

            if (ignoreWhiteSpace) {
                realA = a.trim()
                realB = b.trim()
            }

            if (builder.macro.isNotEmpty()) {
                realA = LineWithNumber(MacroReplacer(realA.line).replace(builder.macro), realA.num)
                realB = LineWithNumber(MacroReplacer(realB.line).replace(builder.macro), realB.num)
            }

            if (realA.line == realB.line) {
                true
            } else {
                if (a.line.startsWith("?")) {
                    try {
                        Regex(a.line.substring(1)).matches(realB.line)
                    } catch (e: PatternSyntaxException) {
                        false
                    }
                } else {
                    false
                }
            }
        }
    }

    class Builder {
        var leftLines = emptyList<LineWithNumber>()
            private set
        var rightLines = emptyList<LineWithNumber>()
            private set
        var leftPath = "old"
            private set
        var rightPath = "new"
            private set
        var count = 3
            private set
        var ignoreWhiteSpace = true
            private set
        var ignoreBlankLine = true
            private set
        var macro = mapOf<String, String>()
            private set

        fun leftLines(leftLines: List<String>) = apply {
            val res = mutableListOf<LineWithNumber>()
            for ((num, line) in leftLines.withIndex()) {
                res.add(LineWithNumber(line, num + 1))
            }
            this.leftLines = res
        }

        fun rightLines(rightLines: List<String>) = apply {
            val res = mutableListOf<LineWithNumber>()
            for ((num, line) in rightLines.withIndex()) {
                res.add(LineWithNumber(line, num + 1))
            }
            this.rightLines = res
        }

        fun leftPath(leftPath: String) = apply { this.leftPath = leftPath }
        fun rightPath(rightPath: String) = apply { this.rightPath = rightPath }
        fun count(count: Int) = apply { this.count = count }
        fun ignoreWitheSpace(ignoreWhiteSpace: Boolean) = apply { this.ignoreWhiteSpace = ignoreWhiteSpace }
        fun ignoreBlankLine(ignoreBlankLine: Boolean) = apply { this.ignoreBlankLine = ignoreBlankLine }
        fun macro(macro: Map<String, String>) = apply { this.macro = macro }
        fun build() = JDiffer(this)
    }

    /**
     * diff with line regex compare
     */
    fun diff(): Boolean {
        return DiffUtils.diff(leftLines, rightLines, equalizer).deltas.size == 0
    }

    fun diffToReadable(): String {
        val rows = DiffRowMaker().generateDiffRows(leftLines, rightLines, equalizer);
        return DiffResult(rows, leftPath, rightPath, count).toString()
    }

    /**
     * fixed capacity queue, which when queue is full, head one will be drop
     */
    private class FixedQueue<T>(private val capacity: Int = 3) {
        private val buffer = LinkedList<T>()

        fun offer(item: T) {
            buffer.offer(item)
            if (buffer.size > capacity) {
                buffer.poll()
            }
        }

        fun clear(): List<T> {
            val iter = buffer.iterator()
            val res = List(buffer.size) { iter.next() }
            buffer.clear()
            return res
        }

        fun size(): Int {
            return buffer.size
        }
    }

    private class DiffResult(
            private val rows: List<DiffRow<LineWithNumber>>,
            private val lpath: String = "old",
            private val rpath: String = "new",
            private val count: Int = 3) {

        val parts = LinkedList<DiffPart>()
        val rowsIter = rows.iterator()

        init {
            while (rowsIter.hasNext()) {
                val part = parsePart()
                if (!part.isEmpty()) {
                    parts.add(part)
                }
            }
        }

        private fun parsePart(): DiffPart {
            val head = parseHead()
            if (head.isEmpty()) {
                return DiffPart()
            }

            val tail = parseTail()

            val res = DiffPart()
            res.diffRows.addAll(head)
            res.diffRows.addAll(tail)

            return res
        }

        private fun parseHead(): List<DiffRow<LineWithNumber>> {
            val equalBuffer = FixedQueue<DiffRow<LineWithNumber>>(count)

            while (rowsIter.hasNext()) {
                val row = rowsIter.next()

                when (row.tag) {
                    DiffRow.Tag.EQUAL -> {
                        equalBuffer.offer(row)
                    }
                    else -> {
                        val res = mutableListOf<DiffRow<LineWithNumber>>()
                        res.addAll(equalBuffer.clear())
                        res.add(row)
                        return res
                    }
                }
            }
            return arrayListOf()
        }

        private fun parseTail(): List<DiffRow<LineWithNumber>> {
            val res = mutableListOf<DiffRow<LineWithNumber>>()
            var equalCount = 0
            while (rowsIter.hasNext()) {
                val row = rowsIter.next()

                when (row.tag) {
                    DiffRow.Tag.EQUAL -> {
                        equalCount++
                        res.add(row)
                        if (equalCount == count) {
                            return res
                        }
                    }
                    else -> res.add(row)
                }
            }

            return res
        }

        override fun toString(): String {
            val res = ArrayList<String>()

            res.add("*** $lpath")
            res.add("--- $rpath")

            parts.forEach {
                res.add(it.toString())
            }

            return res.joinToString("\n")
        }
    }

    private class DiffPart {
        val diffRows = LinkedList<DiffRow<LineWithNumber>>()

        override fun toString(): String {
            if (diffRows.isEmpty()) {
                return ""
            }

            val res = ArrayList<String>()
            res.add("***************")

            res.add("*** ${diffRows.first.oldLine.num},${diffRows.last.oldLine.num} ***")

            for (row in diffRows) {
                val old = row.oldLine

                when (row.tag) {
                    DiffRow.Tag.EQUAL -> {
                        res.add("  $old")
                    }
                    DiffRow.Tag.CHANGE -> {
                        if (old.isNotEmpty()) {
                            res.add("! $old")
                        }
                    }
                    DiffRow.Tag.DELETE -> {
                        res.add("- $old")
                    }
                    else -> {
                        /* do nothing */
                    }
                }
            }

            res.add("--- ${diffRows.first.newLine.num},${diffRows.last.newLine.num} ---")
            for (row in diffRows) {
                val new = row.newLine

                when (row.tag) {
                    DiffRow.Tag.EQUAL -> {
                        res.add("  $new")
                    }
                    DiffRow.Tag.CHANGE -> {
                        if (new.isNotEmpty()) {
                            res.add("! $new")
                        }
                    }
                    DiffRow.Tag.INSERT -> {
                        res.add("+ $new")
                    }
                    else -> {
                        /* do nothing */
                    }
                }
            }

            return res.joinToString("\n")
        }

        fun isEmpty(): Boolean {
            return diffRows.isEmpty()
        }
    }
}

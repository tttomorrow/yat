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

package com.huawei.gauss.yat.case.properties.parser

import com.huawei.gauss.yat.common.ArrayCycleQueue
import com.huawei.gauss.yat.common.lex.PeekReader
import java.io.Reader
import java.lang.StringBuilder
import java.util.*
import java.util.stream.Collectors
import kotlin.math.max


class CommentReader(reader: Reader, lineMark: List<String>, multiLineMark: List<Pair<String, String>>) {
    companion object {
        private const val EOF = -1
    }
    private val reader = PeekReader(reader)
    private val buffer = StringBuilder()
    private val lineMark: List<CharArray> = lineMark.stream().map { it.toCharArray() }.collect(Collectors.toList())
    private val multiLineMark: List<Pair<CharArray, CharArray>> =
            multiLineMark.stream().map { Pair(it.first.toCharArray(), it.second.toCharArray()) }.collect(Collectors.toList())
    private val maxSize = getMaxSize()
    private val queue = ArrayCycleQueue<Char>(maxSize)

    fun parse(): String {
        buffer.clear()
        while (true) {
            val ch = reader.peek()
            if (reader.peek() == EOF) {
                break
            }

            if (queue.isFull()) {
                queue.poll()
            }
            enqueue()
            var found = false
            for (line in lineMark) {
                if (queueStartWith(line)) {
                    val prefix = if (queue.size() > line.size) {
                        queue.read(line.size).toCharArray()
                    } else {
                        CharArray(0)
                    }
                    appendUntil(CharArray(1) {'\n'}, prefix)
                    queue.clear()
                    found = true
                    break
                }
            }
            if (found) {
                continue
            }

            for (multi in multiLineMark) {
                if (queueStartWith(multi.first)) {
                    val prefix = if (queue.size() > multi.first.size) {
                        queue.read(multi.first.size).toCharArray()
                    } else {
                        CharArray(0)
                    }
                    appendUntil(multi.second, prefix)
                    queue.clear()
                    break
                }
            }
        }
        return buffer.toString()
    }

    private fun appendUntil(until: CharArray, prefix: CharArray = CharArray(0)) {
        val queue = ArrayDeque<Char>()
        val prefixQueue = ArrayDeque<Char>(prefix.size)
        prefix.forEach {
            prefixQueue.add(it)
        }

        val localRead = {
            if (prefixQueue.size > 0) {
                prefixQueue.poll()
            } else {
                reader.next().toChar()
            }
        }

        (1..until.size).forEach { _ ->
            queue.add(localRead())
        }

        while (true) {
            var equal = true
            queue.toCharArray().forEachIndexed { idx, it ->
                if (it != until[idx]) {
                    equal = false
                }
            }

            if (equal) {
                buffer.append('\n')
                break
            }
            val value = queue.poll()
            if (value == EOF.toChar()) {
                throw CommentReadError("not complete multi-comment, expect multi-comment end, found EOF")
            }
            buffer.append(value)
            queue.add(localRead())
        }
    }

    private fun enqueue() {
        queue.add(reader.next().toChar())
    }

    private fun queueStartWith(cmp: CharArray): Boolean {
        if (queue.size() < cmp.size) {
            return false
        }

        var idx = 0
        for (ch in queue) {
            if (idx < cmp.size && ch != cmp[idx++]) {
                return false
            }
        }

        return true
    }

    private fun getMaxSize(): Int {
        val lineMaxSize = lineMark.stream().max { a, b -> a.size - b.size }.get().size
        val multiLineMax = multiLineMark.stream().max { a, b ->
            max(a.first.size, a.second.size) - max(b.first.size, b.second.size)
        }.get()

        return max(lineMaxSize, max(multiLineMax.first.size, multiLineMax.second.size))
    }
}
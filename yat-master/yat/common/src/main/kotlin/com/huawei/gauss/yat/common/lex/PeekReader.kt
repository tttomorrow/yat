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

package com.huawei.gauss.yat.common.lex

import com.huawei.gauss.yat.common.ArrayCycleQueue
import java.io.Reader

class PeekReader constructor(private val reader: Reader, peekMaxSize: Int = PEEK_DEFAULT_SIZE) {
    private val caches: ArrayCycleQueue<Int> = ArrayCycleQueue(peekMaxSize)

    private var newLine = false
    private var col = 0
    private var line = 1

    fun peek(index: Int = 0): Int {
        val size = caches.size()
        if (size <= index) {
            val count = index - size + 1
            for (i in 0 until count) {
                caches.add(reader.read())
            }
        }
        return caches.peek(index)!!
    }

    fun skipBlank(): Int {
        var ch = peek()
        while (ch in blankSet) {
            next()
            ch = peek()
        }
        return ch
    }

    operator fun next(): Int {
        val ch: Int = if (caches.isEmpty) {
            reader.read()
        } else {
            caches.poll()!!
        }
        if (newLine) {
            col = 0
            line++
            newLine = false
        }
        col++
        if (ch == LF) {
            newLine = true
        }
        return ch
    }

    fun position(): Position {
        return Position(line, col)
    }

    companion object {
        private const val PEEK_DEFAULT_SIZE = 4
        private const val LF = '\n'.code
        private const val BLANK = ' '.code
        private const val CR = '\r'.code
        private const val TAB = '\t'.code
        private val blankSet = setOf(LF, BLANK, CR, TAB)
    }

}
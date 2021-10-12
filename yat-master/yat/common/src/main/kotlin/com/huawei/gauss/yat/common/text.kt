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


object ColorText {
    fun black(str: String, bright: Boolean = true): String {
        return colorText(30, str, bright)
    }

    fun red(str: String, bright: Boolean = true): String {
        return colorText(31, str, bright)
    }

    fun green(str: String, bright: Boolean = true): String {
        return colorText(32, str, bright)
    }

    fun yellow(str: String, bright: Boolean = true): String {
        return colorText(33, str, bright)
    }

    fun blue(str: String, bright: Boolean = true): String {
        return colorText(34, str, bright)
    }

    fun purple(str: String, bright: Boolean = true): String {
        return colorText(35, str, bright)
    }

    fun cyan(str: String, bright: Boolean = true): String {
        return colorText(36, str, bright)
    }

    fun white(str: String, bright: Boolean = true): String {
        return colorText(37, str, bright)
    }

    private fun colorText(color: Int, str: String, bright: Boolean = true): String {
        val colorMark = "[$color${if (bright) ";1m" else "m"}"
        return "${27.toChar()}$colorMark$str${27.toChar()}[0m"
    }
}

class FixedWidthText(private val width: Int, private val blank: Char = '.') {
    private val buffer = CharArray(width) { blank }

    private fun check(start: Int, end: Int) {
        if (start > end || start < 0 || end >= width) {
            throw IndexOutOfBoundsException()
        }
    }

    private fun put(str: String, strStart: Int, bufStart: Int, end: Int) {
        var bufPos = bufStart
        str.forEachIndexed { index, c ->
            if (index >= strStart && bufPos <= end) {
                buffer[bufPos++] = c
            }
        }
    }

    fun left(str: String, start: Int = 0, end: Int = width - 1): FixedWidthText {
        check(start, end)

        put(str, 0, start, end)
        return this
    }

    fun right(str: String, start: Int = 0, end: Int = width - 1): FixedWidthText {
        check(start, end)
        val bufLen = end - start + 1
        val strStart: Int
        val bufStart: Int

        if (bufLen >= str.length) {
            strStart = 0
            bufStart = start + bufLen - str.length
        } else {
            strStart = str.length - bufLen
            bufStart = start
        }

        put(str, strStart, bufStart, end)
        return this
    }

    fun center(str: String, start: Int = 0, end: Int = width - 1): FixedWidthText {
        check(start, end)
        val bufLen = end - start + 1
        val strStart: Int
        val bufStart: Int

        if (bufLen >= str.length) {
            strStart = 0
            bufStart = start + (bufLen - str.length) / 2
        } else {
            strStart = (str.length - bufLen) / 2
            bufStart = start
        }

        put(str, strStart, bufStart, end)

        return this
    }

    fun build(): String {
        return String(buffer)
    }
}

class ThumbPrinter(private val width: Int = 100) {
    private val buffer = StringBuffer(width)
    private var added = 0
    private var full = false

    private fun printOne(str: String): Boolean {
        if (full) return false

        if (added + str.length > width) {
            val writePos = width - added - 5
            buffer.append("${str.slice(IntRange(0, writePos))} ...")
            added += writePos
            full = true
            return false
        }

        buffer.append(str)
        added += str.length
        return true
    }

    fun printArray(list: List<String>) {
        for (v in list) {
            if (!printOne("$v ")) {
                break
            }
        }

        print(buffer.toString())
    }

    fun printArrayln(list: List<String>) {
        printArray(list)
        println()
    }
}
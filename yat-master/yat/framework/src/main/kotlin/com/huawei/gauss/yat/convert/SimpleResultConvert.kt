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

package com.huawei.gauss.yat.convert

import com.huawei.gauss.yat.sql.Result


class SimpleResultConvert(result: Result): ResultConvert(result) {
    override fun convert(): String {
        val sb = StringBuilder()
        val metaText = convertMeta()

        sb.append(metaText).append('\n')
        val maxLen = target.metaData.colMaxLength

        target.forEach {
            it.forEachIndexed { i, value ->
                if (i != 0) {
                    sb.append("   ")
                }
                val len = maxLen[i]
                sb.append(String.format("%-${len}s", value.toString()))
            }
            sb.append("\n")
        }

        if (target.isRowMax) {
            sb.append("\n......\n")
            sb.append("!!!Warning: The row number of Result Set is bigger than the max value(${Result.ROW_MAX_COUNT}), and the result set is truncated")
        }

        return sb.toString()
    }

    private fun convertMeta(): String {
        val meta = target.metaData
        val sb = StringBuilder()
        meta.forEachIndexed { i, it ->
            if (i != 0) {
                sb.append(" | ")
            }

            val len = meta.colMaxLength[i]
            sb.append(String.format("%-${len}s", it.name))
        }
        sb.append("\n")
        sb.append(makeSplitLine())

        return sb.toString()
    }

    private fun makeSplitLine(): String {
        var columnSum = 0
        target.metaData.forEachIndexed { i, _ ->
            columnSum += target.metaData.colMaxLength[i]
        }

        return String(CharArray(columnSum + (target.metaData.columnCount() - 1) * 3) {'-'})
    }
}
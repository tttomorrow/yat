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

package com.huawei.gauss.yat.sql

import java.sql.ResultSet
import java.util.*

class Result(resultSet: ResultSet) : Iterable<ResultRow> {
    companion object {
        val ROW_MAX_COUNT = 1000
    }
    var count: Long = 0
        private set
    val metaData: ResultMeta = ResultMeta(resultSet.metaData)
    private val rows = LinkedList<ResultRow>()
    var isRowMax = false
        private set

    init {
        val colCount = metaData.columnCount()
        val colMaxLen = metaData.colMaxLength

        while (resultSet.next()) {
            count++
            val row = ResultRow(resultSet)
            (0 until colCount).forEach {
                val rowLen = row.rowLengths[it]
                val rowMaxLen = colMaxLen[it]
                if (rowLen > rowMaxLen) {
                    colMaxLen[it] = rowLen
                }
            }
            rows.add(row)

            if (count > ROW_MAX_COUNT) {
                isRowMax = true
                break
            }
        }
    }

    override fun iterator(): Iterator<ResultRow> {
        return rows.iterator()
    }
}
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

class ResultRow(resultSet: ResultSet) : Iterable<ResultValue> {
    private val row: Array<ResultValue>
    val rowLengths: Array<Int>

    init {
        val meta = resultSet.metaData
        row = Array(meta.columnCount) {
            val index = it + 1
            ResultValue(resultSet.getObject(index), meta.getColumnType(index))
        }

        rowLengths = Array(meta.columnCount) {
            row[it].toString().length
        }
    }

    override fun iterator(): Iterator<ResultValue> {
        return row.iterator()
    }
}

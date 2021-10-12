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

import java.sql.ResultSetMetaData

class ResultMeta(meta: ResultSetMetaData) : Iterable<ColumnMeta> {
    val metaValue: List<ColumnMeta>
    val colMaxLength: Array<Int>

    init {
        val count = meta.columnCount
        val list = ArrayList<ColumnMeta>(count)
        colMaxLength = Array(count) { 0 }
        (1..count).forEach {
            val metaValue = ColumnMeta.fromMetaData(meta, it)
            colMaxLength[it - 1] = metaValue.name.length
            list.add(metaValue)
        }

        metaValue = list
    }

    override fun iterator(): Iterator<ColumnMeta> {
        return metaValue.iterator()
    }

    fun columnCount(): Int {
        return metaValue.size
    }
}
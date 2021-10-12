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

class ColumnMeta private constructor() {
    var name: String = ""
        private set
    var type: Int = -1
        private set
    var precision: Int = 0
        private set
    var scale: Int = 0
        private set

    companion object {
        fun fromMetaData(meta: ResultSetMetaData, index: Int): ColumnMeta {
            val colMeta = ColumnMeta()
            colMeta.name = meta.getColumnName(index)
            colMeta.type = meta.getColumnType(index)
            colMeta.precision = meta.getPrecision(index)
            colMeta.scale = meta.getScale(index)

            return colMeta
        }
    }
}
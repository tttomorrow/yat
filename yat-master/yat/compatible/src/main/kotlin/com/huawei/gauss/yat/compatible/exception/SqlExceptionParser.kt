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
 
package com.huawei.gauss.yat.compatible.exception

import java.sql.SQLException

interface SqlExceptionParser {
    fun parse(exception: SQLException): SqlExceptionContext

    companion object {
        fun parse(exception: SQLException): SqlExceptionContext {
            val typeName = exception.javaClass.canonicalName
            return when {
                typeName.startsWith("com.huawei.gauss.exception.") -> GaussSqlExceptionParser().parse(exception)
                typeName == "org.postgresql.util.PSQLException" -> OpenGaussSqlExceptionParser().parse(exception)
                else -> CommonSqlExceptionParser().parse(exception)
            }
        }
    }
}
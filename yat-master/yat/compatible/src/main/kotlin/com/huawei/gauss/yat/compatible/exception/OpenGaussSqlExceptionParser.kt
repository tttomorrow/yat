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


class OpenGaussSqlExceptionParser: SqlExceptionParser {
    companion object {
        private val messageRegex = Regex(".*org.postgresql.util.PSQLException: Error: (.*).*", RegexOption.DOT_MATCHES_ALL)
    }

    override fun parse(exception: SQLException): SqlExceptionContext {
        val matcher = messageRegex.matchEntire(exception.message!!)
        return if (matcher != null) {
            val msg = matcher.groupValues[1]
            return SqlExceptionContext(msg, "")
        } else {
            SqlExceptionContext(exception.message!!, "")
        }
    }
}
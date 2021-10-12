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

class GaussSqlExceptionParser : SqlExceptionParser {
    companion object {
        private val messageRegex = Regex(".*errorCode *= *(GS-[0-9]{5}).*errMsg *= *(.*),ioClient:@.*", RegexOption.DOT_MATCHES_ALL)
        private val messageRegexNetError = Regex(".*errorCode *= *(GS-[0-9]{5}).*reason *= *'(.*)', *serverIP=(.*),.*", RegexOption.DOT_MATCHES_ALL)
    }

    override fun parse(exception: SQLException): SqlExceptionContext {
        val matcher = messageRegex.matchEntire(exception.message!!)
        return if (matcher != null) {
            val code = matcher.groupValues[1]
            val msg = matcher.groupValues[2]
            SqlExceptionContext(msg, code)
        } else {
            val matcherNet = messageRegexNetError.matchEntire(exception.message!!)
            return if (matcherNet != null) {
                val code = matcherNet.groupValues[1]
                val msg = matcherNet.groupValues[2]
                val ip = matcherNet.groupValues[3]
                SqlExceptionContext("$msg, server = $ip", code)
            } else {
                // parse error return origin error message
                SqlExceptionContext(exception.message!!, "")
            }
        }
    }
}
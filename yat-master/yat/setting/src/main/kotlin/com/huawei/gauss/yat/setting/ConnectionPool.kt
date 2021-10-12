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

package com.huawei.gauss.yat.setting

import com.huawei.gauss.yat.common.YatRuntimeError
import java.sql.Connection
import java.sql.DriverManager


class ConnectionPool {
    companion object {
        private fun makeURL(url: String, host: String, port: Int, name: String, opt: String): String {
            return url.replace("\${host}", host)
                    .replace("\${port}", port.toString())
                    .replace("\${name}", name)
                    .replace("\${opt}", opt)
        }
    }

    private var autocommit = true
    private var nodes: Map<String, YatContext.Node> = mapOf()

    fun initialize(context: YatContext) {
        autocommit = context.jdbc.autocommit
        nodes = context.nodes
    }

    fun getConnection(nodeName: String = "default", username: String? = null, password: String? = null, host: String? = null, port: Int? = null): Connection {
        val node = nodes[nodeName] ?: throw YatRuntimeError("not found given host name $nodeName")

        val realUsername = username ?: node.db.user
        val realPassword = password ?: node.db.password
        val realHost = host ?: node.db.host
        val realPort = port ?: node.db.port
        val realURL = makeURL(node.db.url, realHost, realPort, node.db.name, node.db.opt)

        val connection = getConnection(realURL, node.db.driver, realUsername, realPassword)
        connection.autoCommit = autocommit
        return connection
    }

    private fun getConnection(url: String, driver: String, username: String?, password: String?): Connection {
        Class.forName(driver)
        return if (username == null && password == null) {
            DriverManager.getConnection(url)
        } else {
            DriverManager.getConnection(url, username, password)
        }
    }
}

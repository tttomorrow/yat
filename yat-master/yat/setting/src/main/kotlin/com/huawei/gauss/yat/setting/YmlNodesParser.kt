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

import org.yaml.snakeyaml.Yaml
import java.io.File

class YmlNodesParser(private val nodesFile: File, private val context: YatContext) {
    fun parse() {
        val yml = Yaml()
        val tryNodes: Any = yml.load(nodesFile.reader()) ?: return

        try {
            when (tryNodes) {
                is Map<*, *> -> {
                    val nodes: Map<String, Map<String, Any>> = yml.load(nodesFile.reader()) ?: return
                    parseMapNodes(nodes)
                }
                is List<*> -> {
                    System.err.println("Warning: Deprecated nodes configure found, it will not be support in future")
                    val nodes: List<Map<String, Any>> = yml.load(nodesFile.reader()) ?: return
                    parseListNodes(nodes)
                }
                else -> {
                    throw SettingParseError("parse node file: ${nodesFile.absolutePath} failed with error: Invalid nodes configure file found")
                }
            }
        } catch (e: Exception) {
            when (e) {
                is ClassCastException, is NoSuchElementException ->
                    throw SettingParseError("parse node file: ${nodesFile.absolutePath} failed with error: ${e.message}", e)
                else -> throw e
            }
        }
    }

    private fun parseMapNodes(nodes: Map<String, Map<String, Any>>) = nodes.forEach { (name, node) ->
        context.nodes[name] = parseCommon(name, node)
    }


    private fun parseListNodes(nodes: List<Map<String, Any>>) = nodes.forEach { node ->
        val name = node["name"] as String
        context.nodes[name] = parseCommon(name, node)
    }

    private fun parseCommon(name: String, node: Map<String, Any>): YatContext.Node {
        @Suppress("UNCHECKED_CAST")
        val db = node["db"] as Map<String, Any>

        @Suppress("UNCHECKED_CAST")
        val ssh = node["ssh"] as Map<String, Any>

        val hostValue = node.getValue("host") as String

        val host = YatContext.Node(name)

        host.db.port = db.getValue("port") as Int
        host.db.user = db.getValue("username") as String
        host.db.password = db.getValue("password") as String
        host.db.name = db.getOrDefault("name", "") as String
        host.db.host = hostValue
        host.db.type = db.getOrDefault("type", "") as String
        host.db.url = db.getOrDefault("url", "") as String
        host.db.driver = db.getOrDefault("driver", "") as String
        host.db.opt = db.getOrDefault("opt", "") as String

        host.ssh.host = hostValue
        host.ssh.user = ssh.getValue("username") as String
        host.ssh.password = ssh.getValue("password") as String
        host.ssh.port = if (ssh.containsKey("port")) {
            ssh.getValue("port") as Int
        } else {
            22
        }

        return rewrite(host)
    }

    private fun rewrite(host: YatContext.Node): YatContext.Node {
        if (host.db.url.isEmpty() && host.db.type.isEmpty()) {
            throw SettingParseError("parse node file: ${nodesFile.absolutePath} failed with error: url or type must be supply for db properties")
        } else if (host.db.url.isEmpty()) {
            if (host.db.type !in drivers) {
                throw SettingParseError("parse node file: ${nodesFile.absolutePath} failed with error: found not support db type ${host.db.type}")
            }
            val driverInfo = drivers.getValue(host.db.type)
            host.db.url = driverInfo.url
            if (host.db.driver.isEmpty()) {
                host.db.driver = driverInfo.driver
            }
        }

        return host
    }

    private data class DriverInfo(val driver: String, val url: String)

    companion object {
        private val drivers = mapOf(
                Pair("zenith",
                        DriverInfo("com.huawei.gauss.jdbc.ZenithDriver", "jdbc:zenith:@\${host}:\${port}?useSSL=false")),
                Pair("postgresql",
                        DriverInfo("org.postgresql.Driver", "jdbc:postgresql://\${host}:\${port}/\${name}")),
                Pair("oracle",
                        DriverInfo("oracle.jdbc.driver.OracleDriver", "jdbc:oracle:thin:@\${host}:\${port}:\${name}"))
        )
    }
}
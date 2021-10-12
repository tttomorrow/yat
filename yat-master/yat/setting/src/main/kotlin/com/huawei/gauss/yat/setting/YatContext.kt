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

import com.beust.jcommander.JCommander
import com.huawei.gauss.yat.common.PathSearcher
import com.huawei.gauss.yat.common.YatExitNormal
import com.huawei.gauss.yat.common.YatRuntimeError
import org.yaml.snakeyaml.Yaml
import java.io.PrintStream


class YatContext {
    fun load(home: String, args: Array<String>) {
        load(home, parseCommandLine(args))
    }

    fun load(home: String, command: Command) {
        val workDir = YatWorkDir(command.testDir)

        loadConfigure(command, workDir)
        loadNodes(command, workDir)
        loadFromCommandLine(home, command, workDir)
        loadSuiteSettings(workDir)
        loadScheduleSettings(command.schedule, workDir)
        connectionPool.initialize(this)
        loadMacros(command, workDir)
    }

    private fun loadMacros(command: Command, workDir: YatWorkDir) {
        val macroFile = if (command.macroConfigureFile.isEmpty()) {
            CONST_MACRO_YML_FILE
        } else {
            command.macroConfigureFile
        }

        val realMacroFile = PathSearcher(".", workDir.confDir.absolutePath).search(macroFile)
        if (realMacroFile != null) {
            this.macroFile = realMacroFile.absolutePath
            macro.load(realMacroFile)
        }

        command.macros.forEach {
            val index = it.indexOf('=')
            if (index == -1 || index == it.length - 1) {
                throw YatRuntimeError("-i $it is not a legal parameter")
            }

            val key = it.substring(0, index)
            val value = it.substring(index + 1)

            macro.set(key.trim(), value.trim())
        }

        initHostsMacro()
        macro.set(CONST_SUITE_DIR, workDir.output.outputDir.absolutePath)
        macro.set(CONST_SUITE_TMP, workDir.output.tempDir.absolutePath)
    }

    private fun loadConfigure(command: Command, workDir: YatWorkDir) {
        val configPath = if (command.configureFile.isEmpty()) {
            CONST_CONFIG_YML_FILE
        } else {
            command.configureFile
        }

        val realConfPath = PathSearcher(".", workDir.confDir.absolutePath).search(configPath)

        if (realConfPath != null) {
            this.configure = realConfPath.absolutePath
            if (realConfPath.name.endsWith(".yml") || realConfPath.name.endsWith(".yaml")) {
                YmlSettingsParser(realConfPath, this).parse()
            } else {
                throw SettingParseError("configure file ${realConfPath.name}'s name is illegal")
            }
        }
    }

    private fun loadNodes(command: Command, workDir: YatWorkDir) {
        val nodesPath = if (command.nodesConfigureFile.isEmpty()) {
            CONST_NODES_YML_FILE
        } else {
            command.nodesConfigureFile
        }

        val realPath = PathSearcher(".", workDir.confDir.absolutePath).search(nodesPath)
        if (realPath != null) {
            this.nodeFile = realPath.absolutePath
            if (realPath.name.endsWith(".yml") || realPath.name.endsWith(".yaml")) {
                YmlNodesParser(realPath, this).parse()
            } else {
                throw SettingParseError("nodes file ${realPath.name}'s name is illegal")
            }
        } else {
            // load at lest one
            nodes["default"] = Node("default")
        }
    }

    private fun initHostsMacro() {
        nodes.forEach { (k, v) ->
            // db info
            macro.set("${k.uppercase()}_DB_HOST", v.db.host)
            macro.set("${k.uppercase()}_DB_PORT", v.db.port.toString())
            macro.set("${k.uppercase()}_DB_USER", v.db.user)
            macro.set("${k.uppercase()}_DB_PASSWD", v.db.password)
            macro.set("${k.uppercase()}_DB_TYPE", v.db.type)
            macro.set("${k.uppercase()}_DB_NAME", v.db.name)

            // ssh info
            macro.set("${k.uppercase()}_SSH_HOST", v.ssh.host)
            macro.set("${k.uppercase()}_SSH_USER", v.ssh.user)
            macro.set("${k.uppercase()}_SSH_PASSWD", v.ssh.password)
            macro.set("${k.uppercase()}_SSH_PORT", v.ssh.port.toString())
        }
    }

    private fun loadFromCommandLine(home: String, command: Command, workDir: YatWorkDir) {
        // configure value from command line
        this.home = home
        this.action = command.action
        workDir.setExpect(command.expect)
        suite.expect = command.expect
        scheduleMode = command.mode
        forceSerial = command.serial
        target.target = command.targetHost
        target.left = command.leftHost
        target.right = command.rightHost
        reporter.color = command.color
        reporter.bare = command.bare
        if (command.width > 0) {
            reporter.width = command.width
        }
        cases = command.cases

        echoSql = command.sqlEcho
        panic = command.panic
        if (command.timeout > 0) {
            case.timeout = command.timeout
        }
    }

    private fun loadSuiteSettings(workDir: YatWorkDir) {
        suite.vSuite = workDir
        suite.name = workDir.workDir.toPath().fileName.toString()
    }

    private fun loadScheduleSettings(scheduleName: String, workDir: YatWorkDir) {
        val scheduleList = if (scheduleName.isEmpty()) {
            arrayOf(CONST_SCHEDULE_SCHD_FILE, CONST_SCHEDULE_YAT_FILE)
        } else {
            arrayOf(scheduleName)
        }

        val scheduleSearcher = PathSearcher(".", workDir.scheduleDir.absolutePath)
        val res = scheduleSearcher.search(*scheduleList)
        if (res != null) {
            schedule = res.absolutePath
        }
    }

    private fun parseCommandLine(args: Array<String>): Command {
        val command = Command()

        val jCommander = JCommander.newBuilder().addObject(command).programName(CONST_PROGRAM_NAME).build()
        jCommander.parse(*args)

        if (command.help) {
            jCommander.usage()
            throw YatExitNormal()
        }

        if (command.version) {
            println(Version.detailVersionInfo())
            throw YatExitNormal()
        }

        return command
    }

    class DB {
        var host = "127.0.0.1"
        var port = 1611
        var user = "yat"
        var name = ""
        var password = ""
        var type = "zenith"
        var driver = ""
        var url = ""
        var opt = ""
    }

    class SSH {
        var port = 22
        var host = "127.0.0.1"
        var user = ""
        var password = ""
    }

    class Node(var name: String) {
        var db = DB()
        var ssh = SSH()
    }

    class Compare {
        var type = "smart"
        var ignoreCase = true
        var disorder = true
        var hash = false
    }

    class Case {
        var outSuffix = ""
        var outMode = "pretty"
        var timeout = 0L
    }

    class Suite {
        var name = ""
        var expect = ""
        lateinit var vSuite: YatWorkDir
    }

    class JDBC {
        var checkingSQL = "select 1"
        var autocommit = true
    }

    class Reporter {
        var filling = '.'
        var width = 100
        var color = false
        var bare = false
    }

    class Limit {
        var caseMaxCount = 500
        var caseMaxSize = 15000
        var caseMaxDepth = 2
        var caseNamePattern = Regex("[a-z0-9_]+")
    }

    class Checking {
        var limit = Limit()
    }

    class Target {
        var target = "default"
        var left = "left"
        var right = "right"
    }

    val connectionPool = ConnectionPool() // connection pool using jdbc
    val macro = Macro()
    var nodes = mutableMapOf<String, Node>()
    var checking = Checking()
    var case = Case()
    var jdbc = JDBC()
    var reporter = Reporter()
    var compare = Compare()
    var schedule = "" // schedule configure file path
    var macroFile = "" // macro configure file path
    var nodeFile = "" // node configure file path
    var configure = "" // configure file path
    var home = "" // yat home path
    var suite = Suite()
    var panic = false // panic when error or not
    var echoSql = true // echo sql statement or not
    var forceSerial = false // force run all test case serial
    var scheduleMode = "regress" // schedule mode to schedule test case
    var target = Target()
    var zsql = "zsql"
    var gsql = "gsql"
    var cases = ""
    var action = "run" // action to do [run, info, debug]

    fun dump(out: PrintStream? = null) {
        val writer = out?.writer() ?: this.suite.vSuite.output.contextLog.writer()

        Yaml().dump(this, writer)
    }
}
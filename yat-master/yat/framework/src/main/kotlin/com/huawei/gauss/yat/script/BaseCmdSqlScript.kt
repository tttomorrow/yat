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

package com.huawei.gauss.yat.script

import com.huawei.gauss.yat.common.MacroReplacer
import com.huawei.gauss.yat.common.commander.ProcessCommander
import java.io.File
import java.io.IOException
import java.nio.file.Path
import java.nio.file.Paths


abstract class BaseCmdSqlScript(builder: Builder) : FileOutputScript() {
    enum class CmdScriptType {
        TYPE_ZSQL,
        TYPE_GSQL
    }

    class Builder {
        var user: String = ""
            private set
        var password: String = ""
            private set
        var host: String = ""
            private set
        var port: Int = 0
            private set
        var dbname: String = ""
            private set
        var testDir: String = ""
            private set
        var tempDir: String = ""
            private set
        var cmdPath: String = ""
            private set
        var echo: Boolean = true
            private set
        var env: Map<String, String> = mapOf()
            private set
        var output: File? = null
            private set

        fun user(user: String) = apply { this.user = user }
        fun password(password: String) = apply { this.password = password }
        fun host(host: String) = apply { this.host = host }
        fun port(port: Int) = apply { this.port = port }
        fun dbname(dbname: String) = apply { this.dbname = dbname }
        fun testDir(testDir: String) = apply { this.testDir = testDir }
        fun tempDir(tempDir: String) = apply { this.tempDir = tempDir }
        fun cmdPath(cmdPath: String) = apply { this.cmdPath = cmdPath }
        fun echo(echo: Boolean) = apply { this.echo = echo }
        fun env(env: Map<String, String>) = apply { this.env = env }
        fun output(output: File) = apply { this.output = output }

        fun build(type: CmdScriptType): BaseCmdSqlScript {
            return when (type) {
                CmdScriptType.TYPE_ZSQL -> ZSqlScript(this)
                CmdScriptType.TYPE_GSQL -> GSqlScript(this)
            }
        }
    }

    protected val user = builder.user
    protected val password = builder.password
    protected val host = builder.host
    protected val port = builder.port
    protected val dbname = builder.dbname
    protected val testDir = builder.testDir
    protected val tempDir = builder.tempDir
    protected val cmdPath = builder.cmdPath
    protected val output = builder.output!!
    protected val echo = builder.echo
    protected val env = builder.env

    inner class CmdCommander(private val defaultCmd: String, private val conn: String) {
        private val commander = ProcessCommander()

        fun sfexec(sql: String, output: File, env: Map<String, String>? = null): Int {
            val cmd = mutableListOf(cmdPath(), conn)
            cmdSetting(cmd)
            buildCmdExecFromParams(cmd, sql)

            return commander.sfexec(*cmd.toTypedArray(), output = output, env = env)
        }

        fun isfexec(sql: String, output: File, env: Map<String, String>? = null): Int {
            val cmd = mutableListOf(cmdPath(), conn)
            cmdSetting(cmd)

            return commander.sfexec(*cmd.toTypedArray(), input = sql, output = output, env = env)
        }

        fun ffexec(sqlFile: File, output: File, env: Map<String, String>? = null): Int {
            val cmd = mutableListOf(cmdPath(), conn)
            cmdSetting(cmd)
            buildCmdExecFromFile(cmd, sqlFile)

            return commander.sfexec(*cmd.toTypedArray(), output = output, env = env)
        }

        private fun cmdPath(): String {
            val macroCmd = getCmdPathFromMacro()
            return when {
                macroCmd != null -> {
                    macroCmd
                }
                cmdPath.isNotEmpty() -> {
                    return cmdPath
                }
                else -> {
                    defaultCmd
                }
            }
        }
    }

    abstract fun getCmdPathFromMacro(): String?
    abstract fun cmdSetting(cmd: MutableList<String>)
    abstract fun makeMirrorFile(relative: Path): File
    abstract fun makeCommander(): CmdCommander
    abstract fun buildCmdExecFromFile(cmd: MutableList<String>, sqlFile: File)
    abstract fun buildCmdExecFromParams(cmd: MutableList<String>, sql: String)

    open fun execute(script: String): Boolean {
        val realScript = makeRealScript(script, env)

        val commander = makeCommander()
        makeParentPathExists(output)
        return try {
            0 == commander.sfexec(realScript, output = output, env = env)
        } catch (e: IOException) {
            output.writeText(e.message!!)
            false
        }
    }

    open fun execute(scriptFile: File): Boolean {
        val realScriptFile = makeRealScript(scriptFile, env)
        val commander = makeCommander()
        makeParentPathExists(output)
        return try {
            0 == commander.ffexec(realScriptFile, output = output, env = env)
        } catch (e: IOException) {
            if (e.message != null) {
                output.writeText(e.message!!)
            }
            false
        }
    }

    open fun iexecute(script: String): Boolean {
        val realScript = makeRealScript(script, env)

        val commander = makeCommander()
        makeParentPathExists(output)

        return try {
            0 == commander.isfexec(realScript, output = output, env = env)
        } catch (e: IOException) {
            output.writeText(e.message!!)
            false
        }
    }

    private fun makeRealScript(script: String, macro: Map<String, String>): String {
        return MacroReplacer(script).replace(macro)
    }

    private fun makeRealScript(scriptFile: File, macro: Map<String, String>): File {
        val realScript = MacroReplacer(scriptFile.bufferedReader().readText()).replace(macro)

        val abs = scriptFile.absolutePath
        val relative = Paths.get(abs.slice(IntRange(testDir.length, abs.length - 1)))
        val realScriptFile = makeMirrorFile(relative)
        makeParentPathExists(realScriptFile)
        realScriptFile.writeText(realScript)

        return realScriptFile
    }
}
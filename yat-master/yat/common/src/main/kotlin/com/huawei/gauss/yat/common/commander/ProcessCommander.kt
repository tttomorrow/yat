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

package com.huawei.gauss.yat.common.commander

import com.huawei.gauss.yat.common.WorkPool
import org.slf4j.LoggerFactory
import java.io.File
import java.io.InputStream
import java.io.OutputStream
import java.util.concurrent.Callable
import java.util.concurrent.Future


class ProcessCommander {
    companion object {
        private val logger = LoggerFactory.getLogger(ProcessCommander::class.java)

        fun write(writer: OutputStream, input: String) {
            WorkPool.pool.submit(Writer(writer, input))
        }

        fun read(reader: InputStream): Future<String> {
            return WorkPool.pool.submit(Reader(reader))
        }
    }

    private class Writer(private val writer: OutputStream, private val input: String) : Runnable {
        override fun run() {
            writer.write(input.toByteArray())
            writer.flush()
            writer.close()
        }
    }

    private class Reader(private val reader: InputStream) : Callable<String> {
        override fun call(): String {
            return reader.bufferedReader().readText()
        }
    }

    private fun execCommon(vararg cmds: String, env: Map<String, String>? = null): Process {
        val builder = ProcessBuilder(*cmds)
        builder.redirectErrorStream(true)
        setEnv(builder, env)

        return builder.start()
    }

    private fun execInherit(vararg cmds: String, env: Map<String, String>? = null): Process {
        val builder = ProcessBuilder(*cmds)
        builder.redirectErrorStream(true)
        builder.inheritIO()
        setEnv(builder, env)

        return builder.start()
    }

    private fun setEnv(builder: ProcessBuilder, env: Map<String, String>? = null) {
        val processEnv = builder.environment()
        env?.forEach { t, u ->
            processEnv[t] = u
        }
    }

    fun iiexec(vararg cmds: String, env: Map<String, String>? = null): Int {
        val proc = execInherit(*cmds, env = env)

        val exitValue = proc.waitFor()

        logger.info("execute cmd: {}", cmds.joinToString(" "))
        return exitValue
    }

    fun exec(vararg cmds: String, env: Map<String, String>? = null): Int {
        val proc = execCommon(*cmds, env = env)
        val exitValue = proc.waitFor()

        logger.info("execute cmd: {}", cmds.joinToString(" "))
        return exitValue
    }

    fun ssexec(vararg cmds: String, input: String? = null, env: Map<String, String>? = null): CommandResult {
        val proc = execCommon(*cmds, env = env)

        if (input != null) {
            write(proc.outputStream, input)
        }

        val reader = read(proc.inputStream)
        val exitValue = proc.waitFor()

        logger.info("execute cmd: {}", cmds.joinToString(" "))
        return CommandResult(exitValue, reader.get())
    }

    fun sfexec(vararg cmds: String, input: String? = null, output: File? = null, env: Map<String, String>? = null): Int {
        val builder = ProcessBuilder(*cmds)

        if (output != null) {
            builder.redirectErrorStream(true)
            builder.redirectOutput(output)
        }

        setEnv(builder, env)

        val proc = builder.start()

        if (input != null) {
            write(proc.outputStream, input)
        }

        val ret = proc.waitFor()
        logger.info("execute cmd: {}", cmds.joinToString(" "))
        return ret

    }

    fun fsexec(vararg cmds: String, input: File? = null, env: Map<String, String>? = null): CommandResult {
        val builder = ProcessBuilder(*cmds)
        builder.redirectErrorStream(true)

        if (input != null) {
            builder.redirectInput(input)
        }

        setEnv(builder, env)
        val proc = builder.start()

        val reader = read(proc.inputStream)
        val exitValue = proc.waitFor()

        logger.info("execute cmd: {}", cmds.joinToString(" "))
        return CommandResult(exitValue, reader.get())
    }

    fun ffexec(vararg cmds: String, input: File? = null, output: File? = null, env: Map<String, String>? = null): Int {
        val builder = ProcessBuilder(*cmds)

        if (output != null) {
            builder.redirectErrorStream(true)
            builder.redirectOutput(output)
        }

        if (input != null) {
            builder.redirectInput(input)
        }

        setEnv(builder, env)
        val ret = builder.start().waitFor()
        logger.info("execute cmd: {}", cmds.joinToString(" "))
        return ret
    }
}



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

import org.junit.platform.engine.discovery.DiscoverySelectors
import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder
import org.junit.platform.launcher.core.LauncherFactory
import org.junit.platform.launcher.listeners.SummaryGeneratingListener
import spock.util.EmbeddedSpecCompiler
import java.io.File
import java.io.PrintWriter


class SpockScript(private val output: File) : FileOutputScript() {
    private fun executeCls(source: String): Boolean {
        val compiler = EmbeddedSpecCompiler()
        compiler.unwrapCompileException = false

        val clss = compiler.compile(source) as List<Class<*>>
        val request = LauncherDiscoveryRequestBuilder.request()
            .selectors(clss.map { DiscoverySelectors.selectClass(it) })
            .build()

        val launcher = LauncherFactory.create()
        launcher.discover(request)
        val listener = SummaryGeneratingListener()
        launcher.registerTestExecutionListeners(listener)
        launcher.execute(request)

        val printer = PrintWriter(output)
        listener.summary.printFailuresTo(printer)
        listener.summary.printTo(printer)

        return listener.summary.testsFailedCount == 0L
    }

    fun execute(script: String): Boolean {
        return executeCls(script)
    }

    fun execute(scriptFile: File): Boolean {
        return executeCls(scriptFile.readText())
    }
}
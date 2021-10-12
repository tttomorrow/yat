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

import com.beust.jcommander.Parameter
import java.io.File

class Command {
    @Parameter(names = ["-a", "--action"], description = "Set the action to do [run, info, debug]")
    var action: String = "run"

    @Parameter(names = ["-s", "--schedule"], description = "The schedule file")
    var schedule: String = ""

    @Parameter(names = ["-m", "--mode"], description = "The mode to run the testcase [single, compare, regress]")
    var mode: String = "regress"

    @Parameter(names = ["-d", "--test-dir"], description = "Setting the test directory")
    var testDir: String = "."

    @Parameter(names = ["-l", "--left"], description = "Set the left node host name")
    var leftHost: String = "left"

    @Parameter(names = ["-r", "--right"], description = "Set the right node host name")
    var rightHost: String = "right"

    @Parameter(names = ["-t", "--target"], description = "Set the target node host name")
    var targetHost: String = "default"

    @Parameter(names = ["-f", "--configure"], description = "Set the configure file to load")
    var configureFile: String = ""

    @Parameter(names = ["-n", "--nodes"], description = "Set the node configure file to load")
    var nodesConfigureFile: String = ""

    @Parameter(names = ["-e", "--macros"], description = "Set the macros configure file to load")
    var macroConfigureFile: String = ""

    @Parameter(names = ["-i", "--macro"], description = "Set the macro to load")
    var macros: MutableList<String> = mutableListOf()

    @Parameter(names = ["--version"], description = "Get the version information")
    var version: Boolean = false

    @Parameter(names = ["--no-echo"], description = "Not echo the sql text to output")
    var sqlEcho: Boolean = true

    @Parameter(names = ["--panic"], description = "Panic the process when error")
    var panic: Boolean = false

    @Parameter(names = ["-h", "--help"], description = "Print this help message")
    var help: Boolean = false

    @Parameter(names = ["--serial"], description = "Execute all testcase serial")
    var serial: Boolean = false

    @Parameter(names = ["--bare"], description = "Only show test case output")
    var bare: Boolean = false

    @Parameter(names = ["--color"], description = "print report with color")
    var color: Boolean = false

    @Parameter(names = ["--lib-path"], description = "Set the jar library search path")
    var libPath: String = ""

    @Parameter(names = ["--daemon"], description = "Run Yat in daemon mode")
    var daemon: Boolean = false

    @Parameter(names = ["--width"], description = "Set the output report print-width")
    var width: Int = 0

    @Parameter(names = ["-c", "--cases"], description = "Set the cases to debug")
    var cases: String = ""

    @Parameter(names = ["--timeout"], description = "Set the case timeout")
    var timeout = 0L

    @Parameter(names = ["--expect"], description = "Set the expect sub directory")
    var expect = ""

    constructor()
    constructor(testDir: File) {
        this.testDir = testDir.toString()
    }
}
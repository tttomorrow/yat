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

package com.huawei.gauss.yat.scheduler.parser

import com.huawei.gauss.yat.scheduler.parser.cmd.CmdParser
import com.huawei.gauss.yat.scheduler.parser.regress.RegressParser
import com.huawei.gauss.yat.scheduler.parser.yat.YatParser
import java.io.File

interface Parser {
    companion object {
        fun create(schedule: File, importPaths: Array<String>): Parser {
            val stream = schedule.bufferedReader()
            return when (schedule.extension) {
                "schd" -> RegressParser(stream, importPaths)
                "yat" -> YatParser(stream, importPaths)
                else -> throw ScheduleSyntaxError("the given schedule's extension ${schedule.extension} is illegal")
            }
        }

        fun create(line: String): Parser {
            return CmdParser(line)
        }
    }

    fun parse(): ScheduleTree
}
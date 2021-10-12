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

package com.huawei.gauss.yat.report

import java.io.File
import java.io.OutputStream
import java.time.Duration
import java.time.LocalDateTime

class RedoLog(private val log: File) {
    companion object {
        private val LF = "\n".toByteArray()
    }

    enum class Result {
        SUCCESS,
        FAILED,
        IGNORE,
        NO_DIFF_OK,
        NO_DIFF_FAILED,
        NO_VALID,
        TIMEOUT
    }

    interface Record {
        fun toBytes(): ByteArray
    }

    class CaseRecord(val suite: String, val group: Int, val name: String,
                     val time: Duration, val start: LocalDateTime, val res: Result) : Record {
        override fun toBytes(): ByteArray {
            return "case|$suite|$group|$name|$time|$start|$res".toByteArray()
        }
    }

    class GroupRecord(val suite: String, val group: Int, val time: Duration, val start: LocalDateTime) : Record {
        override fun toBytes(): ByteArray {
            return "group|$suite|$group|$time|$start".toByteArray()
        }
    }

    class SuiteRecord(val suite: String, val time: Duration, val start: LocalDateTime) : Record {
        override fun toBytes(): ByteArray {
            return "suite|$suite|$time|$start".toByteArray()
        }
    }

    class IntervalSuiteRecord(val suite: String, val time: Duration, val start: LocalDateTime, val count: Int) : Record {
        override fun toBytes(): ByteArray {
            return "interval|$suite|$time|$start|$count".toByteArray()
        }
    }

    class DaemonSuiteRecord(val suite: String, val time: Duration, val start: LocalDateTime) : Record {
        override fun toBytes(): ByteArray {
            return "daemon|$suite|$time|$start".toByteArray()
        }
    }

    class ScheduleRecord(val schedule: String, val time: Duration, val start: LocalDateTime) : Record {
        override fun toBytes(): ByteArray {
            return "schedule|$schedule|$time|$start".toByteArray()
        }
    }

    private val stream: OutputStream

    init {
        stream = log.outputStream().buffered()
    }

    @Synchronized
    fun addRecord(recode: Record) {
        stream.write(recode.toBytes())
        stream.write(LF)
        stream.flush()
    }
}
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

package com.huawei.gauss.yat.sql

import org.apache.commons.codec.binary.Hex
import java.io.ByteArrayOutputStream
import java.io.InputStream
import java.io.Reader
import java.sql.Array
import java.sql.Blob
import java.sql.Clob
import java.sql.Date
import java.sql.Time
import java.sql.Timestamp
import java.time.format.DateTimeFormatter

class ResultValue(val value: Any?, val type: Int) {
    override fun toString(): String {
        return unifyString()
    }

    private fun unifyString(): String {
        return if (value == null) {
            ""
        } else {
            normalString(value)
        }
    }

    private fun normalString(value: Any): String {
        return when (value) {
            is kotlin.Array<*> -> readLocalArray(value)
            is Timestamp -> readTimestamp(value)
            is Time -> readTime(value)
            is Date -> readDate(value)
            is ByteArray -> readByteArray(value)
            is Array -> readSqlArray(value)
            is Clob -> readClob(value)
            is Blob -> readBlob(value)
            else -> value.toString()
        }
    }

    private fun readLocalArray(value: Any): String {
        return arrayToString(value as kotlin.Array<*>)
    }

    private fun arrayToString(value: kotlin.Array<*>): String {
        val builder = StringBuilder()

        builder.append("{")
        var first = true
        for (item in value) {
            val itemStr = if (item == null) {
                ""
            } else {
                normalString(item)
            }
            if (first) {
                first = false
            } else {
                builder.append(",")
            }
            builder.append(itemStr)
        }

        builder.append("}")
        return builder.toString()
    }

    private fun readBlob(value: Any): String {
        val blob = value as Blob
        return readByteStream(blob.binaryStream)
    }

    private fun readByteArray(value: Any): String {
        val array = value as ByteArray
        return Hex.encodeHexString(array)
    }

    private fun readSqlArray(value: Any): String {
        val array = value as Array
        return arrayToString(array.array as kotlin.Array<*>)
    }

    private fun readClob(value: Any): String {
        val clob = value as Clob
        return readCharStream(clob.characterStream)
    }

    private fun readTime(value: Any): String {
        val time = value as Time
        return time.toLocalTime().format(timePattern)
    }

    private fun readDate(value: Any): String {
        val date = value as Date
        return date.toLocalDate().format(datePattern)
    }

    private fun readTimestamp(value: Any): String {
        val time = value as Timestamp
        return time.toLocalDateTime().format(timestampPattern)
    }

    companion object {
        private val datePattern = DateTimeFormatter.ofPattern("yyyy-MM-dd")
        private val timePattern = DateTimeFormatter.ofPattern("HH:mm:ss")
        private val timestampPattern = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.nnnnnnnnn")
        private const val MAX_CLOB_SIZE = 128
        private const val MAX_BLOB_SIZE = 64
        private const val BUF_SIZE = 1024

        private fun readByteStream(stream: InputStream): String {
            val builder = ByteArrayOutputStream()
            val buffer = ByteArray(BUF_SIZE)
            var readCount: Int
            var sum = 0
            var overflow = false

            while (stream.read(buffer).also { readCount = it } > 0) {
                if (sum < MAX_BLOB_SIZE) {
                    val writeCount = if (sum + readCount <= MAX_BLOB_SIZE) {
                        readCount
                    } else {
                        MAX_BLOB_SIZE - sum
                    }
                    builder.write(buffer, 0, writeCount)
                    sum += writeCount
                }

                if (sum == MAX_BLOB_SIZE) {
                    overflow = true
                }
            }
            return Hex.encodeHexString(builder.toByteArray()) + if (overflow) {
                "..."
            } else {
                ""
            }
        }

        private fun readCharStream(reader: Reader): String {
            val builder = StringBuilder()
            val buffer = CharArray(BUF_SIZE)
            var readCount: Int
            var sum = 0
            var overflow = false

            while (reader.read(buffer).also { readCount = it } > 0) {
                if (sum < MAX_CLOB_SIZE) {
                    val writeCount = if (sum + readCount <= MAX_CLOB_SIZE) {
                        readCount
                    } else {
                        MAX_CLOB_SIZE - sum
                    }
                    builder.append(buffer, 0, writeCount)
                    sum += writeCount
                }

                if (sum == MAX_CLOB_SIZE) {
                    overflow = true
                }
            }

            return builder.toString() + if (overflow) {
                "..."
            } else {
                ""
            }
        }
    }

}
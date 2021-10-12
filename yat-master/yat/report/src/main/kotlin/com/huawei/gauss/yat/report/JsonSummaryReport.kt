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

import com.fasterxml.jackson.annotation.JsonProperty
import com.fasterxml.jackson.databind.ObjectMapper
import com.huawei.gauss.yat.common.YatRuntimeError
import java.io.File
import java.nio.file.Paths
import java.time.Duration
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

class JsonSummaryReport(private val name: String, private val filename: File) : SummaryReport {

    companion object {
        private val dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
    }

    data class CaseResult(
            @get: JsonProperty("case") val case: String,
            @get: JsonProperty("caseType") val caseType: String,
            @get: JsonProperty("result") val result: String,
            @get: JsonProperty("startTime") val start: String,
            @get: JsonProperty("usingTime") val time: Long,
            @get: JsonProperty("valid") val valid: String
    )

    data class GroupResult(@get: JsonProperty("type") val type: String) {
        @get: JsonProperty("cases")
        val cases = mutableListOf<CaseResult>()

        @Synchronized
        fun addCase(case: CaseResult) {
            cases.add(case)
        }
    }

    data class SuiteResult(@get: JsonProperty("name") val name: String) {
        @get: JsonProperty("results")
        val results = mutableListOf<GroupResult>()

        @Synchronized
        fun addGroup(group: GroupResult) {
            results.add(group)
        }
    }

    data class JsonResult(@get: JsonProperty("suitePath") val suitePath: String) {
        @get: JsonProperty("suite")
        val suite: String = Paths.get(suitePath).fileName.toString()

        @JsonProperty("subSuites")
        val subSuites = mutableListOf<SuiteResult>()

        @JsonProperty("usingTime")
        var usingTime = 0L

        @JsonProperty("startTime")
        var startTime = ""

        @JsonProperty("endTime")
        var endTime = ""

        @Synchronized
        fun addSubSuite(suiteResult: SuiteResult) {
            subSuites.add(suiteResult)
        }
    }

    private val jsonReport = JsonResult(name)
    private var startTime = LocalDateTime.now()
    private var endTime = startTime

    class JsonGroupReport(private val groupResult: GroupResult) : GroupReport {
        override fun addTest(name: String, result: GroupReport.Result, start: LocalDateTime, time: Duration, meta: Map<String, String>) {
            var validStatus = "valid"
            val textResult = when (result) {
                GroupReport.Result.OK -> "ok"
                GroupReport.Result.FAILED -> "failed"
                GroupReport.Result.NO_DIFF_FAILED -> {
                    validStatus = "no-diff"
                    "failed"
                }
                GroupReport.Result.NO_DIFF_OK -> {
                    validStatus = "no-diff"
                    "ok"
                }
                GroupReport.Result.IGNORE -> {
                    validStatus = "ignore"
                    "ignore"
                }
                GroupReport.Result.NO_VALID -> {
                    validStatus = "no-valid"
                    "ok"
                }
                GroupReport.Result.TIMEOUT -> {
                    validStatus = "timeout"
                    "timeout"
                }
            }

            val caseType = meta["caseType"]
            if (caseType == null) {
                throw YatRuntimeError("Json report require test case meta key caseType")
            } else {
                groupResult.addCase(CaseResult(
                        name,
                        caseType,
                        textResult,
                        start.format(dateFormatter),
                        time.toNanos() / 1000000,
                        validStatus))
            }
        }

        override fun finish() {

        }
    }

    class EmptyGroupReport : GroupReport {
        override fun addTest(name: String, result: GroupReport.Result, start: LocalDateTime, time: Duration, meta: Map<String, String>) {

        }

        override fun finish() {
        }
    }

    class EmptySuiteReport : SuiteReport {
        override fun newGroupReport(): GroupReport {
            return EmptyGroupReport()
        }

        override fun newSetupGroup(): GroupReport {
            return EmptyGroupReport()
        }

        override fun newCleanupGroup(): GroupReport {
            return EmptyGroupReport()
        }

        override fun finish() {
        }
    }

    class JsonSuiteReport(private val suiteResult: SuiteResult) : SuiteReport {

        override fun newGroupReport(): GroupReport {
            val groupResult = GroupResult("group")
            suiteResult.addGroup(groupResult)
            return JsonGroupReport(groupResult)
        }

        override fun newSetupGroup(): GroupReport {
            val groupResult = GroupResult("setup")
            suiteResult.addGroup(groupResult)
            return JsonGroupReport(groupResult)
        }

        override fun newCleanupGroup(): GroupReport {
            val groupResult = GroupResult("cleanup")
            suiteResult.addGroup(groupResult)
            return JsonGroupReport(groupResult)
        }

        override fun finish() {
        }
    }

    override fun start() {
        startTime = LocalDateTime.now()
        jsonReport.startTime = startTime.format(dateFormatter)
    }

    override fun newSuiteReport(name: String): SuiteReport {
        val suite = SuiteResult(name)
        jsonReport.addSubSuite(suite)
        return JsonSuiteReport(suite)
    }

    override fun newDaemonReport(name: String): SuiteReport {
        return EmptySuiteReport()
    }

    override fun newIntervalReport(name: String): SuiteReport {
        return EmptySuiteReport()
    }

    override fun finish() {
        endTime = LocalDateTime.now()
        jsonReport.endTime = endTime.format(dateFormatter)
        jsonReport.usingTime = Duration.between(startTime, endTime).toMillis()
        val mapper = ObjectMapper()
        mapper.writerWithDefaultPrettyPrinter().writeValue(filename, jsonReport)
    }
}
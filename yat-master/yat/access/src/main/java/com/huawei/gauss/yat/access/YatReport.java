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

package com.huawei.gauss.yat.access;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.util.List;

@Data
public class YatReport {
    @JsonProperty("suite")
    String suite;

    @JsonProperty("suitePath")
    String suitePath;

    @JsonProperty("startTime")
    String startTime;

    @JsonProperty("endTime")
    String endTime;

    @JsonProperty("usingTime")
    long usingTime;

    @JsonProperty("subSuites")
    List<SubSuite> subSuites;

    @Data
    public static class SuiteCase {
        @JsonProperty("case")
        String caseName;

        @JsonProperty("caseType")
        String caseType;

        @JsonProperty("result")
        String result;

        @JsonProperty("startTime")
        String startTime;

        @JsonProperty("usingTime")
        long usingTime;

        @JsonProperty("valid")
        String valid;
    }

    @Data
    public static class SuiteGroup {
        @JsonProperty("type")
        String type;

        @JsonProperty("cases")
        List<SuiteCase> cases;
    }

    @Data
    public static class SubSuite {
        @JsonProperty("name")
        String name;

        @JsonProperty("results")
        List<SuiteGroup> results;
    }
}

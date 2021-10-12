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

import java.io.File;
import java.io.IOException;
import java.util.List;

public interface YatAccess {
    static YatAccess create(File testDir) {
        return new YatJsonAccess(testDir);
    }

    List<String> listSuites() throws IOException, YatAccessError;

    YatReport getReport(String suiteName) throws IOException, YatAccessError;

    String readCaseContent(String suiteName, String caseName) throws IOException, YatAccessError;

    String readCaseOutput(String suiteName, String caseName) throws IOException, YatAccessError;

    List<String> readCaseExpect(String suiteName, String caseName) throws IOException, YatAccessError;
}

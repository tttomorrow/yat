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

import com.fasterxml.jackson.databind.ObjectMapper;
import com.huawei.gauss.yat.common.TestCaseSearcher;
import com.huawei.gauss.yat.scheduler.parser.CaseMeta;
import com.huawei.gauss.yat.setting.Command;
import com.huawei.gauss.yat.setting.YatContext;
import lombok.Data;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static java.util.Collections.emptyList;


class YatJsonAccess implements YatAccess {
    private File testDir;
    private volatile boolean refresh = false;
    private Map<String, SuiteContext> suitesCache = new HashMap<>();

    public YatJsonAccess(File testDir) {
        this.testDir = testDir;
    }

    @Override
    public List<String> listSuites() throws IOException {
        refreshSuiteCache(true);

        return getSuiteList();
    }

    @Override
    public YatReport getReport(String suiteName) throws IOException, YatAccessError {
        refreshSuiteCache();

        SuiteContext suiteCtx = getSuiteCtx(suiteName);

        if (suiteCtx == null) {
            throw new YatAccessError("suite with name $suiteName is not exists");
        } else {
            ObjectMapper mapper = new ObjectMapper();
            File reportFile = Paths.get(suiteCtx.path.toString(), "log", "yat.json").toFile();
            return mapper.readValue(reportFile, YatReport.class);
        }
    }

    @Override
    public String readCaseContent(String suiteName, String caseName) throws IOException, YatAccessError {
        refreshSuiteCache();

        SuiteName suite = parseSuiteName(suiteName);

        SuiteContext suiteCtx = getSuiteCtx(suite.suiteName);
        if (suiteCtx == null) {
            throw new YatAccessError("suite with name ${suite.subSuiteName} is not exists");
        } else {
            CaseMeta meta = suiteCtx.context.getSuite().vSuite.getCaseMeta(caseName, suite.subSuiteName, suiteCtx.context.getCase().getOutSuffix());
            return new String(Files.readAllBytes(meta.getFile().toPath()), Charset.forName("utf-8"));
        }
    }

    @Override
    public String readCaseOutput(String suiteName, String caseName) throws IOException, YatAccessError {
        refreshSuiteCache();

        SuiteName suite = parseSuiteName(suiteName);

        SuiteContext suiteCtx = getSuiteCtx(suite.suiteName);
        if (suiteCtx == null) {
            throw new YatAccessError("suite with name $suiteName is not exists");
        } else {
            CaseMeta meta = suiteCtx.context.getSuite().vSuite.getCaseMeta(caseName, suite.subSuiteName, suiteCtx.context.getCase().getOutSuffix());
            return new String(Files.readAllBytes(meta.getOutput().toPath()), Charset.forName("utf-8"));
        }
    }

    @Override
    public List<String> readCaseExpect(String suiteName, String caseName) throws IOException, YatAccessError {
        refreshSuiteCache();

        SuiteName suite = parseSuiteName(suiteName);

        SuiteContext suiteCtx = getSuiteCtx(suite.suiteName);
        if (suiteCtx == null) {
            throw new YatAccessError("suite with name $suiteName is not exists");
        } else {
            TestCaseSearcher caseSearcher = new TestCaseSearcher(suiteCtx.path, suiteCtx.context.getSuite().vSuite.getExpectDir());
            try {
                List<File> expectFiles = caseSearcher.searchExpect(caseName, suite.subSuiteName, suiteCtx.context.getCase().getOutSuffix());
                List<String> expects = new ArrayList<>(expectFiles.size());

                for (File expect : expectFiles) {
                    expects.add(new String(Files.readAllBytes(expect.toPath()), Charset.forName("utf-8")));
                }
                return expects;
            } catch (IOException e) {
                return emptyList();
            }
        }
    }

    private boolean isFinishedSuiteDir(File dir) {
        File[] subFiles = dir.listFiles();
        if (subFiles == null) {
            return false;
        }

        if (subFiles.length > 20) {
            return false;
        }

        Map<String, Boolean> checker = new HashMap<>();
        checker.put("testcase", false);
        checker.put("expect", false);
        checker.put("log", false);
        checker.put("conf", false);
        checker.put("schedule", false);

        for (File subFile : subFiles) {
            if (subFile.isDirectory() && checker.containsKey(subFile.getName())) {
                checker.put(subFile.getName(), true);
            }
        }

        boolean isSuiteDir = true;
        for (Map.Entry<String, Boolean> entry : checker.entrySet()) {
            if (!entry.getValue()) {
                isSuiteDir = false;
                break;
            }
        }

        return isSuiteDir && Paths.get(dir.toString(), "log", "yat.json").toFile().exists();
    }

    private List<String> getSuiteList() {
        synchronized (this) {
            return new ArrayList<>(suitesCache.keySet());
        }
    }

    private SuiteContext getSuiteCtx(String suiteName) {
        synchronized (this) {
            return suitesCache.get(suiteName);
        }
    }

    private void refreshSuiteCache() throws IOException {
        refreshSuiteCache(false);
    }

    private void refreshSuiteCache(boolean force) throws IOException {
        if (force) {
            synchronized (this) {
                refreshSuiteCacheInner(this.testDir);
                refresh = true;
            }
        } else {
            if (!refresh) {
                synchronized (this) {
                    if (!refresh) {
                        refreshSuiteCacheInner(this.testDir);
                        refresh = true;
                    }
                }
            }
        }
    }

    private void refreshSuiteCacheInner(File dir) throws IOException {
        if (!dir.isDirectory()) {
            throw new IOException("only directory is allow");
        }

        if (isFinishedSuiteDir(dir)) {
            suitesCache.put(dir.getName(), new SuiteContext(dir));
        } else {
            File[] files = dir.listFiles();
            if (files != null) {
                for (File subFile : files) {
                    if (subFile.isDirectory()) {
                        refreshSuiteCacheInner(subFile);
                    }
                }
            }
        }
    }

    private SuiteName parseSuiteName(String suiteName) throws YatAccessError {
        String[] split = suiteName.split("/");
        if (split.length == 1) {
            return new SuiteName(suiteName);
        } else if (split.length == 2) {
            return new SuiteName(split[0], split[1]);
        } else {
            throw new YatAccessError("suite name $suiteName is invalid");
        }
    }

    private static class SuiteContext {
        YatContext context = new YatContext();
        File path;

        public SuiteContext(File path) {
            this.path = path;
            context.load("", new Command(path));
        }
    }

    @Data
    private static class SuiteName {
        private String suiteName;
        private String subSuiteName;

        SuiteName(String suiteName) {
            this(suiteName, "");
        }

        SuiteName(String suiteName, String subSuiteName) {
            this.suiteName = suiteName;
            this.subSuiteName = subSuiteName;
        }
    }
}

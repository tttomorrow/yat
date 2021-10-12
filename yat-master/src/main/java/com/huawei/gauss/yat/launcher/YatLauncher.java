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

package com.huawei.gauss.yat.launcher;

import org.springframework.boot.loader.ExecutableArchiveLauncher;
import org.springframework.boot.loader.archive.Archive;
import org.springframework.boot.loader.archive.ExplodedArchive;

import java.io.File;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

public class YatLauncher extends ExecutableArchiveLauncher {
    private final static String YAT_INF_CLASSES = "YAT-INF/classes/";
    private final static String YAT_INF_LIB = "YAT-INF/lib/";

    private final List<File> libPaths;

    private YatLauncher(List<File> libPaths) {
        this.libPaths = libPaths;
    }

    @Override
    protected boolean isNestedArchive(Archive.Entry entry) {
        if (entry.isDirectory()) {
            return entry.getName().equals(YAT_INF_CLASSES);
        }
        return entry.getName().startsWith(YAT_INF_LIB) && entry.getName().endsWith(".jar");
    }

    @Override
    protected Iterator<Archive> getClassPathArchivesIterator() throws Exception {
        Archive jarArchive = createArchive();

        List<Iterator<Archive>> iterators = new LinkedList<>();

        iterators.add(jarArchive.getNestedArchives(this::isNestedArchive, null));

        for (File path: libPaths) {
            iterators.add(new ExplodedArchive(path).getNestedArchives(this::isNested, null));
        }

        return new Iterator<Archive>() {
            private final Iterator<Iterator<Archive>> iteratorIterator = iterators.iterator();
            private Iterator<Archive> current = iteratorIterator.next();

            @Override
            public boolean hasNext() {
                if (current.hasNext()) {
                    return true;
                } else {
                    if (iteratorIterator.hasNext()) {
                        current = iteratorIterator.next();
                        return current.hasNext();
                    } else {
                        return false;
                    }
                }
            }

            @Override
            public Archive next() {
                return current.next();
            }
        };
    }

    private boolean isNested(Archive.Entry entry) {
        return !entry.isDirectory() && entry.getName().endsWith(".jar");
    }

    public static void main(String[] args) throws Exception {
        List<File> libpaths = new ArrayList<>();

        String yatHome = System.getenv("YAT_HOME");
        if (yatHome == null) {
            System.err.println("You must set $YAT_HOME env value to specific the yat home directory");
            System.exit(1);
        }
        addLibPath(libpaths, Paths.get(yatHome, "lib").toFile());
        final String testDir = searchParamValue(args, "-d", "--test-dir");
        final File testDirLib;
        if (testDir == null) {
            testDirLib = new File("lib");
        } else {
            testDirLib = Paths.get(testDir, "lib").toFile();
        }
        addLibPath(libpaths, testDirLib);

        String classPath = searchParamValue(args, "--lib-path");
        if (classPath == null) {
            classPath = System.getenv("YAT_LIB_PATH");
        }
        if (classPath != null) {
            addLibPath(libpaths,  new File(classPath));
        }

        new YatLauncher(libpaths).launch(args);
    }

    private static void addLibPath(List<File> libPaths, File path) {
        if (path.exists()) {
            libPaths.add(path);
        }
    }

    private static String searchParamValue(String[] args, String ... opts) {
        for (int i = 0; i < args.length; ++i) {
            String arg = args[i];
            for (String opt : opts) {
                if (opt.equals(arg)) {
                    return args[i + 1];
                }
            }
        }
        return null;
    }

}

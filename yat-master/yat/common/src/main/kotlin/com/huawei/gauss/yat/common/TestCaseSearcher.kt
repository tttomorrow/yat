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

package com.huawei.gauss.yat.common

import java.io.File
import java.nio.file.Paths

class TestCaseSearcher(private val testcaseDir: File, private val expectDir: File) {
    companion object {
        private const val MULTI_EXPECT_LIMIT = 16

        // type to suffix
        private val typeSuffixMapper = mapOf(
            Pair(Type.SQL, ".sql"),
            Pair(Type.UNIT_SQL, ".u.sql"),
            Pair(Type.RANDOM_SQL, ".r.sql"),
            Pair(Type.G_SQL, ".g.sql"),
            Pair(Type.CBO_SQL, ".cbo.sql"),
            Pair(Type.Z_SQL, ".z.sql"),
            Pair(Type.IZ_SQL, ".iz.sql"),
            Pair(Type.SHELL, ".sh"),
            Pair(Type.UNIT_GROOVY, ".groovy"),
            Pair(Type.UNIT_PYTHON, ".py"),
            Pair(Type.PYTHON, ".r.py"),
            Pair(Type.GO, ".go"),
            Pair(Type.CBO_SPIDER, ".cbo.g"),
            Pair(Type.SPOCK, ".spec.groovy")
        )

        private val suffixMapper = mutableMapOf<String, Type>()

        init {
            // value to key mapper
            for (map in typeSuffixMapper) {
                suffixMapper[map.value] = map.key;
            }
        }

        // type to type-name
        private val typeNameMapper = mapOf(
            Pair(Type.UNIT_SQL, "unit_sql"),
            Pair(Type.SQL, "sql"),
            Pair(Type.RANDOM_SQL, "parallel_sql"),
            Pair(Type.Z_SQL, "zsql"),
            Pair(Type.IZ_SQL, "interactive_zsql"),
            Pair(Type.SHELL, "shell"),
            Pair(Type.UNIT_GROOVY, "unit_groovy"),
            Pair(Type.UNIT_PYTHON, "unit_python"),
            Pair(Type.PYTHON, "python"),
            Pair(Type.GO, "go"),
            Pair(Type.G_SQL, "gsql"),
            Pair(Type.CBO_SQL, "cbo_sql"),
            Pair(Type.CBO_SPIDER, "cbo_spider"),
            Pair(Type.SPOCK, "unit_spock")
        )
    }

    enum class Type {
        UNIT_SQL, RANDOM_SQL, SQL, CBO_SQL, Z_SQL,
        G_SQL, CBO_SPIDER, IZ_SQL, SHELL, UNIT_GROOVY,
        PYTHON, UNIT_PYTHON, GO, SPOCK;

        fun typeName(): String {
            return typeNameMapper[this] ?: error("found unexpect type $this")
        }

        fun suffixName(): String {
            return typeSuffixMapper[this] ?: error("found unexpect type $this")
        }
    }

    data class TestCase(val case: File, val type: Type)

    fun searchCase(caseName: String): TestCase {
        suffixMapper.forEach { (ext, type) ->
            val realFile = searchFile(testcaseDir, caseName, ext)
            if (realFile != null) {
                return TestCase(realFile, type)
            }
        }

        throw YatRuntimeError("can not found test case file with case name $caseName")
    }

    private fun searchFile(path: File, caseName: String, ext: String): File? {
        val file = Paths.get(path.toString(), "$caseName$ext").toFile()
        return if (file.exists()) {
            file
        } else {
            null
        }
    }

    fun searchExpect(caseName: String, subSuite: String = "", ext: String = ""): List<File> {
        val res = mutableListOf<File>()
        val defaultExpect = Paths.get(expectDir.toString(), subSuite, "$caseName$ext").toFile()
        res.add(defaultExpect)

        (1..MULTI_EXPECT_LIMIT).forEach {
            val multiExpect = Paths.get(expectDir.toString(), subSuite, "${caseName}_$it$ext").toFile()
            if (multiExpect.exists()) {
                res.add(multiExpect)
            }
        }

        return res
    }
}
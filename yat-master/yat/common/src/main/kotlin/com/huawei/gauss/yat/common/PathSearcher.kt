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
import java.nio.file.Path
import java.nio.file.Paths

class PathSearcher {
    private val paths = mutableListOf<String>()

    constructor()
    constructor(vararg paths: String) {
        this.paths.addAll(paths)
    }

    constructor(vararg paths: Path) {
        paths.forEach {
            addSearchPath(it)
        }
    }

    constructor(paths: List<String>) {
        this.paths.addAll(paths)
    }

    fun addSearchPath(path: String) {
        paths.add(path)
    }

    fun addSearchPath(path: Path) {
        paths.add(path.toString())
    }

    fun search(name: String): File? {
        val thePath = Paths.get(name)
        if (thePath.isAbsolute) {
            return if (thePath.toFile().exists()) {
                thePath.toFile()
            } else {
                null
            }
        }

        for (path in paths) {
            val res = Paths.get(path, name).toFile()
            if (res.exists()) {
                return res
            }
        }

        return null
    }

    fun search(vararg names: String): File? {
        for (name in names) {
            val path = search(name)
            if (path != null) {
                return path
            }
        }
        return null
    }
}
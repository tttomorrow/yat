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
 
package com.huawei.gauss.yat.diff

class DifferHandler<T> {
    private val filters = mutableListOf<DiffFilter<T>>()

    fun registerFilter(filter: (T) -> Boolean) {
        filters.add(object : DiffFilter<T> {
            override fun filter(line: T): Boolean {
                return filter(line)
            }
        })
    }

    private fun filter(list: List<T>): List<T> {
        val res = mutableListOf<T>()
        list.forEach { line ->
            var keep = true
            filters.forEach { filter ->
                keep = keep && filter.filter(line)
            }
            if (keep) {
                res.add(line)
            }
        }

        return res
    }

    fun handle(list: List<T>): List<T> {
        return filter(list)
    }
}

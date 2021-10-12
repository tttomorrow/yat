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

import java.util.concurrent.atomic.AtomicLong

class Statistics {
    private var testAll = AtomicLong(0)
    private var testSuccess = AtomicLong(0)

    fun incAll() {
        testAll.incrementAndGet()
    }

    fun incSuccess() {
        testSuccess.incrementAndGet()
    }

    fun allCount(): Long {
        return testAll.get()
    }

    fun successCount(): Long {
        return testSuccess.get()
    }
}


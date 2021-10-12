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

package com.huawei.gauss.yat.scheduler.parser

import com.huawei.gauss.yat.common.lex.Position

class ScheduleSyntaxError : Exception {
    constructor(msg: String, position: Position) :
            super("*** Syntax error: $msg, at line ${position.line} column ${position.column}")

    constructor(msg: String, line: Int, column: Int) :
            super("*** Syntax error: $msg, at line $line column $column")

    constructor(msg: String) :
            super("*** Syntax error: $msg")
}

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

package com.huawei.gauss.yat.sql.parser

import com.huawei.gauss.yat.common.lex.Position

class SqlLexError : Exception {
    constructor(msg: String, line: Int, col: Int) : super("[$line:$col] $msg")
    constructor(msg: String, position: Position) : super("[${position.line}:${position.column}] $msg")
    constructor(msg: String, cause: Throwable, line: Int, col: Int) : super("[$line:$col]$msg", cause)

}
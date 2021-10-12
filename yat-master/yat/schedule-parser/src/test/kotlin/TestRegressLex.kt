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

import com.huawei.gauss.yat.scheduler.parser.regress.RegressLex
import org.junit.Test
import java.io.StringReader

class TestRegressLex {
    companion object {
        private val regress = """
            value: xml-test
            macro: key value
            macro: key value
            setup: setup(valid: false diff= true)
            group: abc abc2 abc3
                abc4
                abc5
                abc6
            group: 
                bbc1
                bbc
                bbc4
            import: '../../abc.schd'
            cleanup: cleanup_001
            ------
            value: xml-test
            macro: key value
            macro: key value
            setup: setup(valid: false diff= true)
            group: abc abc2 abc3
                abc4
                abc5
                abc6
            group: 
                bbc1
                bbc
                bbc4
            cleanup: cleanup_001
        """
    }

    @Test
    fun testLex() {
        val lexer = RegressLex(StringReader(regress))
        while (lexer.hasNext()) {
            println(lexer.nextToken())
        }
    }
}
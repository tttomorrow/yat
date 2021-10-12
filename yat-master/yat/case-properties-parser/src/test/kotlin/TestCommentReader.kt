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
 
import com.huawei.gauss.yat.case.properties.parser.CommentReader
import org.junit.Test
import java.io.StringReader


class TestCommentReader {
    @Test
    fun testReader() {
        CommentReader(StringReader("""
            # test step 1
            select * from gcc where id > ?;
            -- comment 2
            -- comment 3
            --
            /* xml */
            /* */
            /**/
            #
            /**/
            #
            
            /*
             * xml support
             * - list
             * - list of list
             */
            create or replace function(a: int, b: int) as
            
            ''''''
            '''inner'''
            begin
                i = 10 - 10;
                b = 10 * 10;
            end;
            /
        """.trimIndent()), arrayListOf("//", "#", "--"), arrayListOf(Pair("/*", "*/"), Pair("'''", "'''"))).parse()
    }
}
"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
"""
Case Type   : 功能测试
Case Name   : SYSTEM：事务中重建数据库上所有系统表的索引
Description :
    1. 事务中重建数据库上所有系统表的索引
Expect      :
    1. 合理报错，不支持
History     : 
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('''---Opengauss_Function_DDL_Index_Case0198开始---''')

    def test_copy(self):
        cmd0 = """select CURRENT_CATALOG;"""
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('ERROR') == -1)
        dbname = msg0.split('\n')[-2].strip()

        cmd1 = f'''explain performance select * from pg_proc where 
            oid = (select oid from pg_class where relname = 'pg_proc');
            begin;
            REINDEX SYSTEM {dbname};
            end;
            explain performance select * from pg_proc where 
            oid = (select oid from pg_class where relname = 'pg_proc');
            '''
        info = 'ERROR:  REINDEX DATABASE cannot run inside a transaction block'
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue(msg1.find(info) > -1)

    def tearDown(self):
        self.log.info('''---Opengauss_Function_DDL_Index_Case0198结束---''')
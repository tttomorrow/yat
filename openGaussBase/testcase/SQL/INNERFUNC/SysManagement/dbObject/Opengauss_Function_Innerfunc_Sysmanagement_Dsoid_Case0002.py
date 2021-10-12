"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Name   : pg_database_size(oid)函数参数类型及个数校验，合理报错
Description :
    1.空值
    2.非法值
    3.多参、少参
Expect      :
    1.返回空
    2.合理报错
    3.合理报错
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info("""
        ---Opengauss_Function_Innerfunc_Sysmanagement_Dsoid_Case0002开始---""")

    def test_dbsize(self):

        self.log.info("""------------入参为空值、非法值--------------------""")
        cmd0 = f"""select pg_database_size('') from pg_database a 
                  where a.datname = current_catalog;
                  select pg_database_size(null) from pg_database a 
                  where a.datname = current_catalog;"""
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.assertTrue(msg0.splitlines()[2].strip() == '')
        self.assertTrue(msg0.splitlines()[-2].strip() == '')

        error = ['你好', 'nodatabasename', '987654', 'False', 'Ture']
        for i in range(5):
            cmd = f"""select pg_database_size('{error[i]}') from pg_database a 
                    where a.datname = current_catalog;"""
            msg = self.commonsh.execut_db_sql(cmd)
            self.log.info(msg)
            self.assertTrue('ERROR' in msg)

        self.log.info("""----------------校验多参、少参--------------------""")
        cmd1 = """select pg_database_size();
                select pg_database_size(a.oid,a.oid) from pg_database a 
                where a.datname = current_catalog;"""
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue('ERROR' in msg1 and 'No function matches' in msg1)

    def tearDown(self):
        db_drop = f"""drop database if exists new cascade;"""
        self.commonsh.execut_db_sql(db_drop)
        self.log.info("""
        ---Opengauss_Function_Innerfunc_Sysmanagement_Dsoid_Case0002结束---""")

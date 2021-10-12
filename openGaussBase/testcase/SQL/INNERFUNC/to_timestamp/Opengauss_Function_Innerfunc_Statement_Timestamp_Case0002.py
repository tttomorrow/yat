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
Case Name   : 创建与系统函数statement_timestamp同名自定义函数,
              分别加用户名与不加用户名调用
Description :
    1.创建与系统函数statement_timestamp同名自定义函数
    2.带用户名和不带用户名去调用
Expect      :
    1.函数返回结果正确
    2.内置函数返回当前时间戳，自定义函数返回1314
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.user = Node('dbuser')
        self.commonsh = CommonSH('dbuser')
        self.log.info('''
        ---Opengauss_Function_Innerfunc_Statement_Timestamp_Case0002开始---''')

    def test_timestamp(self):

        cmd = f'''drop function if exists Johnson.statement_timestamp;
                drop user if exists Johnson cascade;
                create user Johnson identified by '{macro.COMMON_PASSWD}';
                create or replace function Johnson.statement_timestamp( x int )
                return int
                as
                begin
                    return 1314;
                end;'''
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        self.assertTrue('CREATE FUNCTION' in msg)
        # 测试点1：不带用户名调用
        now = self.user.sh('date "+%Y-%m-%d %H:%M:%S"').result()
        cmd1 = 'select statement_timestamp();'
        msg = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg)
        db_time = msg.splitlines()[2].strip()  # 2021-01-14 19:26:15.265936+08
        self.assertTrue(len(db_time) > 23)
        cmd2 = f"select '{now}'::timestamp - '{db_time}'::timestamp;"
        msg2 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg2)
        diff = msg2.splitlines()[-2].strip().strip('-')
        self.assertTrue(diff[:5] == '00:00')
        self.assertTrue(db_time[-3:] == '+08')
        # 测试点2：带用户名调用
        cmd3 = 'select Johnson.statement_timestamp(11);'
        msg3 = self.commonsh.execut_db_sql(cmd3)
        self.log.info(msg3)
        self.assertTrue(msg3.splitlines()[2].strip() == '1314')

    def tearDown(self):
        cmd = f'''drop function if exists Johnson.statement_timestamp;
                  drop user if exists Johnson cascade;'''
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        self.log.info('''
        ---Opengauss_Function_Innerfunc_Statement_Timestamp_Case0002结束---''')
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
Case Name   : 使用pgxc_is_committed(transaction_id)函数获取事务状态
Description :
    1. 分别在事务外、事务回滚以及提交后进行查询
    2. 函数错误调用
Expect      :
    1. 返回正确的事务是否提交状态信息
    2. 入参错误时返回空，多参少参返回error
"""
import time
import unittest

from yat.test import Node

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.user = Node('dbuser')
        self.log.info('''---
            Opengauss_Function_Innerfunc_Pgxc_Is_Committed_Case0001开始---''')

    def test_pgxc(self):
        self.log.info('------获取当前事务oid，传入pgxc_is_committed函数------')
        cmd0 = '''select txid_current();'''
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        oid0 = msg0.splitlines()[2].strip()
        cmd1 = f'''select pgxc_is_committed('{oid0}');'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue(msg1.splitlines()[2].strip() == 't')

        xact = ['rollback;', 'end;']
        res = ['f', 't']
        for i in range(2):
            cmd2 = f"""begin;
                       select txid_current();
                       {xact[i]}"""
            msg2 = self.commonsh.execut_db_sql(cmd2)
            self.log.info(msg2)
            oid2 = msg2.splitlines()[3].strip()
            cmd3 = f'''select pgxc_is_committed('{oid2}');'''
            msg3 = self.commonsh.execut_db_sql(cmd3)
            self.log.info(msg3)
            self.assertTrue(msg3.splitlines()[2].strip() == res[i])

        self.log.info('------------异常校验，部分测试点合理报错------------')
        time.sleep(3)
        sql_cmd = '''select pgxc_is_committed('hey');'''
        self.log.info(sql_cmd)
        msg4 = self.commonsh.execut_db_sql(sql_cmd)
        self.log.info(msg4)
        sql_result_list = msg4.splitlines()
        self.log.info(sql_result_list)
        self.log.info(len(msg4.splitlines()[2].strip()))
        self.assertEqual(len(msg4.splitlines()[2].strip()), 0)
        sql_cmd = '''select pgxc_is_committed('987654','987654');'''
        self.log.info(sql_cmd)
        msg4 = self.commonsh.execut_db_sql(sql_cmd)
        self.log.info(msg4)
        self.assertIn('ERROR', msg4)
        sql_cmd = '''select pgxc_is_committed();'''
        self.log.info(sql_cmd)
        msg4 = self.commonsh.execut_db_sql(sql_cmd)
        self.log.info(msg4)
        self.assertIn('ERROR', msg4)

    def tearDown(self):
        self.log.info('''---
            Opengauss_Function_Innerfunc_Pgxc_Is_Committed_Case0001结束---''')

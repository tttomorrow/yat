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
Case Name   : 使用txid_current函数获取当前事务ID
Description :
    1. 分别在事务内外进行获取
    2. 函数错误调用
Expect      :
    1. 返回不同的bigint类型值
    2. 合理报错
History     : 
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('Opengauss_Function_Innerfunc_Txid_Current_Case0001开始')

    def test_txid(self):
        func = ['select txid_current();',
                "select txid_current('current'); select txid_current;"]

        self.log.info('-------------直接查询-------------')
        msg0 = self.commonsh.execut_db_sql(func[0])
        self.log.info(msg0)
        id0 = int(msg0.splitlines()[-2].strip())
        self.assertTrue(0 < id0 < 9223372036854775807)
        self.log.info('-------------事务内查询-------------')
        cmd1 = '''begin;
                  select txid_current();
                  end;
                  '''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        id1 = int(msg1.splitlines()[3].strip())
        self.assertTrue(0 < id1 < 9223372036854775807)
        self.log.info('-------------事务外查询-------------')
        msg2 = self.commonsh.execut_db_sql(func[0])
        self.log.info(msg2)
        id2 = int(msg2.splitlines()[-2].strip())
        self.assertTrue(0 < id2 < 9223372036854775807)
        self.assertTrue(id0 < id1 < id2)

        self.log.info('-------------错误调用-------------')
        msg3 = self.commonsh.execut_db_sql(func[1])
        self.log.info(msg3)
        self.assertTrue(msg3.count('ERROR') == 2)

    def tearDown(self):
        self.log.info('Opengauss_Function_Innerfunc_Txid_Current_Case0001结束')
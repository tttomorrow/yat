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
Case Name   : 使用txid_current_snapshot函数获取当前快照
Description :
    1. 开启事务，并在事务内外对txid_snapshot进行获取
    2. 函数错误调用
Expect      :
    1. 随事务递增返回正确的xmin:xmax:xip_list
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
        self.log.info('''
            Opengauss_Function_Innerfunc_Txid_Current_Snapshot_Case0001开始''')

    def test_txid(self):
        self.log.info('-------------直接查询，获取txid_snapshot-------------')
        cmd0 = 'select txid_current_snapshot();'
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        txid_snapshot = msg0.splitlines()[2].strip()
        xmin, xmax = txid_snapshot.split(':')[0], txid_snapshot.split(':')[1]
        self.assertTrue(int(xmin) <= int(xmax))

        cmd1 = '''select txid_current_snapshot();
                  drop table if exists hong;
                  create table hong(id int);
                  insert into hong values(99);
                  select txid_current_snapshot();
                  begin;
                  update hong set id = 89 where id = 99;
                  drop table hong;
                  select txid_current_snapshot();
                  end;
                  select txid_current_snapshot();
                  '''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)

        self.log.info('-------------错误调用-------------')
        cmd2 = '''select txid_current_snapshot('current'); 
            select txid_current_snapshot;
            '''
        msg3 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg3)
        self.assertTrue(msg3.count('ERROR') == 2)

    def tearDown(self):
        self.log.info('''
            Opengauss_Function_Innerfunc_Txid_Current_Snapshot_Case0001结束''')

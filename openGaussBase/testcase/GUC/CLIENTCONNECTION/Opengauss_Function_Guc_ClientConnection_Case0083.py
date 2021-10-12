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
Case Type   : GUC
Case Name   : 使用gs_guc reload方法设置参数statement_timeout为5ms,插入2000万条
            数据，合理报错
Description :
        1.建表
        2.修改参数值为5ms
        3.插入2000万条数据
        4.恢复参数默认值
Expect      :
        1.建表成功
        2.设置成功，显示5ms
        3.合理报错ERROR:  canceling statement due to statement timeout
        4.默认值恢复成功
"""
import re
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0083start------')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_statement_timeout(self):
        self.log.info('--步骤1:建表--')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists test083 
            cascade;
            create table test083(id int);''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.log.info('--步骤2:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('''show statement_timeout;''')
        self.log.info(sql_cmd)
        self.assertIn('0', sql_cmd)
        self.log.info('--步骤3:设置参数值为5ms--')
        msg = self.commonsh.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          'statement_timeout =5')
        self.log.info(msg)
        self.assertTrue(msg)
        self.log.info('--步骤4:插入2000万数据,报错--')
        sql_cmd = self.commonsh.execut_db_sql('''insert into test083 
            values(generate_series(1,20000000));''')
        self.log.info(sql_cmd)
        assert_msg = re.search(
            r'ERROR:(.*)canceling statement due to statement timeout', sql_cmd,
            re.I | re.S)
        self.assertTrue(assert_msg)

    def tearDown(self):
        self.log.info('--步骤4:清理环境--')
        msg = self.commonsh.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f'statement_timeout=0')
        self.log.info(msg)
        sql_cmd = self.commonsh.execut_db_sql('''show statement_timeout;''')
        self.log.info(sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists test083 
                   cascade;''')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0083执行完成----')

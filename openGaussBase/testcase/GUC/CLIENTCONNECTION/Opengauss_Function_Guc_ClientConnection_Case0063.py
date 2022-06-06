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
Case Type   : GUC
Case Name   : 使用gs_guc reload方法设置参数default_transaction_read_only为on,建表，合理报错
Description :
        1.查询default_transaction_read_only默认值
        2.修改参数值为on
        3.建表验证
        4.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.设置成功
        3.合理报错
        4.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0063start----')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.expect_res = 'ERROR:  cannot execute CREATE TABLE in a' \
                          ' read-only transaction'

    def test_default_transaction_read_only(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('''show
            default_transaction_read_only;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('--步骤2:设置设置参数值为on--')
        msg = self.commonsh.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          'default_transaction_read_only = on')
        self.log.info(msg)
        self.assertTrue(msg)
        self.log.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = self.commonsh.execut_db_sql('''show 
            default_transaction_read_only;''')
        self.log.info(sql_cmd)
        self.assertIn('on', sql_cmd)
        self.log.info('--步骤4: 建表，报错--')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists test_063;
            create table test_063(id int);''')
        self.log.info(sql_cmd)
        self.assertIn(self.expect_res, sql_cmd)

    def tearDown(self):
        self.log.info('--步骤5:清理环境--')
        sql_cmd = self.commonsh.execut_db_sql('''show 
            default_transaction_read_only;''')
        self.log.info(sql_cmd)
        current_value = sql_cmd.splitlines()[-2].strip()
        self.log.info(current_value)
        self.log.info(str(type(self.res)) + " : " + self.res)
        if self.res != current_value:
            msg = self.commonsh.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"default_transaction_read_only"
                                              f"= '{self.res}'")
            self.log.info(msg)
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0063执行完成--')

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
Case Name   : 使用gs_guc reload方法设置参数vacuum_freeze_table_age为10000 ,观察预期结果
Description :
        1.查询vacuum_freeze_table_age默认值
        2.修改参数值为10000
        3.恢复参数默认值
Expect      :
        2.设置成功
        3.默认值恢复成功
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
            '----Opengauss_Function_Guc_ClientConnection_Case0093start-----')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_vacuum_freeze_table_age(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show vacuum_freeze_table_age;')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('--步骤2:设置参数为10000--')
        msg = self.commonsh.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          'vacuum_freeze_table_age = 10000')
        self.log.info(msg)
        self.assertTrue(msg)
        self.log.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = self.commonsh.execut_db_sql('show vacuum_freeze_table_age;')
        self.log.info(sql_cmd)
        self.assertIn('10000', sql_cmd)

    def tearDown(self):
        self.log.info('--步骤4:恢复默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show vacuum_freeze_table_age;')
        self.log.info(sql_cmd)
        if self.res not in sql_cmd:
            msg = self.commonsh.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f'''vacuum_freeze_table_age
                                              ={self.res}''')
            self.log.info(msg)
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0093执行完成--')

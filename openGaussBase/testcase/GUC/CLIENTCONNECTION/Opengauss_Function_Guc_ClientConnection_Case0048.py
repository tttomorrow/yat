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
Case Name   : 使用gs_guc reload方法设置参数check_function_bodies为off,观察预期结果
Description :
        1.查询check_function_bodies默认值
        2.修改参数值为off
        3.创建函数，函数无参数，返回值有参数
        4.恢复参数默认值
Expect      :
        1.显示默认值为on
        2.设置成功
        3.创建成功
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
            '---Opengauss_Function_Guc_ClientConnection_Case0048start----')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_check_function_bodies(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show check_function_bodies;')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('--步骤2:设置设置参数值为off--')
        msg = self.commonsh.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          'check_function_bodies=off')
        self.log.info(msg)
        self.assertTrue(msg)
        self.log.info('--步骤3:查询该参数修改后的值--')
        sql_cmd = self.commonsh.execut_db_sql('show check_function_bodies;')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        self.log.info('--步骤4:创建函数--')
        sql_cmd = self.commonsh.execut_db_sql('''create or replace 
            function bad048() returns void language sql as 'select \$1';''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, sql_cmd)

    def tearDown(self):
        self.log.info('--步骤4:清理环境--')
        sql_cmd = self.commonsh.execut_db_sql('''drop function bad048;''')
        self.log.info(sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql('show check_function_bodies;')
        self.log.info(sql_cmd)
        current_value = sql_cmd.splitlines()[-2].strip()
        self.log.info(current_value)
        self.log.info(str(type(self.res)) + " : " + self.res)
        if self.res != current_value:
            msg = self.commonsh.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f'check_function_bodies'
                                              f'={self.res}')
            self.log.info(msg)
        self.log.info(
            '-----Opengauss_Function_Guc_ClientConnection_Case0048执行完成----')

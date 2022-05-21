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
Case Name   : 使用gs_guc reload方法设置参数lc_monetary为en_US ,观察预期结果
Description :
        1.查询lc_monetary默认值
        2.修改参数值为en_US并使用查询
        3恢复参数默认值
Expect      :
        1.显示默认值为C
        2.设置成功;查询显示美元符号
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
            '----Opengauss_Function_Guc_ClientConnection_Case0151start----')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_lc_monetary(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('''show lc_monetary;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('--步骤2:修改参数值为en_US--')
        msg = self.commonsh.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          "lc_monetary = 'en_US'")
        self.log.info(msg)
        self.assertTrue(msg)
        self.log.info('--步骤3:查询参数值并查询货币类型显示格式--')
        sql_cmd = self.commonsh.execut_db_sql('''show lc_monetary;
            SELECT 12.13::money;
            ''')
        self.log.info(sql_cmd)
        self.assertIn('en_US', sql_cmd)
        self.assertIn('$12.13', sql_cmd)

    def tearDown(self):
        self.log.info('--步骤4:清理环境--')
        sql_cmd = self.commonsh.execut_db_sql('''show lc_monetary;''')
        self.log.info(sql_cmd)
        if self.res not in sql_cmd:
            msg = self.commonsh.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"lc_monetary='{self.res}'")
            self.log.info(msg)
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0151执行完成---')

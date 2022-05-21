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
Case Name   : 使用gs_guc reload方法设置参数DateStyle输入输出的年/月/日顺序(YMD) ,观察预期结果
Description :
        1.查询DateStyle默认值
        2.修改参数值为YMD并查询当前日期
        3.恢复参数默认值
Expect      :
        1.显示默认值为 ISO, MDY
        2.设置成功查询当前日期显示顺序为YMD
        3.默认值恢复成功
History     :
"""
import unittest
import time

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0125start-----')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_DateStyle(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql(f'''show DateStyle;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('--步骤2:设置参数值为YMD输出顺序--')
        msg = self.commonsh.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          "DateStyle = 'YMD'")
        self.log.info(msg)
        self.assertTrue(msg)
        self.log.info('--步骤3:查询修改后的参数值--')
        sql_cmd = self.commonsh.execut_db_sql('''show DateStyle;''')
        self.log.info(sql_cmd)
        self.assertIn('ISO, YMD', sql_cmd)
        self.log.info('--步骤4:查询当前日期--')
        sql_cmd = self.commonsh.execut_db_sql('''select current_date;''')
        self.log.info(sql_cmd)
        create_date = time.strftime("%Y-%m-%d", time.localtime())
        self.log.info(create_date)
        self.assertTrue(sql_cmd.splitlines()[-2].strip() == create_date)

    def tearDown(self):
        self.log.info('--步骤4:清理环境--')
        sql_cmd = self.commonsh.execut_db_sql(f'''show DateStyle;''')
        self.log.info(sql_cmd)
        if self.res not in sql_cmd:
            msg = self.commonsh.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"DateStyle='{self.res}'")
            self.log.info(msg)
        self.log.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0125执行完成---')

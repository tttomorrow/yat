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
Case Name   : 使用gs_guc reload方法设置参数TimeZone为Australia/South ,
              观察预期结果
Description :
        1.查询TimeZone默认值
        2.修改参数值为Australia/South
        3.查询当前时间
        4.清理环境
Expect      :
        1.显示默认值为PRC
        2.设置成功当前时间为北京时间
        3.时区修改成功，和系统表pg_timezone_names相对于UTC的偏移量一致
        4.清理环境完成
             故Australia/South时区的偏移量会变化
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-----Opengauss_Function_Guc_ClientConnection_Case0131start---')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_TimeZone(self):
        text = '--步骤1:查看默认值;expect:默认值为PRC--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql('''show TimeZone;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        text = '--步骤2:修改参数值为Australia/South;expect:修改成功--'
        self.log.info(text)
        msg = self.commonsh.execute_gsguc('reload',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          "TimeZone = 'Australia/South'")
        self.log.info(msg)
        self.assertTrue(msg)
        text = '--步骤3:查询修改后的参数值;expect:时区修改成功，和系统表' \
               'pg_timezone_names相对于UTC的偏移量一致--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql('''show TimeZone;''')
        self.log.info(sql_cmd)
        self.assertIn('Australia/South', sql_cmd, '执行失败:' + text)
        sql_cmd = self.commonsh.execut_db_sql('''select now();''')
        self.log.info(sql_cmd)
        msg1 = sql_cmd.splitlines()[-2].strip()
        self.log.info(msg1)
        res1 = msg1.split('+')[-1]
        self.log.info(res1)
        sql_cmd = self.commonsh.execut_db_sql('''select * from  \
            pg_timezone_names where name= 'Australia/South';''')
        self.log.info(sql_cmd)
        msg2 = sql_cmd.splitlines()[-2].strip()
        self.log.info(msg2)
        res2 = msg2.split('|')[-2].strip().replace(':00', '')
        self.log.info(res2)
        self.assertEqual(res1, res2, '执行失败:' + text)

    def tearDown(self):
        text = '--步骤4:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql('''show TimeZone;''')
        self.log.info(sql_cmd)
        if self.res not in sql_cmd.splitlines()[-2].strip():
            msg = self.commonsh.execute_gsguc('reload',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"TimeZone='{self.res}'")
            self.log.info(msg)
        self.log.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0131执行完成--')

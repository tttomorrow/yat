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
Case Name   : 使用gs_guc set方法设置参数IntervalStyle为无效值,合理报错
Description :
        1.查询IntervalStyle默认值
        2.依次修改参数值为123，test，空串
        3.恢复参数默认值
Expect      :
        1.显示默认值为postgres
        2.合理报错
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
            '---Opengauss_Function_Guc_ClientConnection_Case0237start-----')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')

    def test_intervalstyle(self):
        self.log.info('--步骤一：查询参数默认值--')
        sql_cmd = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           "IntervalStyle=postgres")
        self.log.info(sql_cmd)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.pri_sh.execut_db_sql('show IntervalStyle;')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('--步骤二：修改参数值依次为123，test，空串，合理报错--')
        invalid_value = [123, 'test', "''"]
        for i in invalid_value:
            result = self.pri_sh.execute_gsguc("set",
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"IntervalStyle={i}")
            self.assertFalse(result)

    def tearDown(self):
        self.log.info('--步骤三：恢复参数默认值--')
        sql_cmd = self.pri_sh.execut_db_sql('show IntervalStyle;')
        self.log.info(sql_cmd)
        if self.res != sql_cmd.split("\n")[-2].strip():
            msg = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           "IntervalStyle=postgres")
            self.log.info(msg)
            msg = self.pri_sh.restart_db_cluster()
            self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.pri_sh.execut_db_sql('show IntervalStyle;')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0237执行完成----')

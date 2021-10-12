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
Case Name   : 使用gs_guc reload方法设置参数lockwait_timeout为1 ,观察预期结果
Description :
        1.查询lockwait_timeout默认值
        2.修改参数值为1
        3.恢复参数默认值
Expect      :
        1.显示默认值为20min
        2.设置成功,显示1ms
        3.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0175start-----')
        self.constant = Constant()

    def test_lockwait_timeout(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show lockwait_timeout;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:修改参数值为1--')
        msg = commonsh.execute_gsguc('reload',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'lockwait_timeout = 1')
        LOG.info(msg)
        self.assertTrue(msg)
        LOG.info('--步骤3:查看修改后的参数值--')
        sql_cmd = commonsh.execut_db_sql('show lockwait_timeout;')
        LOG.info(sql_cmd)
        self.assertIn('1ms', sql_cmd)

    def tearDown(self):
        LOG.info('--步骤4:恢复默认值--')
        msg = commonsh.execute_gsguc('reload',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"lockwait_timeout='{self.res}'")
        LOG.info(msg)
        LOG.info(
            '--Opengauss_Function_Guc_ClientConnection_Case0175执行完成----')

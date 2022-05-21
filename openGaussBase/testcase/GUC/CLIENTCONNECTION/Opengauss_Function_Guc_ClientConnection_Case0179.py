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
Case Name   : 使用gs_guc set方法设置参数lockwait_timeout为无效值，合理报错
Description :
        1.查询lockwait_timeout默认值
        2.修改参数值为test
        3.修改参数值为-1
        4.修改参数值为123.859
        5.修改参数值为2147483648
        6.修改参数值为空串
        7.恢复参数默认值
Expect      :
        1.显示默认值为20min
        2.合理报错
        3.合理报错
        4.合理报错
        5.合理报错
        6.合理报错
        7.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro

LOG = Logger()
commonsh = CommonSH('dbuser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '--Opengauss_Function_Guc_ClientConnection_Case0168start-----')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_lockwait_timeout(self):
        # 查询默认值
        sql_cmd = commonsh.execut_db_sql('show lockwait_timeout;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 设置参数为test
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                    'lockwait_timeout =test')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql('show lockwait_timeout;')
        LOG.info(sql_cmd)
        self.assertIn('20min', sql_cmd)
        # 设置参数为-1
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                    'lockwait_timeout = -1')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql('show lockwait_timeout;')
        LOG.info(sql_cmd)
        self.assertIn('20min', sql_cmd)
        # 设置参数为123.859
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                    'lockwait_timeout = 123.859')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql('show lockwait_timeout;')
        LOG.info(sql_cmd)
        self.assertIn('20min', sql_cmd)
        # 设置参数为2147483648
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                    'lockwait_timeout = 2147483648')
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql('show lockwait_timeout;')
        LOG.info(sql_cmd)
        self.assertIn('20min', sql_cmd)
        # 设置参数为空串
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                    "lockwait_timeout = ''")
        LOG.info(msg)
        self.assertFalse(msg)
        # 查询
        sql_cmd = commonsh.execut_db_sql('show lockwait_timeout;')
        LOG.info(sql_cmd)
        self.assertIn('20min', sql_cmd)

    def tearDown(self):
        LOG.info('----------------恢复默认值-----------------------')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f'lockwait_timeout = {self.res}')
        LOG.info(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0179执行完成---')

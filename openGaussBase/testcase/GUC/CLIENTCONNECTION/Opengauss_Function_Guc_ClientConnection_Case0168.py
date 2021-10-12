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
Case Name   : 使用gs_guc set方法设置参数deadlock_timeout为5 ,观察预期结果
Description :
        1.查询deadlock_timeout默认值
        2.修改参数值为5并重启数据库
        3.查看修改后的参数值
        4.恢复参数默认值
Expect      :
        1.显示默认值为1s
        2.设置成功
        3.显示5ms
        4.默认值恢复成功
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

    def test_deadlock_timeout(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show deadlock_timeout;')
        LOG.info(sql_cmd)
        self.assertEqual('1s', sql_cmd.split("\n")[-2].strip())
        LOG.info('--步骤2:设置参数为5并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'deadlock_timeout = 5')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查看修改后的参数值--')
        sql_cmd = commonsh.execut_db_sql('show deadlock_timeout;')
        LOG.info(sql_cmd)
        self.assertEqual('5ms', sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        LOG.info('--步骤4:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('show deadlock_timeout;')
        LOG.info(sql_cmd)
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "deadlock_timeout='1s'")
        LOG.info(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0168执行完成---')

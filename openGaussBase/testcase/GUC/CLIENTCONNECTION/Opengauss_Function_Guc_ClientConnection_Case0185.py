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
Case Name   : 使用gs_guc set方法设置参数update_lockwait_timeout为无效值，
             合理报错
Description :
        1.查询update_lockwait_timeout默认值
        2.修改参数值为test
        3.修改参数值为-1
        4.修改参数值为123.859
        6.修改参数值为空串
        7.恢复参数默认值
Expect      :
        1.显示默认值为2min
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
            '--Opengauss_Function_Guc_ClientConnection_Case0185start-----')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_update_lockwait_timeout(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('show update_lockwait_timeout;')
        LOG.info(sql_cmd)
        self.assertEqual('2min', sql_cmd.split("\n")[-2].strip())
        for i in invalid_value:
            result = commonsh.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"update_lockwait_timeout={i}")
            self.assertFalse(result)

    def tearDown(self):
        LOG.info('--步骤3:恢复默认值--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "update_lockwait_timeout='2min'")
        LOG.info(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0185执行完成---')

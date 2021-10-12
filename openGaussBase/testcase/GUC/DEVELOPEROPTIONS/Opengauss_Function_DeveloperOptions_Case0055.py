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
Case Name   : 使用gs_guc set方法设置参数enable_debug_vacuum为on,观察预期结果
Description :
        1.查询enable_debug_vacuum默认值
        2.修改参数值为on并重启数据库
        3.查询修改后的参数值
        4.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.设置成功
        3.修改后的参数值为on
        4.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class DeveloperOptions(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '----Opengauss_Function_DeveloperOptions_Case0055start------')
        self.constant = Constant()

    def test_enable_debug_vacuum(self):
        LOG.info('--步骤一：查询默认值--')
        sql_cmd = commonsh.execut_db_sql('show enable_debug_vacuum;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        LOG.info('--步骤二：修改参数值为on并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    'enable_debug_vacuum = on')
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        LOG.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤三：查询修改后的参数值--')
        sql_cmd = commonsh.execut_db_sql('show enable_debug_vacuum;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)

    def tearDown(self):
        LOG.info('--步骤四：恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('show enable_debug_vacuum;')
        LOG.info(sql_cmd)
        if "off" != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'enable_debug_vacuum=off')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('show enable_debug_vacuum;')
        LOG.info(sql_cmd)
        LOG.info(
            '-------Opengauss_Function_DeveloperOptions_Case0055finish----')

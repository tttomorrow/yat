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
Case Name   : 使用gs_guc set方法设置参数support_extended_features值为on，
              观察预期结果
Description :
        1.查询support_extended_features默认值
        2.修改参数值为on并重启数据库
        3.查询修改后的参数值
        4.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.修改成功
        3.显示on(开启后资料表示支持数据库的扩展特性，不清楚是支持哪些操作)
        4.默认值恢复成功
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
            '-------Opengauss_Function_Guc_VPC_Case0013start-------')
        self.constant = Constant()

    def test_support_extended_features(self):
        LOG.info('---步骤1:查询默认值---')
        sql_cmd = commonsh.execut_db_sql('''show support_extended_features;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('---步骤2:修改参数值为on---')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     'support_extended_features = on')
        LOG.info(msg)
        self.assertTrue(msg)
        LOG.info('---步骤3:重启数据库---')
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('---步骤4:查询修改后的参数值---')
        sql_cmd = commonsh.execut_db_sql('''show support_extended_features;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)

    def tearDown(self):
        LOG.info('---步骤5:清理环境---')
        sql_cmd = commonsh.execut_db_sql('''show support_extended_features;''')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'support_extended_features'
                                         f'={self.res}')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '------Opengauss_Function_Guc_VPC_Case0013finish-----')

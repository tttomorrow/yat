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
Case Name   : 使用gs_guc set方法设置参数session_replication_role,观察预期结果
Description :
        1.查询session_replication_role默认值
        2.修改参数值为replica并重启数据库
        3.查看修改后的参数值
        4.修改参数值为local并重启数据库
        5.查看修改后的参数值
        6.恢复参数默认值
Expect      :
        1.显示默认值为origin
        2.设置成功
        3.显示replica
        4.设置成功
        5.显示local
        6.默认值恢复成功
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
            '-Opengauss_Function_Guc_ClientConnection_Case0076start--')
        self.constant = Constant()

    def test_session_replication_role(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show session_replication_role;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:修改参数值为replica并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "session_replication_role = 'replica'")
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤3:查看修改后的参数值--')
        sql_cmd = commonsh.execut_db_sql('''show session_replication_role;''')
        LOG.info(sql_cmd)
        self.assertIn('replica', sql_cmd)
        LOG.info('--步骤4:修改参数值为local并重启数据库--')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "session_replication_role = 'local'")
        LOG.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤5:查看修改后的参数值--')
        sql_cmd = commonsh.execut_db_sql('''show session_replication_role;''')
        LOG.info(sql_cmd)
        self.assertIn('local', sql_cmd)

    def tearDown(self):
        LOG.info('--步骤6:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('''show session_replication_role;''')
        LOG.info(sql_cmd)
        if sql_cmd.split('\n')[-2].strip() != self.res:
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"session_replication_role"
                                         f"='{self.res}'")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show session_replication_role;''')
        LOG.info(sql_cmd)
        LOG.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0076执行完成---')

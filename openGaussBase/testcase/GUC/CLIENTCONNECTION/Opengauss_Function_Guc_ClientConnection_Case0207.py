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
Case Name   : ALTER SYSTEM SET方法设置enable_online_ddl_waitlock参数为on
Description :
        1.查看默认值enable_online_ddl_waitlock
        2.修改该参数值为on
        3.重启数据库
Expect      :
        1.默认值为off
        2-3.重启数据库后参数修改成功
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
            '---Opengauss_Function_Guc_Resource_Case0207start--------')
        self.constant = Constant()

    def test_enable_online_ddl_waitlock(self):
        LOG.info('--步骤1:查询该参数默认值--')
        sql_cmd = commonsh.execut_db_sql('show enable_online_ddl_waitlock;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        LOG.info('--步骤2:alter system set方法修改参数值为on--')
        sql_mdg = commonsh.execut_db_sql('''alter system set 
            enable_online_ddl_waitlock to on;
            ''')
        LOG.info(sql_mdg)
        self.assertIn('ALTER SYSTEM SET', sql_mdg)
        LOG.info('--步骤3:重启数据库--')
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤4:查询修改后的值--')
        sql_cmd = commonsh.execut_db_sql('show enable_online_ddl_waitlock;')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd)

    def tearDown(self):
        LOG.info('--步骤5:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('show enable_online_ddl_waitlock;')
        LOG.info(sql_cmd)
        if "off" != sql_cmd.split('\n')[2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'enable_online_ddl_waitlock=off')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('show enable_online_ddl_waitlock;')
        LOG.info(sql_cmd)
        LOG.info(
            '----Opengauss_Function_Guc_ClientConnection_Case0207执行完成---')

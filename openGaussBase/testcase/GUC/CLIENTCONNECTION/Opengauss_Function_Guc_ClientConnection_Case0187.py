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
Case Name   : ALTER SYSTEM SET方法设置max_locks_per_transaction参数为10
Description :
        1.查看默认值max_locks_per_transaction
        2.修改该参数值为10
        3.重启数据库
        4.恢复参数默认值
Expect      :
        1.默认值为256
        2-3.重启数据库后参数修改成功
        4.恢复参数默认值成功
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
            '---Opengauss_Function_Guc_Resource_Case0187start----')
        self.constant = Constant()

    def test_max_locks_per_transaction(self):
        LOG.info('--步骤1:查询该参数默认值--')
        sql_cmd = commonsh.execut_db_sql('''show max_locks_per_transaction;''')
        LOG.info(sql_cmd)
        self.assertEqual('256', sql_cmd.split("\n")[-2].strip())
        LOG.info('--步骤2:alter system set方法修改参数值为10--')
        sql_cmd = commonsh.execut_db_sql('''alter system set 
            max_locks_per_transaction to 10;
            ''')
        LOG.info(sql_cmd)
        self.assertIn('ALTER SYSTEM SET', sql_cmd)
        LOG.info('--步骤3:重启数据库--')
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤4:查询修改后的值--')
        sql_cmd = commonsh.execut_db_sql('''show max_locks_per_transaction;''')
        LOG.info(sql_cmd)
        self.assertEqual('10', sql_cmd.split("\n")[-2].strip())

    def tearDown(self):
        LOG.info('--步骤5:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('''show max_locks_per_transaction;''')
        LOG.info(sql_cmd)
        if "256" != sql_cmd.split('\n')[2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'max_locks_per_transaction=256')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show max_locks_per_transaction;''')
        LOG.info(sql_cmd)
        LOG.info(
            '--Opengauss_Function_Guc_ClientConnection_Case0187执行完成----')

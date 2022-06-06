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
Case Name   : ALTER SYSTEM SET方法设置xloginsert_locks参数为1
Description :
        1.查看默认值xloginsert_locks
        2.修改该参数值为1
        3.重启数据库
Expect      :
        1.默认值为8
        2-3.重启数据库后参数修改成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class ClientConnection(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '----Opengauss_Function_Guc_Resource_Case0211start-------')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_xloginsert_locks(self):
        LOG.info('--步骤1:查询该参数默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show xloginsert_locks;')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        LOG.info('--步骤2:alter system set方法修改参数值为1--')
        sqlmdg = self.commonsh.execut_db_sql('''alter system set
            xloginsert_locks to 1;
            ''')
        LOG.info(sqlmdg)
        self.assertIn('ALTER SYSTEM SET', sqlmdg)
        LOG.info('--步骤3:重启数据库--')
        msg = self.commonsh.restart_db_cluster()
        LOG.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('--步骤4:查询修改后的值--')
        sql_cmd = self.commonsh.execut_db_sql('show xloginsert_locks;')
        LOG.info(sql_cmd)
        self.assertIn('1', sql_cmd)

    def tearDown(self):
        LOG.info('--步骤5:恢复默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show xloginsert_locks;')
        LOG.info(sql_cmd)
        if self.res not in sql_cmd.split('\n')[2].strip():
            msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f'xloginsert_locks={self.res}')
            LOG.info(msg)
            msg = self.commonsh.restart_db_cluster()
            LOG.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.commonsh.execut_db_sql('show xloginsert_locks;')
        LOG.info(sql_cmd)
        LOG.info(
            '---Opengauss_Function_Guc_ClientConnection_Case0211执行完成---')

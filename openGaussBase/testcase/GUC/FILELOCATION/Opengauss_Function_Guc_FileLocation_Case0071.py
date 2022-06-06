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
Case Type   : GUC--文件位置
Case Name   : 检查postgresql.conf文件中参数默认值
Description :
        1.查询config_file默认值
        2.查询不同类型参数默认值
Expect      :
        1.postgresql.conf(实际安装可能带有绝对目录)
        2.默认值正确
History     :
            2021/6/11,修改用例
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()
commonsh = CommonSH('PrimaryDbUser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '-------Opengauss_Function_Guc_FileLocation_Case0071start-------')
        self.constant = Constant()
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.pg_config = os.path.join(macro.DB_INSTANCE_PATH,
                                      macro.DB_PG_CONFIG_NAME)

    def test_enable_beta_features(self):
        LOG.info('---步骤1:查询默认值---')
        sql_cmd = commonsh.execut_db_sql('''show config_file;''')
        LOG.info(sql_cmd)
        self.assertEqual(self.pg_config, sql_cmd.split('\n')[2].strip())
        LOG.info('---步骤2:查询sighup类型fsync默认值---')
        cat_cmd = f"cat  {self.pg_config}| grep 'fsync';"
        LOG.info(cat_cmd)
        exec_msg = self.Primary_User_Node.sh(cat_cmd).result()
        LOG.info(exec_msg)
        self.assertIn('fsync = on', exec_msg)
        LOG.info('---步骤3:查询postmaster类型wal_buffers默认值---')
        cat_cmd = f"cat  {self.pg_config}| grep 'wal_buffers';"
        LOG.info(cat_cmd)
        exec_msg = self.Primary_User_Node.sh(cat_cmd).result()
        LOG.info(exec_msg)
        self.assertIn('wal_buffers = 16MB', exec_msg)
        LOG.info('---步骤4:查询backend类型local_preload_libraries默认值---')
        cat_cmd = f"cat  {self.pg_config}| grep 'local_preload_libraries';"
        LOG.info(cat_cmd)
        exec_msg = self.Primary_User_Node.sh(cat_cmd).result()
        LOG.info(exec_msg)
        self.assertIn("local_preload_libraries = ''", exec_msg)
        LOG.info('---步骤5:查询superuser类型log_statement默认值---')
        cat_cmd = f"cat  {self.pg_config}| grep 'log_statement_stats';"
        LOG.info(cat_cmd)
        exec_msg = self.Primary_User_Node.sh(cat_cmd).result()
        LOG.info(exec_msg)
        self.assertIn("log_statement_stats = off", exec_msg)
        LOG.info('---步骤6:查询user类型client_encoding默认值---')
        cat_cmd = f"cat  {self.pg_config}| grep 'client_encoding';"
        LOG.info(cat_cmd)
        exec_msg = self.Primary_User_Node.sh(cat_cmd).result()
        LOG.info(exec_msg)
        self.assertIn("client_encoding = sql_ascii", exec_msg)

    def tearDown(self):
        LOG.info('---清理环境---')
        sql_cmd = commonsh.execut_db_sql('''show config_file;''')
        LOG.info(sql_cmd)
        if self.pg_config != sql_cmd.split('\n')[2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"config_file='{self.pg_config}'")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '------Opengauss_Function_Guc_FileLocation_Case0071finish-----')

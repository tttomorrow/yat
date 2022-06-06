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
Case Name   : 使用gs_guc set方法设置参数config_file值为空
Description :
        1.查询默认值
        2.修改参数config_file值为空并重启数据库
        3.查询修改后的参数值
        4.清理环境
Expect      :
        1.默认值是postgresql.conf，实际安装可能带有绝对目录
        2.修改成功，重启数据库成功
        3.显示依旧是默认值（初始化默认安装路径）
        4.清理环境完成
History     :
"""
import unittest
import os
from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('PrimaryDbUser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '-------Opengauss_Function_Guc_FileLocation_Case0067start-------')
        self.constant = Constant()
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.config = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.DB_PG_CONFIG_NAME)

    def test_enable_beta_features(self):
        LOG.info('---步骤1:查询默认值---')
        sql_cmd = commonsh.execut_db_sql('''show config_file;''')
        LOG.info(sql_cmd)
        self.assertEqual(self.config, sql_cmd.split('\n')[2].strip())
        LOG.info('---步骤2:修改参数值为空值---')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "config_file=''")
        LOG.info(msg)
        self.assertTrue(msg)
        LOG.info('---步骤3:重启数据库---')
        msg = commonsh.restart_db_cluster()
        LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info('---步骤4:查询修改后的参数值---')
        sql_cmd = commonsh.execut_db_sql('''show config_file;''')
        LOG.info(sql_cmd)
        self.assertEqual(self.config, sql_cmd.split('\n')[2].strip())
        LOG.info('---步骤5:执行sql语句验证---')
        sql_cmd = commonsh.execut_db_sql('''drop table if exists test_067;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, sql_cmd)

    def tearDown(self):
        LOG.info('---步骤6:清理环境---')
        sql_cmd = commonsh.execut_db_sql('''show config_file;''')
        LOG.info(sql_cmd)
        if self.config != sql_cmd.split('\n')[2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"config_file='{self.config}'")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '------Opengauss_Function_Guc_FileLocation_Case0067finish-----')

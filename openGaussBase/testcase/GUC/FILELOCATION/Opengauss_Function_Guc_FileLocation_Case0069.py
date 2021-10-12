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
Case Type   : GUC--文件位置
Case Name   : 使用alter system set方法设置参数config_file值为空，合理报错
Description :
        1.查询默认值
        2.修改参数config_file值为空
Expect      :
        1.默认值是postgresql.conf，实际安装可能带有绝对目录
        2.合理报错,开发薛蒙恩表示这个参数虽然是postmaster型，但是代码里限制
        只能用guc方法设置,添加资料说明--I3EO6P
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
            '-------Opengauss_Function_Guc_FileLocation_Case0069start-------')
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
        sql_cmd = commonsh.execut_db_sql("alter system set config_file to '';")
        LOG.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd)

    def tearDown(self):
        LOG.info('---步骤3:清理环境---')
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
            '------Opengauss_Function_Guc_FileLocation_Case0069finish-----')

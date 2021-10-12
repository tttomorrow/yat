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
Case Name   : 使用gs_guc set方法设置参数hba_file值为数字，合理报错
Description :
        1.查询默认值
        2.修改参数hba_file值为数字
Expect      :
        1.pg_hba.conf(实际安装可能带有绝对目录)
        2.合理报错
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
            '-------Opengauss_Function_Guc_FileLocation_Case0027start-------')
        self.constant = Constant()
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.hba = os.path.join(macro.DB_INSTANCE_PATH, macro.PG_HBA_FILE_NAME)

    def test_enable_beta_features(self):
        LOG.info('---步骤1:查询默认值---')
        sql_cmd = commonsh.execut_db_sql('''show hba_file;''')
        LOG.info(sql_cmd)
        self.assertEqual(self.hba, sql_cmd.split('\n')[2].strip())
        LOG.info('---步骤2:修改参数值为数字---')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f'hba_file=1234')
        LOG.info(msg)
        self.assertFalse(msg)

    def tearDown(self):
        LOG.info('---步骤3:清理环境---')
        sql_cmd = commonsh.execut_db_sql('''show hba_file;''')
        LOG.info(sql_cmd)
        if self.hba != sql_cmd.split('\n')[2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"hba_file='{self.hba}'")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        LOG.info(
            '------Opengauss_Function_Guc_FileLocation_Case0027finish-----')

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
Case Name   : 使用gs_guc set方法设置参数hba_file值为空
Description :
        1.查询默认值
        2.修改参数hba_file值为空并重启数据库
        3.恢复默认值
Expect      :
        1.pg_hba.conf(实际安装可能带有绝对目录)
        2.重启失败
        3.恢复成功
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

commonsh = CommonSH('PrimaryDbUser')


class ClientConnection(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-------Opengauss_Function_Guc_FileLocation_Case0030start-------')
        self.constant = Constant()
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.hba = os.path.join(macro.DB_INSTANCE_PATH, macro.PG_HBA_FILE_NAME)

    def test_enable_beta_features(self):
        self.log.info('---步骤1:查询默认值---')
        sql_cmd = commonsh.execut_db_sql('''show hba_file;''')
        self.log.info(sql_cmd)
        self.assertEqual(self.hba, sql_cmd.split('\n')[2].strip())
        self.log.info('---步骤2:修改参数值为空值---')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"hba_file=''")
        self.log.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        self.log.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertFalse("Degraded" in status or "Normal" in status)
        self.log.info('---步骤3:恢复默认值---')
        msg = commonsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f"hba_file='{self.hba}'")
        self.log.info(msg)
        self.assertTrue(msg)
        msg = commonsh.restart_db_cluster()
        self.log.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show hba_file;''')
        self.log.info(sql_cmd)
        self.assertEqual(self.hba, sql_cmd.split('\n')[2].strip())

    def tearDown(self):
        self.log.info('---步骤3:无须清理环境---')
        self.log.info(
            '------Opengauss_Function_Guc_FileLocation_Case0030finish-----')

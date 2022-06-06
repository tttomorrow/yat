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
Case Name   : gs_guc set修改参数max_connections为100
Description :
        1.查询max_connections默认值；查询max_wal_senders默认值
        2.修改参数max_connections为100并重启数据库（max_connections值需
        大于max_wal_senders值）
        3.清理环境
Expect      :
        1.max_connections默认值为5000；max_wal_senders默认值为16
        2.设置成功，max_connections值需大于max_wal_senders值
        3.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0051start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, 'cluster', 'dn1')
        self.pg_file = os.path.join(macro.DB_INSTANCE_PATH,
                                    macro.PG_HBA_FILE_NAME)
        self.u_name = "u_Guc_Connection_0051"

    def test_data_directory(self):
        text = '---step1:查询max_connections和max_wal_senders参数默认值;' \
               'expect:max_connections为5000；max_wal_senders为16---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql("show max_connections;")
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        sql_cmd = self.pri_sh.execut_db_sql("show max_wal_senders;")
        self.log.info(sql_cmd)
        self.assertIn('16', sql_cmd, '执行失败:' + text)

        text = '---step2:使用gs_guc set设置max_connections为100并重启数据库;' \
               'expect:修改成功'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"max_connections=100")
        self.log.info(result)
        self.assertTrue(result, '执行失败:' + text)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

    def tearDown(self):
        text = '---step3:清理环境;expect:清理环境完成---'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"max_connections={self.res}")
        self.log.info(result)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0051finish-')

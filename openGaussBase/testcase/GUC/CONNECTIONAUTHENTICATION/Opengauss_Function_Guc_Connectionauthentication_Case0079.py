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
Case Name   : gs_guc set修改参数sysadmin_reserved_connections为10
Description :
        1.查询sysadmin_reserved_connections默认值
        2.使用gs_guc set设置sysadmin_reserved_connections参数值并重启数据库
        3.创建系统管理员
        4.系统管理员连接数据库执行查询操作
        5.清理环境
Expect      :
        1.sysadmin_reserved_connections默认值为3
        2.设置成功，max_connections值需大于max_wal_senders值
        3.创建成功
        4.查询成功
        5.清理环境完成
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
            '-Opengauss_Function_Guc_Connectionauthentication_Case0079start-')
        self.constant = Constant()
        self.pr_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, 'cluster', 'dn1')
        self.pg_file = os.path.join(macro.DB_INSTANCE_PATH,
                                    macro.PG_HBA_FILE_NAME)
        self.u_name = "u_guc_connection_0079"
        self.db_name = "db_guc_connection_0079"

    def test_data_directory(self):
        text = '---step1:查询sysadmin_reserved_connections默认值;expect:3---'
        self.log.info(text)
        sql_cmd = self.pr_sh.execut_db_sql(
            "show sysadmin_reserved_connections;")
        self.log.info(sql_cmd)
        self.assertIn('3', sql_cmd, '执行失败:' + text)

        text = '---step2:使用gs_guc set设置sysadmin_reserved_connections' \
               '并重启数据库;expect:修改成功--'
        self.log.info(text)
        result = self.pr_sh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"sysadmin_reserved_connections=10")
        self.log.info(result)
        self.assertTrue(result, '执行失败:' + text)
        msg = self.pr_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pr_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '---step3:创建系统管理员;expect:创建成功---'
        self.log.info(text)
        sql_cmd = self.pr_sh.execut_db_sql(f" drop user if exists "
                                           f"{self.u_name};"
                                           f"create user {self.u_name} with "
                                           f"sysadmin password "
                                           f"'{macro.COMMON_PASSWD}';")
        self.log.info(sql_cmd)
        self.assertIn('CREATE ROLE', sql_cmd, '执行失败:' + text)

        text = '---step4:系统管理员创建数据库;expect:创建成功---'
        self.log.info(text)
        sql_cmd = f'''drop database if exists {self.db_name};\
            create database {self.db_name};'''
        self.log.info(sql_cmd)
        result = self.pr_sh.execut_db_sql(sql=sql_cmd,
                                          sql_type=f'-U {self.u_name} '
                                                   f'-W {macro.COMMON_PASSWD}')
        self.log.info(result)
        self.assertIn('CREATE DATABASE', result, '执行失败:' + text)

    def tearDown(self):
        text = '---step5:清理环境;expect:清理环境完成---'
        self.log.info(text)
        sql_cmd = self.pr_sh.execut_db_sql(f"drop database if exists "
                                           f"{self.db_name};"
                                           f"drop user if exists "
                                           f"{self.u_name}")
        self.log.info(sql_cmd)
        result = self.pr_sh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"sysadmin_reserved_connections=3")
        self.log.info(result)
        self.assertTrue(result, '执行失败:' + text)
        msg = self.pr_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pr_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0079finish-')

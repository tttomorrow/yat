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
Case Type   : 工具-GS_BASEBACKUP
Case Name   : 备份前备份用户的备份权限被收回，相当于无权限备份
Description :
    1.回收sysadmin的备份权限
    2.开始备份gs_basebackup -D /usr2/chenchen/basebackup/bak_a -Fp -Xstream
        -p 18333 -h ip -c fast -l gauss_30.bak -P -v -U sysadmin -w
Expect      :
    1.执行成功
    2.备份报错：gs_basebackup: could not connect to server:
        FATAL:  Normal user is not allowed to use HA channel!
History     :
"""

import os
import time
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.ComThread import ComThread


class GsBaseBackUpCase34(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Primary_Root_Node = Node('PrimaryRoot')
        self.LOG = Logger()
        self.Constant = Constant()
        self.Primary_SH = CommonSH('PrimaryDbUser')
        self.U_NAME = 'u_basebackup_34'
        self.gs_basebackup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                                   'gs_basebackup')
        self.gs_basebackup_bak_name = 'gs_basebackup_Case0034.bak'
        self.Gs_Basebackup_Expect_Msg = 'gs_basebackup: could not connect ' \
                                        'to server: FATAL:  Normal user is not allowed to use HA channel!'
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0034 start----')

    def test_server_tools(self):
        self.LOG.info('----创建备份目录----')
        is_dir_exists_cmd = f'''if [ ! -d "{self.gs_basebackup_bak_path}" ]
                                then
                                    mkdir -p {self.gs_basebackup_bak_path}
                                fi'''
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)
        self.assertEqual(result, '')

        self.LOG.info('----修改备份目录权限700，以免权限有误----')
        chmod_cmd = f"chmod 700 -R {self.gs_basebackup_bak_path}"
        self.LOG.info(chmod_cmd)
        chmod_msg = self.Primary_Root_Node.sh(chmod_cmd).result()
        self.LOG.info(chmod_msg)
        self.assertEqual(chmod_msg, '')

        self.LOG.info('----查看备份目录----')
        ls_cmd = f"ls -l {os.path.dirname(self.gs_basebackup_bak_path)}"
        self.LOG.info(ls_cmd)
        ls_msg = self.Primary_User_Node.sh(ls_cmd).result()
        self.LOG.info(ls_msg)

        self.LOG.info('----创建用户并赋权----')
        sql_cmd = f"create user {self.U_NAME} " \
            f"with password '{macro.COMMON_PASSWD}'; " \
            f"alter user {self.U_NAME} with sysadmin; "
        self.LOG.info(sql_cmd)
        result = self.Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(result)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, result)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, result)

        self.LOG.info("----回收用户权限----")
        sql_cmd = f"alter user {self.U_NAME} with nosysadmin;"
        self.LOG.info(sql_cmd)
        result = self.Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(result)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, result)

        self.LOG.info('----执行备份----')
        gs_basebackup_cmd = f"gs_basebackup " \
            f"-D {self.gs_basebackup_bak_path} " \
            f"-Fp " \
            f"-Xstream " \
            f"-p {self.Primary_User_Node.db_port} " \
            f"-c fast " \
            f"-l {self.gs_basebackup_bak_name} " \
            f"-P " \
            f"-v " \
            f"-U {self.U_NAME} " \
            f"-w"
        backup_cmd = f"source {macro.DB_ENV_PATH}; {gs_basebackup_cmd}"
        self.LOG.info(backup_cmd)
        backup_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.LOG.info(backup_msg)
        self.assertIn(self.Gs_Basebackup_Expect_Msg, backup_msg)

    def tearDown(self):
        self.LOG.info('----删除备份文件----')
        rm_cmd = f'''rm -rf {self.gs_basebackup_bak_path}'''
        primary_result = self.Primary_User_Node.sh(rm_cmd).result()
        self.LOG.info(primary_result)

        self.LOG.info("----删除用户----")
        sql_cmd = f"drop user if exists {self.U_NAME}"
        self.LOG.info(sql_cmd)
        result = self.Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(result)

        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0034 end----')

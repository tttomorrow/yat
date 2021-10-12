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
Case Name   : 指定一个不存在的用户备份
Description :
    1、开始备份：gs_basebackup -D /usr2/chenchen/basebackup/bak_Pvfast_wtnotexistusr
        -Ft -Xfetch -p 18333 -l gauss_19.bak -P -v -U notexistusr -w
Expect      :
    1、备份报错：gs_basebackup: could not connect to server:
        FATAL:  Invalid username/password,login denied.
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


class GsBaseBackUpCase18(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Primary_Root_Node = Node('PrimaryRoot')
        self.LOG = Logger()
        self.Constant = Constant()
        self.Primary_SH = CommonSH('PrimaryDbUser')
        self.gs_basebackup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                                   'gs_basebackup')
        self.U_Name = 'u_basebackup_18'
        self.gs_basebackup_bak_name = 'gs_basebackup_Case0018.bak'
        self.Gs_Basebackup_Expect_Msg = 'gs_basebackup: ' \
                                        'could not connect to server: FATAL:  ' \
                                        'Invalid username/password,login denied.'
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0018 start----')

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
        ls_cmd = f"chmod 700 -R {self.gs_basebackup_bak_path}"
        self.LOG.info(ls_cmd)
        ls_msg = self.Primary_Root_Node.sh(ls_cmd).result()
        self.LOG.info(ls_msg)
        self.assertEqual(ls_msg, '')

        self.LOG.info('----查看备份目录----')
        ls_cmd = f"ls -l {os.path.dirname(self.gs_basebackup_bak_path)}"
        self.LOG.info(ls_cmd)
        ls_msg = self.Primary_User_Node.sh(ls_cmd).result()
        self.LOG.info(ls_msg)

        self.LOG.info('----确保用户不存在---')
        sql_cmd = f"drop user if exists {self.U_Name}; "
        self.LOG.info(sql_cmd)
        sql_result = self.Primary_SH.execut_db_sql(sql_cmd)
        self.LOG.info(sql_result)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_result)

        self.LOG.info('----执行备份----')
        gs_basebackup_cmd = f"gs_basebackup " \
            f"-D {self.gs_basebackup_bak_path} " \
            f"-Fp " \
            f"-Xstream " \
            f"-p {self.Primary_User_Node.db_port} " \
            f"-l {self.gs_basebackup_bak_name} " \
            f"-P " \
            f"-v " \
            f"-U {self.U_Name} " \
            f"-w"
        backup_cmd = f'''
                    source {macro.DB_ENV_PATH}; {gs_basebackup_cmd}
                    '''
        self.LOG.info(backup_cmd)
        backup_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.LOG.info(backup_msg)
        self.assertIn(self.Gs_Basebackup_Expect_Msg, backup_msg)

    def tearDown(self):
        self.LOG.info('----删除备份目录----')
        is_dir_exists_cmd = f'''rm -rf {self.gs_basebackup_bak_path}'''
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)

        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0018 end----')

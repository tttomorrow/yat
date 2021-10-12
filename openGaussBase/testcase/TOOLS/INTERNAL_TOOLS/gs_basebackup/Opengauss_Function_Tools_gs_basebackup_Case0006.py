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
Case Name   : 指定的备份目录不存在
Description :
    1、执行备份：gs_basebackup -D /usr2/chenchen/basebackup/bak_notexist
        -Fp -Xstream -p 18333 -l gauss_7.bak -U sysadmin -W
Expect      :
    1、备份报错：gs_basebackup: realpath dir
        "/usr2/chenchen/basebackup/bak_notexist" failed:
        No such file or directory
History     :
"""

import os
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.Logger import Logger


class GsBaseBackUpCold(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.LOG = Logger()
        self.gs_basebackup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                                   'gs_basebackup')
        self.gs_basebackup_bak_name = 'gs_basebackup_Case0006.bak'
        self.ASSERT_INFO = f'gs_basebackup: realpath dir ' \
            f'"{self.gs_basebackup_bak_path}" ' \
            f'failed: No such file or directory'
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0006 start----')

    def test_server_tools(self):
        self.LOG.info('----使目录不存在----')
        is_dir_exists_cmd = f'''if [ -d "{self.gs_basebackup_bak_path}" ]
                                then
                                    rm -rf {self.gs_basebackup_bak_path}
                                fi'''
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)

        self.LOG.info('----执行备份----')
        gs_basebackup_cmd = f"gs_basebackup " \
            f"-D {self.gs_basebackup_bak_path} " \
            f"-Fp " \
            f"-Xstream " \
            f"-p {self.Primary_User_Node.db_port} " \
            f"-l {self.gs_basebackup_bak_name} " \
            f"-U {self.Primary_User_Node.ssh_user} " \
            f"-W "
        backup_cmd = f'''
            source {macro.DB_ENV_PATH}; {gs_basebackup_cmd}
            '''
        self.LOG.info(backup_cmd)
        backup_result = self.Primary_User_Node.sh(backup_cmd).result()
        self.LOG.info(backup_result)
        self.assertIn(self.ASSERT_INFO, backup_result)

    def tearDown(self):
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0006 end----')

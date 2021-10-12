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
Case Name   : gs_basebackup当前仅支持热备份模式，冷机无法备份
Description :
    1、停止数据库
    2、创建目录bak_down
    3、执行备份：gs_basebackup -D /usr2/chenchen/basebackup/bak_down -Fp
        -Xstream -p 18333 -l gauss_4.bak -U sysadmin -W
Expect      :
    1、执行成功
    2、目录创建成功
    3、备份报错：gs_basebackup: could not connect to server
History     :
"""

import unittest
import os

from yat.test import Node
from yat.test import macro

from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class GsBaseBackUpCold(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.LOG = Logger()
        self.CommonSH = CommonSH()
        self.gs_basebackup_bak_path = os.path.join(macro.DB_BACKUP_PATH,
                                                   'gs_basebackup')
        self.gs_basebackup_bak_name = 'gs_basebackup_Case0003.bak'
        self.ASSERT_INFO = f"failed to connect Unknown:"
        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0003 start----')

    def test_server_tools(self):
        self.LOG.info('----停止数据库----')
        is_stopped = self.CommonSH.stop_db_cluster()
        self.assertTrue(is_stopped)

        self.LOG.info('----创建目录----')
        is_dir_exists_cmd = f'''if [ ! -d "{self.gs_basebackup_bak_path}" ]
                                then
                                    mkdir {self.gs_basebackup_bak_path}
                                fi'''
        result = self.Primary_User_Node.sh(is_dir_exists_cmd).result()
        self.LOG.info(result)

        self.LOG.info('----清空目录----')
        ls_cmd = f"rm -rf {os.path.join(self.gs_basebackup_bak_path, '*')}"
        result = self.Primary_User_Node.sh(ls_cmd).result()
        self.LOG.info(result)
        self.assertEqual(result, '')

        self.LOG.info('----查看目录权限----')
        ls_cmd = f"ls -l {os.path.dirname(self.gs_basebackup_bak_path)}"
        result = self.Primary_User_Node.sh(ls_cmd).result()
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
            source {macro.DB_ENV_PATH}
            expect <<EOF
            set timeout 300
            spawn {gs_basebackup_cmd}
            expect "*assword:"
            send "{self.Primary_User_Node.ssh_password}\\n"
            expect eof\n''' + "EOF"
        self.LOG.info(backup_cmd)
        backup_result = self.Primary_User_Node.sh(backup_cmd).result()
        self.LOG.info(backup_result)
        self.assertIn(self.ASSERT_INFO, backup_result)

    def tearDown(self):
        self.LOG.info('----清理备份目录----')
        clean_cmd = f"rm -rf {self.gs_basebackup_bak_path}"
        result = self.Primary_User_Node.sh(clean_cmd).result()
        self.LOG.info(result)

        self.LOG.info('----启动数据库----')
        is_started = self.CommonSH.start_db_cluster()
        self.LOG.info(is_started)

        self.LOG.info(
            '----Opengauss_Function_Tools_gs_basebackup_Case0003 end----')

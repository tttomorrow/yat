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
Case Type   : 系统内部使用工具
Case Name   : 远程模式下，执行全备份,通过SSH连接对远程系统进行全备份，
              指定--remote-user、--remote-host、--remote-port、-d、-p、
              -U选项， -U指定初始用户,合理报错
Description :
    1.创建备份目录
    2.进行初始化
    3.在备份路径内初始化一个新的备份实例
    4.远程备份
    5.清理环境
Expect      :
    1.创建成功
    2.初始化成功
    3.添加成功
    4.备份失败，合理报错
    5.清理环境完成
            新增--remote-lib=libpath参数
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(), '单机环境不执行')
class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.Primary_User_Node = Node('PrimaryDbUser')
        self.Standby1_User_Node = Node('Standby1DbUser')
        self.log = Logger()
        self.constant = Constant()
        self.re_path = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                    'app', 'bin')
        self.remote_lib = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                       'app', 'lib')
        self.gs_probackup_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH),
            'gs_probackup_testdir0164')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.log.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0164 start----')

    def test_server_tools(self):
        text = '--step1:创建备份目录;expect:创建成功----'
        self.log.info(text)
        mkdir_cmd = f'''if [ ! -d "{self.gs_probackup_path}" ]
                        then
                            mkdir -p {self.gs_probackup_path}
                        fi'''
        self.log.info(mkdir_cmd)
        primary_result = self.Primary_User_Node.sh(mkdir_cmd).result()
        self.log.info(primary_result)
        self.assertEqual(primary_result, '', '执行失败:' + text)

        text = '--step2:进行初始化;expect:初始化成功---'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup init -B {self.gs_probackup_path};"
        self.log.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn(self.constant.init_success, init_msg, '执行失败:' + text)

        text = '-step3:在备份路径内初始化一个新的备份实例;expect:添加成功--'
        self.log.info(text)
        init_cmd = f"source {macro.DB_ENV_PATH};" \
                   f"gs_probackup add-instance " \
                   f"-B {self.gs_probackup_path} " \
                   f"-D {macro.DB_INSTANCE_PATH} " \
                   f"--instance=test_0164 " \
                   f"--remote-user={self.Standby1_User_Node.ssh_user} " \
                   f"--remote-host={self.Standby1_User_Node.db_host} " \
                   f"--remote-port=22 " \
                   f"--remote-proto=ssh " \
                   f"--remote-path={self.re_path} " \
                   f"--remote-lib={self.remote_lib} " \
                   f"--ssh-options='-o ServerAliveCountMax=5 " \
                   f"-o ServerAliveInterval=60'"
        self.log.info(init_cmd)
        init_msg = self.Primary_User_Node.sh(init_cmd).result()
        self.log.info(init_msg)
        self.assertIn("'test_0164' " + self.constant.init_success, init_msg,
                      '执行失败:' + text)

        text = '--step4:远程备份;expect:合理报错----'
        self.log.info(text)
        backup_cmd = f"source {macro.DB_ENV_PATH}; " \
                     f"gs_probackup  backup " \
                     f"-B {self.gs_probackup_path} " \
                     f"--instance=test_0164 " \
                     f"-b FULL " \
                     f"--stream " \
                     f"--remote-user={self.Standby1_User_Node.ssh_user}  " \
                     f"--remote-host={self.Standby1_User_Node.db_host}  " \
                     f"--remote-port=22  " \
                     f"--remote-proto=ssh  " \
                     f"--remote-path={self.re_path} " \
                     f"--remote-lib={self.remote_lib} " \
                     f"-d postgres  " \
                     f"-U {self.Standby1_User_Node.ssh_user}  " \
                     f"-W '{self.Standby1_User_Node.ssh_password}' " \
                     f"-p {self.Standby1_User_Node.db_port}"
        self.log.info(backup_cmd)
        exec_msg = self.Primary_User_Node.sh(backup_cmd).result()
        self.log.info(exec_msg)
        self.assertIn('FATAL', exec_msg, '执行失败:' + text)

    def tearDown(self):
        text = '--step5:清理环境;expect:清理环境完成---'
        self.log.info(text)
        clear_cmd = f'rm -rf {self.gs_probackup_path}'
        self.log.info(clear_cmd)
        clear_msg = self.Primary_User_Node.sh(clear_cmd).result()
        self.log.info(clear_msg)
        self.log.info(
            '----Opengauss_Function_Tools_Gs_Probackup_Case0164 end----')

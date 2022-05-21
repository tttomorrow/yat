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
Case Name   : 查看gs_probackup add-instance命令的摘要信息
Description :
    1.执行命令显示gs_probackup add-instance命令的摘要信息
Expect      :
    1.显示gs_probackup add-instance命令的摘要信息成功
History     :
"""

import unittest
import os
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.except_msg = '''
        gs_probackup add-instance 
        -B backup-path 
        -D pgdata-path --instance=instance_name
        [-E external-directories-paths]
        [--remote-proto=protocol] [--remote-host=destination]
        [--remote-path=path] [--remote-user=username]
        [--remote-port=port] [--ssh-options=ssh_options]
        [--remote-libpath=libpath]
        -B, --backup-path=backup-path    
        location of the backup storage area
        -D, --pgdata=pgdata-path         
        location of the database storage area
        --instance=instance_name     name of the new instance
        -E, --external-dirs=external-directories-paths
        backup some directories not from pgdata
        (example: --external-dirs=/tmp/dir1:/tmp/dir2)
        Remote options:
        --remote-proto=protocol      remote protocol to use
        available options: 'ssh', 'none' (default: ssh)
        --remote-host=destination    remote host address or hostname
        --remote-port=port           remote host port (default: 22)
        --remote-path=path           
        path to directory with gs_probackup binary on remote host
        (default: current binary path)
        --remote-user=username       
        user name for ssh connection (default: current user)
        --remote-libpath=libpath         library path on remote host
        --ssh-options=ssh_options    
        additional ssh options (default: none)
        (example: --ssh-options='-c cipher_spec -F configfile')'''

    def test_system_internal_tools(self):
        self.log.info('step1 执行命令显示gs_probackup add-instance命令的摘要信息')
        help_cmd = f"source {macro.DB_ENV_PATH};" \
            f"gs_probackup add-instance --help;"
        self.log.info(help_cmd)
        help_msg = self.PrimaryNode.sh(help_cmd).result()
        self.log.info(help_msg)
        line_msg = help_msg.splitlines()
        self.log.info(line_msg)
        for line in line_msg:
            if line:
                for part in line.split():
                    self.assertIn(part.strip(), self.except_msg)

    def tearDown(self):
        # 无须清理环境
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

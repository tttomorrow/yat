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
Case Type   : 服务端工具
Case Name   : 各主机间root互信状态不正常(互信文件和进程都不存在)时检查操作系统
Description :
    1.创建root互信
    2.破坏互信（删除互信文件，杀掉root互信进程）
    3.各主机间root互信状态不正常时检查操作系统：gs_checkos -i A
Expect      :
    1.创建root互信
    2.破坏互信（删除互信文件，杀掉root互信进程）成功
    3.执行失败
History     :
    root互信被破坏但互信进程ssh-agent仍存在，不影响互信
"""

import os
import unittest
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.root_com_pri = CommonSH('PrimaryRoot')
        self.root_node_pri = Node('PrimaryRoot')
        self.root_node_sta1 = Node('Standby1Root')
        self.root_node_sta2 = Node('Standby2Root')
        self.constant = Constant()
        self.ssh_file = '~/.ssh/'
        self.ssh_path_bak = os.path.join(macro.DB_INSTANCE_PATH, 'ssh')
        self.check_res = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
                          'A9', 'A10', 'A11', 'A12', 'A13', 'A14']
        text = "-----step1: 创建root互信; expect: 执行成功-----"
        self.log.info(text)
        self.host_tuple = (self.root_node_pri.ssh_host,
                           self.root_node_sta1.ssh_host,
                           self.root_node_sta2.ssh_host)
        self.params = {'-f': 'test_hosts'}
        self.root_com_pri.exec_gs_sshexkey(macro.DB_SCRIPT_PATH,
                                           *self.host_tuple,
                                           **self.params)

        text = '----step2: 破坏互信（删除互信文件，杀掉root互信进程）; expect: 执行成功-----'
        self.log.info(text)
        rm_cmd = f"rm -rf {self.ssh_file}/* ;" \
            "ps -aux  | grep root | grep ssh-agent | grep " \
            "/root/gaussdb_tmp/gauss_socket_tmp | grep -v PID | " \
            "awk '{{print $2}}' | xargs kill -9"
        self.log.info(rm_cmd)
        rm_msg = self.root_node_pri.sh(rm_cmd).result()
        self.log.info(f'rm_msg = {rm_msg}')

    def test_server_tools(self):
        self.log.info('----step3: 互信状态不正常时检查操作系统; '
                      'expect: 执行失败----')
        hostname_cmd = f'''hostname; '''
        hostname1 = self.root_node_sta1.sh(hostname_cmd).result()
        self.log.info(hostname1)

        checkos_cmd = f'''source {macro.DB_ENV_PATH};
            expect <<EOF
            set timeout 300
            spawn gs_checkos -i A -h {hostname1};
            expect "*yes/no)?"
            send "yes\\n"
            expect {{{{
                "*assword:" {{{{ send "{self.root_node_pri.ssh_password}\n"; \
                exp_continue }}}}
                eof {{{{ send_user "执行成功！\n" }}}}
                }}}}\n''' + "EOF"
        self.log.info(checkos_cmd)
        checkos_msg = self.root_node_pri.sh(checkos_cmd).result()
        self.log.info(checkos_msg)
        self.assertIn('Failed', checkos_msg)

    def tearDown(self):
        self.log.info('-----无需清理环境-----')
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

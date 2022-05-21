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
Case Name   : 指定多个需要检查的主机名称（主备关系），主机之间使用“英文逗号”分割
Description :
    1. 查看主机名称
    2. 查看备机名称
    3. 指定多个需要检查的主机名称（主备关系）主机之间使用“英文逗号”分割
    4.清理环境
Expect      :
    1. 查看主机名称成功
    2. 查看备机名称成功
    3. 指定多个需要检查的主机名称（主备关系）主机之间使用“英文逗号”分割成功
    4.清理环境成功
History     :
        优化依赖root互信部分代码
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)}start-----')
        self.common = Common()
        self.constant = Constant()
        self.standby2sh = CommonSH('Standby2Root')
        self.primary_dbuser = Node('PrimaryDbUser')
        self.standby1_node = Node('Standby1DbUser')
        self.root_node_pri = Node('PrimaryRoot')
        self.root_node_sta1 = Node('Standby1Root')
        self.root_node_sta2 = Node('Standby2Root')
        self.conf_path = os.path.join(macro.DB_INSTANCE_PATH,
                                      macro.DB_PG_CONFIG_NAME)
        self.ssh_file = '~/.ssh'
        self.log.info("-----获取备节点ip-----")
        shell_cmd = f"cat {self.conf_path} | " \
            f"grep 'replconninfo' | " \
            f"grep -Ev '^#' | " \
            f"tr -s ' '| " \
            f"cut -d ' ' -f 7 | " \
            f"cut -d '=' -f 2"
        self.log.info(shell_cmd)
        msg = self.primary_dbuser.sh(shell_cmd).result()
        self.log.info(msg)
        self.standby_ip_list = msg.splitlines()
        self.log.info(self.standby_ip_list)

        text = '-----数据库解压安装包-----'
        self.log.info(text)
        cmd = f'cd {os.path.dirname(macro.DB_SCRIPT_PATH)} && ' \
            f'tar -xf openGauss-Package-bak*.tar.gz && ' \
            f'ls {macro.DB_SCRIPT_PATH}|grep gs_sshexkey'
        self.log.info(cmd)
        res = self.common.get_sh_result(self.root_node_sta1, cmd)
        self.assertEqual(res, 'gs_sshexkey', f'执行失败: {text}')

        self.log.info("-----创建root互信-----")
        self.host_tuple = (self.root_node_pri.ssh_host,
                           self.root_node_sta1.ssh_host,
                           self.root_node_sta2.ssh_host)
        self.params = {'-f': 'test_hosts'}
        self.standby2sh.exec_gs_sshexkey(macro.DB_SCRIPT_PATH,
                                             *self.host_tuple,
                                             **self.params)

    def test_server_tools1(self):
        text = '-----step1: 查看主机名称 expect: 执行成功-----'
        self.log.info(text)
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname1 = self.primary_dbuser.sh(check_cmd).result()
        self.log.info(hostname1)

        text = '-----step2: 查看备机名称 expect: 执行成功-----'
        self.log.info(text)
        self.log.info('-----查看备机名称-----')
        check_cmd = f'hostname'
        self.log.info(check_cmd)
        hostname2 = self.standby1_node.sh(check_cmd).result()
        self.log.info(hostname2)

        text = '-----step3: 指定多个需要检查的主机名称（主备关系），' \
               '主机之间使用“英文逗号”分割 expect: 执行成功-----'
        self.log.info(text)
        self.log.info('-指定多个需要检查的主机名称（主备关系），主机之间使用“英文逗号”分割-')
        checkos_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkos -i A8 -h {hostname1},{hostname2}'
        self.log.info(checkos_cmd)
        checkos_msg = self.root_node_pri.sh(checkos_cmd).result()
        self.log.info(checkos_msg)
        list1 = checkos_msg.split('\n')
        self.log.info(list1)
        list2 = list1[1].split(':')
        self.log.info(list2)
        self.assertEqual(list2[0].strip(),
                         'A8. [ Disk configuration status ]', '状态异常')
        i = list2[1].strip()
        self.assertTrue(i in ['Normal', 'Warning'], f'状态异常: {i}')

    def tearDown(self):
        text = '----step4: 清理环境 expect: 执行成功----'
        self.log.info(text)
        self.log.info("-----step:4.1清理集群节点互信文件-----")
        for i in self.standby_ip_list:
            self.log.info(f"-----清理备节点互信文件-----")
            rm_cmd1 = f'''ssh {i} <<EOF rm -rf {self.ssh_file}/*\n''' + "EOF"
            self.log.info(rm_cmd1)
            rm_res1 = self.root_node_pri.sh(rm_cmd1).result()
            self.log.info(rm_res1)

        self.log.info(f"-----step:4.2清理主节点互信文件-----")
        rm_cmd2 = f'''rm -rf {self.ssh_file}/*;ls {self.ssh_file}'''
        self.log.info(rm_cmd2)
        rm_res2 = self.root_node_pri.sh(rm_cmd2).result()
        self.log.info(rm_res2)
        self.assertEqual('', rm_res2, '执行失败:' + text)
        self.log.info(f"-----{os.path.basename(__file__)}执行结束-----")

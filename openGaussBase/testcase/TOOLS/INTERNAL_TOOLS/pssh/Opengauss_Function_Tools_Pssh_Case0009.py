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
Case Name   : pssh -h指定空主机列表文件与正确命令
Description :
    1.创建主机ip列表文件
    2.执行pssh -h指定空主机列表文件与正确命令
    3.清理环境
Expect      :
    1.创建成功
    2.执行成功，返回相应结果
    3.清理成功
History     :
"""
import os
import unittest
from testcase.utils.Common import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro
primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != primary_sh.get_node_num(), '非1+2不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.primary_root_node = Node('PrimaryRoot')
        self.primary_node = Node('PrimaryDbUser')
        self.s_root_node1 = Node('Standby1Root')
        self.s_node1 = Node("Standby1DbUser")
        self.s_node2 = Node("Standby2DbUser")
        self.com_root = CommonSH("PrimaryRoot")
        self.ssh_file = os.path.join('/', 'home',
                                     f'{self.primary_node.ssh_user}',
                                     'ssh_file')
        self.common = Common()

    def test_standby(self):
        text = '-----step1:创建主机列表文件 expect:成功-----'
        self.log.info(text)
        self.log.info('-----查看主机名-----')
        add_cmd = f"rm -rf {self.ssh_file};touch {self.ssh_file};" \
                  f"cat {self.ssh_file}"
        self.log.info(add_cmd)
        add_res = self.primary_root_node.sh(add_cmd).result()
        self.log.info(add_res)
        self.assertEqual('', add_res, '构建文件失败')

        text = '-----step2:执行pssh -h指定空主机列表与正确的命令 expect:失败-----'
        self.log.info(text)
        self.log.info("-----创建root互信-----")
        result = self.common.get_sh_result(self.primary_root_node,
                                           f"ls {macro.DB_SCRIPT_PATH}")
        if "gs_sshexkey" not in result:
            cmd = f"cd {macro.DB_SCRIPT_PATH}/../; " \
                  f"tar -zxvf openGauss-Package-bak*.tar.gz > /dev/null"
            result = self.primary_root_node.sh(cmd).result()
            self.log.info(result)
            result = self.common.get_sh_result(self.primary_root_node,
                                               f"ls {macro.DB_SCRIPT_PATH}")
            self.log.info(result)
            if "gs_sshexkey" not in result:
                raise Exception("cat not find gs_sshexkey, Please check!")

        self.host_tuple = (self.primary_root_node.ssh_host,
                           self.s_node1.ssh_host, self.s_node2.ssh_host)
        self.params = {'-f': 'test_hosts'}
        self.com_root.exec_gs_sshexkey(macro.DB_SCRIPT_PATH,
                                       *self.host_tuple,
                                       **self.params)

        self.log.info('-----执行pssh命令-----')
        pssh_cmd = f"pssh -s -h {self.ssh_file} hostname"
        self.log.info(pssh_cmd)
        pssh_res = self.primary_root_node.sh(pssh_cmd).result()
        self.log.info(pssh_res)
        self.assertIn('min() arg is an empty sequence', pssh_res, '执行失败')

    def tearDown(self):
        text = '-----step3:清理环境，删除ssh文件 expect:成功-----'
        self.log.info(text)
        rm_res = self.primary_root_node.sh(f'rm -rf {self.ssh_file}').result()
        self.assertEqual('', rm_res, '文件删除失败')
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

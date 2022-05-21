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
Case Name   : pssh指定-o并指定正确输出结果目录
Description :
    1.pssh指定-o并指定正确输出结果目录
    2.清理环境
Expect      :
    1.执行成功，输出结果文件中报错输出结果
    2.清理成功
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
        self.out_path = os.path.join('/', 'home',
                                     f'{self.primary_node.ssh_user}')
        self.com_root = CommonSH("PrimaryRoot")
        self.common = Common()

    def test_standby(self):
        text = '-----step1:pssh指定-o并指定正确输出结果目录 expect:成功-----'
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
        test = '-----查看主机名-----'
        self.log.info(test)
        node_name = self.s_root_node1.sh("uname -n").result()
        self.log.info(node_name)
        self.assertIsNotNone(node_name, '执行失败:' + text)
        self.log.info('-----执行pssh命令-----')
        pssh_cmd = f"pssh -s -o {self.out_path} -H {node_name} hostname"
        self.log.info(pssh_cmd)
        pssh_res = self.primary_root_node.sh(pssh_cmd).result()
        self.log.info(pssh_res)
        global output_path
        output_path = os.path.join(self.out_path, f'{node_name}')
        check_cmd = f"cat {output_path}"
        self.log.info(check_cmd)
        check_res = self.primary_root_node.sh(check_cmd).result()
        self.assertIn(node_name, check_res, '执行失败')

    def tearDown(self):
        text = f'-----step2:清理环境 expect:成功-----'
        self.log.info(text)
        del_res = self.primary_root_node.sh(f'rm -rf {output_path}').result()
        self.log.info(del_res)
        self.assertEqual('', del_res, '文件删除失败')
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

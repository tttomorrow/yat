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
Case Name   :
    root类检查项CheckFirewall，参数-i,-l,-o,-L的组合测试，
    用--skip-root-items参数跳过需要root权限执行的检查项
Description :
    1.创建存放检查结果文件夹
    2.用户检查防火墙状态，将检查结果输出到指定文件夹
Expect      :
    1.创建存放检查结果文件夹成功
    2.检查失败，将检查结果输出到指定文件夹成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0339start--')
        self.dbuser_node = Node('dbuser')
        self.primary_root = Node('PrimaryRoot')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.log.info('----步骤1.创建存放检查结果文件夹------')
        mkdir_cmd = f'mkdir /home/test_check/ ;' \
            f'chmod -R 777 /home/test_check/;' \
            f'ls /home'
        self.log.info(mkdir_cmd)
        mkdir_msg = self.primary_root.sh(mkdir_cmd).result()
        self.log.info(mkdir_msg)
        self.assertIn('test_check', mkdir_msg)

        self.log.info('---步骤2.用户检查防火墙状态，本地执行，将检查结果输出到指定文件夹---')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_check -i CheckFirewall -U {self.dbuser_node.ssh_user} -L ' \
            f'-l /home/test_check/test_check.log -o /home/test_check/ ' \
            f'--skip-root-items --set'
        self.log.info(check_cmd)
        check_msg = self.dbuser_node.sh(check_cmd).result()
        self.log.info(check_msg)
        self.assertIn('ERROR: No check item can be performed, '
                      'please confirm the input parameters', check_msg)

        self.log.info('-------步骤3.判断log日志是否生成-------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'ls /home/test_check/;' \
            f'cat /home/test_check/test_check*.log'
        self.log.info(check_cmd)
        check_msg = self.dbuser_node.sh(check_cmd).result()
        self.log.info(check_msg)
        self.assertIn('test_check', check_msg)
        self.assertIn('ERROR: No check item can be performed, '
                      'please confirm the input parameters', check_msg)

    def tearDown(self):
        rm_cmd = f'rm -rf /home/test_check/'
        self.log.info(rm_cmd)
        rm_msg = self.primary_root.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0339finish--')

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
Case Type   : 服务端工具
Case Name   : 其他用户检查CPU使用率
Description :
     1.在root用户下创建用户Mary：
        groupadd mary
        useradd -g mary -d /home/mary -m -s /bin/bash mary
     2.切换到omm用户下
     3.sourec 环境变量
     4.检查：gs_check -i CheckCPU -U mary
     5.清理环境：userdel  -r mary
Expect      :
    1.用户创建成功
    2.用户切换成功
    3.sourec 环境变量
    4.检查失败
    5.清理用户
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()

class Tools(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_Tools_gs_check_Case0307start-------------------')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------root用户创建其他用户------------------')
        check_cmd1 = f'''
                                groupadd mary
                                useradd -g mary -d /home/mary -m -s /bin/bash mary
                                '''
        logger.info(check_cmd1)
        msg1 = self.rootNode.sh(check_cmd1).result()
        logger.info(msg1)
        logger.info('------------------其他用户检查CPU使用率------------------')
        check_cmd1 = f'''
                                source {macro.DB_ENV_PATH}
                                gs_check -i CheckCPU -U mary
                                 '''
        logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        logger.info(msg1)
        self.assertIn('not current user',msg1)

    def tearDown(self):
        logger.info('--------------清理环境-------------------')
        check_cmd2 = 'userdel  -r mary'
        logger.info(check_cmd2)
        msg1 = self.rootNode.sh(check_cmd2).result()
        logger.info(msg1)
        logger.info('------------------Opengauss_Function_Tools_gs_check_Case0307finish------------------')

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
Case Name   : gs_encrypt工具显示版本信息(正常)
Description :
    1.执行命令:
      gs_encrypt -V  查看版本信息
Expect      :
    1.显示工具版本信息
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0003 start')
        self.dbuserNode = Node('PrimaryDbUser')

    def test_gs_encrypt(self):
        self.logger.info('-----显示版本信息-----')
        step = "step1:执行命令,查看版本信息  except:显示工具版本信息"
        self.logger.info(step)
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt -V '''
        self.logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        self.logger.info("-----版本信息-----")
        self.logger.info(msg1)
        self.assertIn('openGauss', msg1, "执行失败" + step)

    def tearDown(self):
        self.logger.info('-----无需清理环境-----')
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0003 finish')

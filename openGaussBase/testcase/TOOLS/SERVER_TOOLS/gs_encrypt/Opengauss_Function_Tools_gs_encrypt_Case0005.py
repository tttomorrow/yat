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
Case Name   : gs_encrypt工具单独使用参数-k加密明文字符串
Description :
    1.执行命令:
      gs_encrypt -k [用户输入的口令] [待加密的明文字符串]
      单独使用-k参数加密明文字符串
Expect      :
    1.执行失败，报错提示-k参数不能单独使用
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0005 start')
        self.dbuserNode = Node('PrimaryDbUser')
        self.Constant = Constant()
        self.str = 'test'
        self.encrypt = 'kj#HH452'

    def test_gs_encrypt(self):
        self.logger.info('-----进行加密操作-----')
        step = "step1:执行命令,单独使用-k参数加密明文字符串 except:执行失败，" \
               "报错提示-k参数不能单独使用"
        self.logger.info(step)
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt -k {self.encrypt} {self.str} '''
        self.logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        self.logger.info("-----加密结果-----")
        self.logger.info(msg1)
        self.assertIn(self.Constant.secure_false, msg1, "执行失败" + step)

    def tearDown(self):
        self.logger.info('-----无需清理环境-----')
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0005 finish')

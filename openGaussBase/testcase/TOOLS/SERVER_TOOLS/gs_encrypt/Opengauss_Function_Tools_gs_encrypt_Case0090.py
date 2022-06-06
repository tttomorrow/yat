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
Case Name   : gs_encrypt工具组合使用参数--key，--vector加密明文字符串,
              --key后输入8位纯数字的口令
Description :
    1.执行命令,组合使用参数--key，--vector加密明文字符串,
      --key后输入8位纯数字口令
      gs_encrypt --key=[用户输入的口令] --vector=[用户输入的盐值]
      [待加密明文字符串]
Expect      :
    1.执行失败，报错提示口令要至少包含3种类型字符
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class GsEncrypt60(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.dbuserNode = Node('PrimaryDbUser')
        self.con = Constant()
        self.common = Common()

    def test_gs_encrypt(self):
        self.logger.info('------------------进行加密操作------------------')
        step = "step1:执行命令,组合使用参数--key，--vector加密明文字符串," \
               "--key后输入8位纯数字口令 " \
               "except:执行失败，报错提示口令要至少包含3种类型字符"
        self.logger.info(step)
        str1 = 'test'
        encrypt = '12345678'
        vec = '1234567891236548'
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt --key={encrypt} --vector={vec} {str1}'''
        self.logger.info(check_cmd1)
        self.logger.info("--------加密结果---------")
        msg1 = self.common.get_sh_result(self.dbuserNode, check_cmd1)
        self.assertIn(self.con.encrypted_fail_msg, msg1, "执行失败" + step)

    def tearDown(self):
        self.logger.info('--------------无需清理环境-------------------')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

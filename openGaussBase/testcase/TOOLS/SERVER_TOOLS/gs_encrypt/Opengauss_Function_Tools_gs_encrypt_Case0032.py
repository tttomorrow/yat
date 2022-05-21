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
Case Name   : gs_encrypt工具组合使用参数-k，-v加密明文字符串,-k后输入8位纯大写字
             母的口令
Description :
    1.执行命令:
      gs_encrypt -k [用户输入的口令] -v [用户输入的盐值]  [待加密明文字符串]
      组合使用参数-k，-v加密明文字符串,-k后输入8位纯大写字母的口令
Expect      :
    1.执行失败，报错提示口令要至少包含3种类型字符
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0032 start')
        self.dbuserNode = Node('PrimaryDbUser')

    def test_gs_encrypt(self):
        self.logger.info('-----------进行加密操作------------')
        step = "step1:执行命令,组合使用参数-k，-v加密明文字符串,-k后输入8位纯" \
               "大写字母口令   except:执行失败，报错提示口令要至少包含3种类型" \
               "字符"
        self.logger.info(step)
        str1 = 'test'
        encrypt = 'HHHHHHHH'
        vec = '1234567891236548'
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt -k {encrypt} -v {vec} {str1}'''
        self.logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        self.logger.info("--------加密结果---------")
        self.logger.info(msg1)
        self.assertIn('Invalid password,it must contain at least three kinds'
                      ' of characters', msg1, "执行失败" + step)

    def tearDown(self):
        self.logger.info('--------无需清理环境--------')
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0032 finish')

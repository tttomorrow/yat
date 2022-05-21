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
Case Name   : gs_encrypt工具组合使用参数-k，-D加密明文字符串
Description :
    1.生成输入16位字符串以base64方式编码后的密文:
      base64.b64encode([用户输入的16位字符串].encode(encoding='utf-8'))
    2.执行命令:
      gs_encrypt -k [用户输入的口令] -D [用户输入16位字符串编码后的密文]
      [待加密明文字符串]    组合使用参数-k,-D加密明文字符串
Expect      :
    1.成功生成密文；
    2.执行成功，输出加密后的密文
History     :
"""

import unittest
import base64
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0013 start')
        self.dbuserNode = Node('PrimaryDbUser')
        self.str = 'test'
        self.encrypt = 'jjGG￥￥55'
        self.rand = '1234567891234567'

    def test_gs_encrypt(self):
        self.logger.info('-----进行加密操作-----')
        step = "step1:生成输入16位字符串以base64方式编码的密文" \
               "except:成功生成密文"
        self.logger.info(step)
        self.enc = self.rand.encode(encoding='utf-8')
        self.vec = base64.b64encode(self.enc)
        self.assertEqual(type(self.vec), bytes, "生成失败" + step)

        step = "step2:执行命令,组合使用参数-k,-D加密明文字符串 " \
               "except:执行成功，输出加密后的密文"
        self.logger.info(step)
        self.vec_spl = str(self.vec).split("'")[1]
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt -k {self.encrypt} -D {self.vec_spl} {self.str}'''
        self.logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        self.logger.info("------------加密结果-----------")
        self.logger.info(msg1)
        self.assertEqual(len(msg1), 64, "执行失败" + step)

    def tearDown(self):
        self.logger.info('-----无需清理环境-----')
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0013 finish')

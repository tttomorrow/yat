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
Case Name   : gs_encrypt工具使用参数-B，-D加明文字符串，-D后输入长度为20的字符串
Description :
    1.生成以base64方式编码的密钥；
      base64.b64encode([用户输入的口令].encode(encoding='utf-8'))
    2.生成20位字符串以base64方式编码后的密文；
      base64.b64encode([用户输入的20位字符串].encode(encoding='utf-8'))
    3.执行命令:
      gs_encrypt -B [用户输入口令加密的密文] -D [用户输入字符串加密的密文]
      [待加密明文字符串]
      使用-B，-D参数加密明文字符串
Expect      :
    1.成功生成密钥；
    2.成功生成密文；
    3.执行失败，报错提示输入字符串的长度必须为16
History     :
"""

import os
import base64
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class GsEncrypt58(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'{os.path.basename(__file__)[:-3]}' + ' start')
        self.dbuserNode = Node('PrimaryDbUser')

    def test_gs_encrypt(self):
        self.logger.info('----进行加密操作----')
        step = "step1-2:生成以base64方式编码的密钥,生成以base64方式编码的20位" \
               "字符串密文  except:成功生成密钥，成功生成密文"
        self.logger.info(step)
        str1 = 'test'
        encrypt = '##ffFF12'
        rand = '12345678911111111111'
        enc = encrypt.encode(encoding='utf-8')
        enc1 = rand.encode(encoding='utf-8')
        key = base64.b64encode(enc)
        vec = base64.b64encode(enc1)
        self.assertEqual(type(key), bytes, step)
        self.assertEqual(type(vec), bytes, step)

        step = "step3:执行命令，使用-B，-D参数加密明文字符串 except:执行失败，" \
               "报错提示输入字符串的长度必须为16"
        self.logger.info(step)
        key_spl = str(key).split("'")[1]
        vec_spl = str(vec).split("'")[1]
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt -B {key_spl} -D {vec_spl}  {str1}'''
        self.logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        self.logger.info("----加密结果----")
        self.logger.info(msg1)
        self.assertIn('gs_encrypt: the decoded length of vector must be equal'
                      ' to 16.', msg1, "执行失败" + step)

    def tearDown(self):
        self.logger.info('----无需清理环境----')
        self.logger.info(f'{os.path.basename(__file__)[:-3]}' + ' finish')

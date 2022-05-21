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
Case Name   : gs_encrypt工具组合使用参数-k，-v，-D加密明文字符串
Description :
    1.生成16位字符串以base64方式编码后的密文:
      base64.b64encode([用户输入的16位字符串].encode(encoding='utf-8'))
    2.执行命令:
      gs_encrypt -k [用户输入的口令] -v [用户输入的盐值] -D
      [用户输入的16位字符串]  [待加密明文字符]
      组合使用参数-k，-v，-D加密明文字符串
Expect      :
    1.成功生成密钥；
    2.执行成功，输出加密后的密文
History     :
"""
import base64
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0019 start')
        self.dbuserNode = Node('PrimaryDbUser')

    def test_gs_encrypt(self):
        self.logger.info('-----进行加密操作-----')
        step = "step1:生成16位字符串以base64方式编码后的密文 except:成功生成密" \
               "文"
        self.logger.info(step)
        str1 = 'test'
        encrypt = 'kkk##HH5'
        ran = 'kj#HH4kkjjjjjj55'
        enc = ran.encode(encoding='utf-8')
        vec = base64.b64encode(enc)
        self.assertEqual(type(vec), bytes, step)

        step = "step2:执行命令，组合使用参数-k，-v，-D加密明文字符串 except:执" \
               "行成功，输出加密后的密文"
        self.logger.info(step)
        vec_spl = str(vec).split("'")[1]
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt -k {encrypt} -v {ran} -D {vec_spl}  \
            {str1}'''
        self.logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        self.logger.info("-----加密结果-----")
        self.logger.info(msg1)
        self.assertEqual(len(msg1), 64, "执行失败" + step)

    def tearDown(self):
        self.logger.info('-----无需清理环境-----')
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0019 finish')

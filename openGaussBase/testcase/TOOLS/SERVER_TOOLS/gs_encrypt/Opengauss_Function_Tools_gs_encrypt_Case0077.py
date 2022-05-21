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
Case Name   : gs_encrypt工具组合使用参数--key，--vector，--vector-base64
            加密明文字符串
Description :
    1.生成16位字符串以base64方式编码后的密文；
      base64.b64encode([用户输入的16位字符串].encode(encoding='utf-8'))
    2.执行命令，组合使用参数--key，--vector，--vector-base64加密明文字符串
      gs_encrypt --key=[用户输入的口令] --vector=[用户输入的盐值]
      --vector-base64=[用户输入的16位字符串]  [待加密明文字符]
Expect      :
    1.成功生成密钥；
    2.执行成功，输出加密后的密文
History     :
"""

import os
import base64
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger


class GsEncrypt60(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.dbuserNode = Node('PrimaryDbUser')
        self.common = Common()

    def test_gs_encrypt(self):
        self.logger.info('-----进行加密操作-----')
        step = "step1:生成16位字符串以base64方式编码后的密文  " \
               "except:成功生成密文"
        self.logger.info(step)
        str1 = 'test'
        encrypt = 'kkk##HH5'
        ran = 'kj#HH4kkjjjjjj55'
        enc = ran.encode(encoding='utf-8')
        vec = base64.b64encode(enc)
        self.assertEqual(type(vec), bytes, step)

        step = "step2:执行命令，组合使用参数--key，--vector，--vector-base64" \
               "加密明文字符串 except:执行成功，输出加密后的密文"
        self.logger.info(step)
        vec_spl = str(vec).split("'")[1]
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt --key={encrypt} --vector={ran} \
            --vector-base64={vec_spl} {str1}'''
        self.logger.info(check_cmd1)
        self.logger.info("-----加密结果-----")
        msg1 = self.common.get_sh_result(self.dbuserNode, check_cmd1)
        self.assertEqual(len(msg1), 64, "执行失败" + step)

    def tearDown(self):
        self.logger.info('-----无需清理环境-----')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

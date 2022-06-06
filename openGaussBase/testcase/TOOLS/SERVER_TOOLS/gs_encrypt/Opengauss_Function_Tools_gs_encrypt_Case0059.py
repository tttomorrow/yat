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
Case Name   : gs_encrypt工具频繁执行，验证可靠性
Description :
    1.执行命令:
      gs_guc generate -S [用户输入的口令] -D [$GAUSSHOME/bin命令] -o
      [用户输入的加密文件前缀名]
      生成加密文件cipher，rand到$GAUSSHOME/bin目录下;
    2.执行命令：
      gs_encrypt -f [用户输入的加密文件前缀名] [待加密明文字符串]
      使用-f参数加密明文字符串；
    3.重复步骤2 100次
    4.清理环境
Expect      :
    1.成功生成文件；
    2.执行成功，输出加密后的密文；
    3.执行成功，通过率100%
    4.清理环境成功
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class GsEncrypt59(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'{os.path.basename(__file__)[:-3]}' + ' start')
        self.dbuserNode = Node('PrimaryDbUser')
        self.prefix = 'test'
        self.file_path = os.path.join(os.path.dirname(macro.DB_INSTANCE_PATH),
                                      'app', 'bin')
        self.cipher_path = os.path.join(self.file_path, f'{self.prefix}.key.'
                                        f'cipher')
        self.rand_path = os.path.join(self.file_path, f'{self.prefix}.key.'
                                      f'rand')

    def test_gs_encrypt(self):
        step = "step1:执行命令，在$GAUSSHOME/bin目录下生成加密文件cipher，" \
               "rand except:成功生成文件"
        self.logger.info(step)
        encrypt = 'ddFF##55'
        check_cmd1 = f''' source {macro.DB_ENV_PATH};
            gs_guc generate -S {encrypt} -D {self.file_path} -o \
            {self.prefix};
            ls {self.file_path}'''
        self.logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(f'{self.prefix}.key.cipher' in msg1
                        and f'{self.prefix}.key.rand' in msg1,
                        "生成失败" + step)

        step = "step2-3:执行命令，使用-f参数加密明文字符串,重复步骤2 100次 " \
               "expect:执行成功，通过率100%"
        for i in range(1, 101):
            self.logger.info('-----进行加密操作-----')
            check_cmd1 = f'''source {macro.DB_ENV_PATH};
                gs_encrypt -f {self.prefix} {self.prefix}'''
            self.logger.info(check_cmd1)
            msg1 = self.dbuserNode.sh(check_cmd1).result()
            self.logger.info('-----加密结果-----')
            self.logger.info(msg1)
            self.assertEqual(len(msg1), 64, "执行失败" + step)

    def tearDown(self):
        step = 'step4:清理环境 except:成功'
        self.logger.info(step)
        del_file = f'''rm -rf {self.cipher_path};
            rm -rf {self.rand_path}'''
        self.dbuserNode.sh(del_file).result()
        self.logger.info(del_file)
        self.assertFalse(os.path.isfile(self.cipher_path), "清理失败" + step)
        self.assertFalse(os.path.isfile(self.rand_path), "清理失败" + step)
        self.logger.info('-----清理完成-----')
        self.logger.info(f'{os.path.basename(__file__)[:-3]}' + ' finish')

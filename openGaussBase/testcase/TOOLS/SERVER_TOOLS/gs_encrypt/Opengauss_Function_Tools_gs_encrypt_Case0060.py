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
Case Name   : gs_encrypt工具显示帮助信息(正常)
Description :
    1.执行命令查看帮助信息
      gs_encrypt --help 查看帮助信息
Expect      :
    1.显示详细的帮助信息
History     :
"""

import re
import os
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
        self.logger.info('-----显示帮助信息-----')
        step = 'step1:执行命令,查看帮助信息  except:显示详细的帮助信息'
        self.logger.info(step)
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt --help '''
        self.logger.info(check_cmd1)
        msg1 = self.common.get_sh_result(self.dbuserNode, check_cmd1)
        expect = r'Usage:.*gs_encrypt \[OPTION\]... PLAINTEXT.*' \
            r'General options:.*-?, --help.*show this help, then exit..*' \
            r'-V, --version.*output version information, then exit..*' \
            r'-k, --key=PASSWORD.*the password for AES128..*' \
            r'-v, --vector=VectorValue.*the random vector for AES128..*' \
            r'-f, --file-prefix=FilePrefix.*the cipher files prefix..*' \
            r'-B, --key-base64=Value.*the key value encoded in base64..*' \
            r'-D, --vector-base64=Value.*the random value encoded in base64..*'\
            r'PLAINTEXT.*the plain text you want to encrypt'
        reg_res = re.search(expect, msg1, re.S)
        self.logger.info(reg_res)
        self.assertIsNotNone(reg_res, step)

    def tearDown(self):
        self.logger.info('-----无需清理环境-----')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

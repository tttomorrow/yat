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
Case Name   : gs_encrypt工具显示版本信息(异常)
Description :
    1.执行命令查看版本信息
      gs_encrypt --v
Expect      :
    1.执行失败,合理报错
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger


class GsEncrypt62(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.dbuserNode = Node('PrimaryDbUser')
        self.common = Common()

    def test_gs_encrypt(self):
        self.logger.info('-----显示版本信息-----')
        step = "step1:执行命令查看版本信息  except:执行失败,合理报错"
        self.logger.info(step)
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt --v '''
        self.logger.info(check_cmd1)
        msg1 = self.common.get_sh_result(self.dbuserNode, check_cmd1)
        list1 = ["'--v' is ambiguous", '--version', '--vector-base64',
                 '--vector']
        for i in list1:
            self.assertIn(i, msg1, "执行失败" + step)

    def tearDown(self):
        self.logger.info('-----无需清理环境-----')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

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
Case Name   : 检查系统控制参数
Description :
    检查系统控制参数
Expect      :
    检查完成
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_Tools_gs_checkos_Case0016start-------------------')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools(self):
        logger.info('------------------root用户检查系统控制参数------------------')
        checkos_cmd = f'''
                            source {macro.DB_ENV_PATH}
                            gs_checkos -i  A6
                            '''
        logger.info(checkos_cmd)
        msg = self.rootNode.sh(checkos_cmd).result()
        logger.info(msg)
        logger.info('--------------解析执行结果---------------')
        str_1 = msg.split('\n')
        logger.info(str_1)
        str_list = []
        if len(str_1) > 2:
            str_list = str_1[1].split(':')
            logger.info(str_list)
            logger.info('--------------校验结果---------------')
            self.assertEqual(len(str_list), 2, '结果验证失败1')
            self.assertEqual(str_list[0].strip(), 'A6. [ System control parameters status ]', '结果验证失败3')
            i = str_list[1].strip()
            self.assertTrue(i in ['Normal', 'Warning'], f'状态验证失败，当前状态：{i}')
        else:
            raise Exception("解析结果异常")

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_checkos_Case0016finish------------------')
"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Name   : 设置系统控制参数，设置预读块大小值
Description : 设置系统控制参数，设置预读块大小值
Expect      : 设置成功
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
        logger.info('--Opengauss_Function_Tools_gs_checkos_Case0075start--')
        self.rootnode = Node('default')
        self.constant = Constant()

    def test_server_tools(self):
        logger.info('-------root用户设置系统控制参数，设置预读块大小值-------')
        checkos_cmd = f'''source {macro.DB_ENV_PATH};
            gs_checkos -i  B1,B3
            '''
        logger.info(checkos_cmd)
        checkos_msg = self.rootnode.sh(checkos_cmd).result()
        logger.info(checkos_msg)
        logger.info('--------------解析执行结果---------------')
        checkos_str = checkos_msg.splitlines()
        logger.info(checkos_str)
        status_list = []
        num_list = []
        logger.info('--------------提取选项信息---------------')
        for i in checkos_str:
            if '[' in i and ']' in i:
                num_list.append(i.split('.')[0].strip())
        logger.info(num_list)
        logger.info('--------------提取状态信息---------------')
        for j in checkos_str:
            if '[' in j and ']' in j:
                status_list.append(j.split(':')[-1].strip())
        logger.info(status_list)

        logger.info('---断言，判断选项信息是否正确，判断状态信息是否正常---')
        self.assertEqual(len(num_list), 2)
        self.assertIn(num_list[0], self.constant.GS_CHECKOS_SUCCESS_MSG2)
        self.assertEqual(len(status_list), 2)
        for i in status_list:
            self.assertTrue(i in ['Normal', 'Warning'], f'状态验证\
            失败，当前状态：{i}')

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('--Opengauss_Function_Tools_gs_checkos_Case0075finish--')


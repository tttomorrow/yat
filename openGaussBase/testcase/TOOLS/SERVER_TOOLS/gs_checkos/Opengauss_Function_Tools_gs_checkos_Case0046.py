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
Case Name   : 检查open gaussXML配置文件
Description : 检查open gaussXML配置文件
Expect      : 检查完成
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Tools_gs_checkos_Case0046_start----')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools1(self):
        if os.path.exists(f'{macro.DB_XML_PATH}'):
            text = '-----step1:检查open gaussXML配置文件;expect:检查完成-----'
            self.log.info(text)
            check_cmd = f'source {macro.DB_ENV_PATH};' \
                f'gs_checkos ' \
                f'-i A ' \
                f'-X {macro.DB_XML_PATH};'
            self.log.info(check_cmd)
            msg = self.rootNode.sh(check_cmd).result()
            self.log.info(msg)
            self.log.info('--------------解析执行结果---------------')
            str_1 = msg.splitlines()
            self.log.info(str_1)
            status_list = []
            num_list = []
            self.log.info('--------------提取选项信息---------------')
            for i in str_1:
                if '[' in i and ']' in i:
                    num_list.append(i.split('.')[0].strip())
            self.log.info(num_list)
            self.log.info('--------------提取状态信息---------------')
            for j in str_1:
                if '[' in j and ']' in j:
                    status_list.append(j.split(':')[-1].strip())
            self.log.info(status_list)
            text = '---断言，判断选项信息是否正确，判断状态信息是否正常---'
            self.log.info(text)
            self.assertEqual(self.Constant.GS_CHECKOS_SUCCESS_MSG1, num_list)
            tmp_list = zip(num_list, status_list[:14:])
            self.log.info('tmp_list------')
            for arg in tmp_list:
                self.log.info(arg)
                self.assertIn(arg[-1].strip(),
                              ['Normal', 'Abnormal', 'Warning'],
                              '执行失败' + text)
        else:
            self.log.info('xml配置文件不存在')

    def tearDown(self):
        self.log.info('--------------无需清理环境-------------------')
        self.log.info(
            '----Opengauss_Function_Tools_gs_checkos_Case0046_finish----')

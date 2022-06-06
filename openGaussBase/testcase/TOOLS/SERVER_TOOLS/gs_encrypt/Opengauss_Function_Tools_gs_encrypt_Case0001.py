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
    1.执行命令:
      gs_encrypt -?  查看帮助信息
Expect      :
    1.显示详细的帮助信息
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0001 start')
        self.dbuserNode = Node('PrimaryDbUser')

    def test_gs_encrypt(self):
        self.logger.info('-----显示帮助信息-----')
        step = 'step1:执行命令,查看帮助信息  except:显示详细的帮助信息'
        self.logger.info(step)
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_encrypt -? '''
        self.logger.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-----截取General options部分的语法-----')
        start_index1 = msg1.find('General options:')
        self.logger.info('定义一个空的列表，将获取的参数写入，打印出该列表')
        options_list1 = []
        for i in msg1[start_index1:].splitlines():
            for j in i.split(' '):
                if len(j) == 2 and j[0] == '-':
                    options_list1.append(j)
        self.logger.info('-----打印列表信息-----')
        self.logger.info(options_list1)
        parameter = ['-?', '-V', '-k', '-v,', '-f', '-B', '-D']
        self.assertEqual(options_list1.sort(), parameter.sort(),
                         "执行失败" + step)

    def tearDown(self):
        self.logger.info('-----无需清理环境-----')
        self.logger.info('Opengauss_Function_Tools_gs_encrypt_Case0001 finish')

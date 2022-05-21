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
Case Type   : tools
Case Name   : 执行初始化数据库命令gs_initdb：系统默认区域的编码格式和用--encoding参数指
                定的编码格式不匹配
Description :
    1.执行命令：gs_initdb -D $data/ --nodename=single --locale=yo_NG.utf8
    --encoding=EUC_CN
Expect      :
    1.初始化失败，返回的提示信息中有告知The encoding you selected (EUC_CN) and the
     encoding that the selected locale uses (UTF8) do not match
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('----Opengauss_Function_gs_initdb_Case0012 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH, 'datadir')

    def test_systools(self):
        self.logger.info('--------执行gs_initdb命令--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_initdb -D ' \
                      f'{self.dir_path} --nodename=single -w ' \
                      f'{self.userNode.ssh_password} --locale=yo_NG.utf8 ' \
                      f'--encoding=EUC_CN'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find('The encoding you selected (EUC_CN) and '
                                  'the encoding that the\n'
                                  'selected locale uses'
                                  ' (UTF8) do not match') > -1)
        self.logger.info('-------未生成datadir目录-------')
        excute_cmd2 = f'ls {self.dir_path}'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(msg2.find('No such file or directory') > -1)

    def tearDown(self):
        self.logger.info('---Opengauss_Function_gs_initdb_Case0012 finish---')


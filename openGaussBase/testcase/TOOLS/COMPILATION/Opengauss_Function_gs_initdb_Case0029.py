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
Case Type   : tools
Case Name   : 执行初始化数据库命令gs_initdb：指定参数--xlogdir，所设置的目录不为空目录
Description :
    1.执行命令：gs_initdb -D $data/ --nodename=single --xlogdir=$logdir
Expect      :
    1.初始化成功，在$logdir目录下生成日志文件
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
        self.logger.info('----Opengauss_Function_gs_initdb_Case0029 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH, 'datadir')
        self.log_path = os.path.join(macro.DB_INSTANCE_PATH, 'logdir')
        self.filename = os.path.join(self.log_path, 'wftest.txt')

    def test_systools(self):
        self.logger.info('------执行gs_initdb命令------')
        excute_cmd1 = f'mkdir {self.log_path};touch {self.filename};' \
                      f'{self.log_path};source {self.DB_ENV_PATH};' \
                      f'gs_initdb -D {self.dir_path} --nodename=single -w' \
                      f' {self.userNode.ssh_password} ' \
                      f'--xlogdir={self.log_path}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find('exists but is not empty') > -1)
        self.logger.info('--------生成datadir目录--------')
        excute_cmd2 = f'ls {self.dir_path}'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue('No such file or directory' in msg2)

    def tearDown(self):
        self.logger.info('------------清理环境------------')
        excute_cmd1 = f'rm -rf {self.log_path};ls {self.dir_path}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find('No such file or directory') > -1)
        self.logger.info('---Opengauss_Function_gs_initdb_Case0029 finish---')

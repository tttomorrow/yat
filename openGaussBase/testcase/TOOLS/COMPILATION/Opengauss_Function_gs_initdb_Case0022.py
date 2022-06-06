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
Case Name   : 执行初始化数据库命令gs_initdb：指定参数--pwfile，
                指定的文件第一行为非数据库初始用户密码
Description :
    1.在指定路径下创建一个文件，命名为wf.txt(自定义)，文件第一行为非数据库初始用户密码，
    且非空，执行命令：gs_initdb -D $data/ --nodename=single  --pwfile=$wf.txt
Expect      :
    1.初始化成功
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
        self.logger.info('----Opengauss_Function_gs_initdb_Case0022 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.dir_path1 = os.path.join(macro.DB_INSTANCE_PATH, 'datadir1')
        self.file = os.path.join(macro.DB_INSTANCE_PATH, 'wf.txt')

    def test_systools(self):
        self.logger.info('---------创建文件，写入密码---------')
        excute_cmd0 = f'touch {self.file};' \
                      f'echo "{macro.COMMON_PASSWD}" >> {self.file};'
        self.logger.info(excute_cmd0)
        msg0 = self.userNode.sh(excute_cmd0).result()
        self.logger.info(msg0)
        self.logger.info('------执行gs_initdb命令------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_initdb -D ' \
                      f'{self.dir_path1} --nodename=single ' \
                      f'--pwfile={self.file}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(
            msg1.find('Success. You can now start the database server') > -1)
        self.logger.info('--------生成datadir目录--------')
        excute_cmd2 = f'ls {self.dir_path1}'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue('postgresql.conf' in msg2 and 'pg_hba.conf' in msg2)

    def tearDown(self):
        self.logger.info('-----------清理环境-----------')
        excute_cmd1 = f'rm -rf {self.dir_path1};ls {self.dir_path1}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find('No such file or directory') > -1)
        excute_cmd2 = f'rm -rf {self.file};ls {self.dir_path1}'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(msg2.find('No such file or directory') > -1)
        self.logger.info('---Opengauss_Function_gs_initdb_Case0022 finish---')

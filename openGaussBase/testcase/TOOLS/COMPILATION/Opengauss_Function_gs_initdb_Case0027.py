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
Case Name   : 执行初始化数据库命令gs_initdb：指定参数--enpwdfiledir
Description :
    1.在自定义路径$path下执行gs_guc encrypt -K $password -D $path,password为系统
    管理员用户的密码，path为自定义路径,path必须是一个目录
    2.执行命令：gs_initdb -D $data/ --nodename=single  --enpwdfiledir=$path
Expect      :
    1.在$path路径下生成密钥文件 server.key.cipher和server.key.rand
    2.初始化成功，初始化过程中无需输入密码
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
        self.logger.info('----Opengauss_Function_gs_initdb_Case0027 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.dir_path1 = os.path.join(macro.DB_INSTANCE_PATH, 'datadir1')
        self.dir_path2 = os.path.join(macro.DB_INSTANCE_PATH, 'datadir2')

    def test_systools(self):
        self.logger.info('------生成密钥文件------')
        excute_cmd0 = f'mkdir {self.dir_path2};source {self.DB_ENV_PATH};' \
                      f'gs_guc encrypt -K {self.userNode.ssh_password} ' \
                      f'-D {self.dir_path2}'
        self.logger.info(excute_cmd0)
        msg0 = self.userNode.sh(excute_cmd0).result()
        self.logger.info(msg0)
        self.logger.info('------执行gs_initdb命令------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_initdb -D ' \
                      f'{self.dir_path1} --nodename=single ' \
                      f'--enpwdfiledir={self.dir_path2}'
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
        self.logger.info('------------清理环境------------')
        excute_cmd1 = f'rm -rf {self.dir_path1};ls {self.dir_path1}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find('No such file or directory') > -1)
        excute_cmd2 = f'rm -rf {self.dir_path2};ls {self.dir_path2}'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue(msg2.find('No such file or directory') > -1)
        self.logger.info('---Opengauss_Function_gs_initdb_Case0027 finish---')

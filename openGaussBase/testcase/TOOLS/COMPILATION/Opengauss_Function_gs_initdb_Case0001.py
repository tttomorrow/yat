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
Case Name   : 执行初始化数据库命令gs_initdb：指定数据目录的位置
Description :
    1.执行命令：gs_initdb -D $data/ --nodename=single
Expect      :
    1.在data目录下生成初始化后的文件
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
        self.logger.info('----Opengauss_Function_gs_initdb_Case0001 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH, 'datadir')

    def test_systools(self):
        self.logger.info('--------执行gs_initdb命令--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_initdb -D ' \
                      f'{self.dir_path} --nodename=single -w ' \
                      f'{self.userNode.ssh_password}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find(
            'Success. You can now start the database server of single node'))
        self.logger.info('--------查看初始化生成的目录--------')
        excute_cmd2 = f'ls {self.dir_path}'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertTrue('postgresql.conf' in msg2 and 'pg_hba.conf' in msg2)

    def tearDown(self):
        self.logger.info('-----------清理环境-----------')
        excute_cmd1 = f'rm -rf {self.dir_path};ls {self.dir_path}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find('No such file or directory') > -1)
        self.logger.info('---Opengauss_Function_gs_initdb_Case0001 finish---')

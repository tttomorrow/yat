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
Case Name   : 执行初始化数据库命令gs_initdb：指定参数--debug (单机)
Description :
    1.执行命令：单机：gs_initdb -D $data/ --nodename=single -w $password --debug
    2.查询data目录下的文件
Expect      :
    1.初始化成功，且打印出Running in debug mode等信息
    2.data目录下有文件生成，如postgresql.conf文件
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

Primary_SH = CommonSH('PrimaryDbUser')


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('----Opengauss_Function_gs_initdb_Case0031 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH, 'datadir')

    def test_systools(self):
        self.logger.info('------执行gs_initdb命令------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_initdb -D {self.dir_path} --nodename=single -w' \
                      f' {self.userNode.ssh_password} --locale=es_US.UTF-8 ' \
                      f'--debug'
        self.logger.info(excute_cmd1)
        self.userNode.sh(excute_cmd1).result()
        self.logger.info('--------生成datadir目录---------')
        excute_cmd3 = f'ls {self.dir_path}'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue('postgresql.conf' in msg3 and 'pg_hba.conf' in msg3)

    def tearDown(self):
        self.logger.info('-----------清理环境-----------')
        excute_cmd1 = f'rm -rf {self.dir_path};ls {self.dir_path}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find('No such file or directory') > -1)
        self.logger.info('---Opengauss_Function_gs_initdb_Case0031 finish---')

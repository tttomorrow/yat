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
Case Name   : 初始化数据库gs_initdb：本地用户通过TCP/IP连接数据库时的认证方法为md5
Description :
    1.执行命令：gs_initdb -D $data/ --nodename=single -w $password
    --auth-host=md5
Expect      :
    1.在data目录下生成初始化后的文件,pg_hba.conf文件中，host行认证方法为md5
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
        self.logger.info('----Opengauss_Function_gs_initdb_Case0039 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH, 'datadir')

    def test_systools(self):
        self.logger.info('------执行gs_initdb命令------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_initdb -D {self.dir_path} --nodename=single -w' \
                      f' {self.userNode.ssh_password} --auth-host=md5'
        self.logger.info(excute_cmd1)
        msg2 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg2)
        self.assertTrue(
            msg2.find('Success. You can now start the database server') > -1)
        self.logger.info('--------生成datadir目录--------')
        excute_cmd3 = f'ls {self.dir_path}'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue('postgresql.conf' in msg3 and 'pg_hba.conf' in msg3)
        self.logger.info('--------查看认host证方法为md5--------')
        pg_file = os.path.join(self.dir_path, 'pg_hba.conf')
        excute_cmd4 = f'cat {pg_file} |grep "^host"'
        self.logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.assertTrue(msg4.count('md5') >= 2)
        self.logger.info('--------查看认local证方法默认为trust--------')
        pg_file = os.path.join(self.dir_path, 'pg_hba.conf')
        excute_cmd4 = f'cat {pg_file} |grep "local"'
        self.logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.assertTrue(msg4.count('trust') >= 1)

    def tearDown(self):
        self.logger.info('-----------清理环境-----------')
        excute_cmd1 = f'rm -rf {self.dir_path};ls {self.dir_path}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.assertTrue(msg1.find('No such file or directory') > -1)
        self.logger.info('---Opengauss_Function_gs_initdb_Case0039 finish---')

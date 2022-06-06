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
Case Name   : 执行初始化数据库命令gs_initdb：指定参数--lc-ctype，--lc-monetary，
                --lc-numeric，--lc-time
Description :
    1.执行命令：gs_initdb -D $data2/ --nodename=single -w $passwd
    --lc-monetary=yo_NG.utf8
    2.执行命令：gs_initdb -D $data3/ --nodename=single -w $passwd
    --lc-numeric=yo_NG.utf8
    3.执行命令：gs_initdb -D $data4/ --nodename=single -w $passwd
    --lc-time=yo_NG.utf8
Expect      :
    1.初始化成功，且$data2目录生成文件，打印 MONETARY: yo_NG.utf8信息
    2.初始化成功，且$data3目录生成文件
    3.初始化成功，且$data4目录生成文件
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
        self.logger.info('----Opengauss_Function_gs_initdb_Case0019 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.dir_path1 = os.path.join(macro.DB_INSTANCE_PATH, 'datadir1')
        self.dir_path2 = os.path.join(macro.DB_INSTANCE_PATH, 'datadir2')
        self.dir_path3 = os.path.join(macro.DB_INSTANCE_PATH, 'datadir3')

    def test_systools(self):
        self.logger.info('--------执行gs_initdb命令,参数"--lc-monetary"--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_initdb -D ' \
                      f'{self.dir_path1} --nodename=single -w ' \
                      f'{self.userNode.ssh_password} --lc-monetary=yo_NG.utf8'
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
        self.logger.info('--------执行gs_initdb命令,参数"--lc-numeric"--------')
        excute_cmd3 = f'source {self.DB_ENV_PATH};gs_initdb -D ' \
                      f'{self.dir_path2} --nodename=single -w ' \
                      f'{self.userNode.ssh_password} --lc-numeric=yo_NG.utf8'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(
            msg3.find('Success. You can now start the database server') > -1)
        self.logger.info('--------生成datadir目录--------')
        excute_cmd4 = f'ls {self.dir_path2}'
        self.logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        self.logger.info(msg4)
        self.assertTrue('postgresql.conf' in msg4 and 'pg_hba.conf' in msg4)
        self.logger.info('--------执行gs_initdb命令,参数"--lc-time"--------')
        excute_cmd5 = f'source {self.DB_ENV_PATH};gs_initdb -D ' \
                      f'{self.dir_path3} --nodename=single -w ' \
                      f'{self.userNode.ssh_password} --lc-time=yo_NG.utf8'
        self.logger.info(excute_cmd5)
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.logger.info(msg5)
        self.assertTrue(
            msg5.find('Success. You can now start the database server') > -1)
        self.logger.info('--------生成datadir目录--------')
        excute_cmd6 = f'ls {self.dir_path3}'
        self.logger.info(excute_cmd6)
        msg6 = self.userNode.sh(excute_cmd6).result()
        self.logger.info(msg6)
        self.assertTrue('postgresql.conf' in msg6 and 'pg_hba.conf' in msg6)

    def tearDown(self):
        self.logger.info('-----------清理环境-----------')
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
        excute_cmd3 = f'rm -rf {self.dir_path3};ls {self.dir_path3}'
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find('No such file or directory') > -1)
        self.logger.info('---Opengauss_Function_gs_initdb_Case0019 finish---')

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
Case Name   : 执行初始化数据库命令gs_initdb：指定参数--noclean
Description :
    1.在/home路径下创建一个文件，命名为wf.txt(自定义)，文件第为空
    2.执行命令：gs_initdb -D $data/ --nodename=single --pwfile=home/wf.txt 
    --noclean
Expect      :
    1-2.初始化失败,密码文件为空，但data目录及其内容没有被删除
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')
Logger = Logger()


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        Logger.info('----Opengauss_Function_gs_initdb_Case0032 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH, 'datadir')
        self.file_name = os.path.join(macro.DB_INSTANCE_PATH, 'wf.txt')

    def test_systools(self):
        Logger.info('------执行gs_initdb命令------')
        excute_cmd1 = f'touch {self.file_name};' \
                      f'source {self.DB_ENV_PATH};' \
                      f'gs_initdb -D {self.dir_path} --nodename=single ' \
                      f'--pwfile={self.file_name} --noclean'
        Logger.info(excute_cmd1)
        msg2 = self.userNode.sh(excute_cmd1).result()
        Logger.info(msg2)
        Logger.info('--------初始化失败，但是目录未自动删除--------')
        self.assertTrue(msg2.find('not removed at user\'s request') > -1)
        excute_cmd3 = f'ls {self.dir_path}'
        Logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        Logger.info(msg3)
        self.assertTrue('postgresql.conf' in msg3 and 'pg_hba.conf' in msg3)

    def tearDown(self):
        Logger.info('-----------清理环境-----------')
        excute_cmd1 = f'rm -rf {self.dir_path};ls {self.dir_path}'
        Logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        Logger.info(msg1)
        self.assertTrue(msg1.find('No such file or directory') > -1)
        excute_cmd2 = f'rm -rf {self.file_name};ls {self.file_name}'
        Logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        Logger.info(msg2)
        self.assertTrue(msg2.find('No such file or directory') > -1)
        Logger.info('---Opengauss_Function_gs_initdb_Case0032 finish---')

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
Case Name   : 启动gaussdb进程时，使用-?参数是否显示正确帮助信息
Description :
    1.使用gaussdb工具显示正确帮助信息
    gaussdb -?
    2.检查打印信息是否正确无误
    3.使用gaussdb工具显示正确帮助信息
    gaussdb -?
    4.检查打印信息是否正确无误
Expect      :
    1.使用gaussdb工具显示正确帮助信息成功
    2.打印信息正确无误
    3.使用gaussdb工具显示正确帮助信息成功
    4.打印信息正确无误
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_Gaussdb_Case0052 start--')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_systools(self):
        self.logger.info('--------执行gaussdb查看帮助信息--------')
        help_msg = ["-B NBUFFERS", "-b BINARY UPGRADES flag used for binary",
                    "-c NAME=VALUE", "-C NAM", "-d 1-5", "-D DATADIR", "-e",
                    "-F", "-h HOSTNAME", "-i", "-k", "-l",
                    "-N", "-M SERVERMODE", "-o OPTIONS", "-p PORT",
                    "-s", "-S WORK-MEM", "-u NUM", "-V, --version",
                    "--NAME=VALUE", "--describe-config", "--securitymode",
                    "--single_node", "-?, --help", "-f", "-n", "-O", "-P",
                    "-t pa|pl|ex", "-T", "-W NUM", "--localxid", "--single",
                    "DBNAME", "-d 0-5", "-E", "-j", "-r FILENAME", "--boot",
                    "-r FILENAME", "-x NUM", "--single_node"]
        excute_cmd1 = f'source {self.DB_ENV_PATH};gaussdb -?'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        for content in (help_msg):
            self.logger.info(content)
            self.assertTrue(msg1.find(content) > -1)
        self.logger.info('------使用gaussdb --help查看帮助信息------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};gaussdb --help'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        for content in (help_msg):
            self.logger.info(content)
            self.assertTrue(msg2.find(content) > -1)

    def tearDown(self):
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0052 finish-')

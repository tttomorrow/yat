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
Case Name   : 执行初始化数据库命令gs_initdb：指定参数--help
Description :
    1.执行命令：gs_initdb --help
Expect      :
    1.返回帮助信息
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger

Logger = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        Logger.info('----Opengauss_Function_gs_initdb_Case0035 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_systools(self):
        Logger.info('------执行gs_initdb命令------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_initdb --help'
        Logger.info(excute_cmd1)
        msg2 = self.userNode.sh(excute_cmd1).result()
        Logger.info(msg2)
        msg_list = ['-A, --auth=METHOD', '--auth-host=METHOD',
                    '--auth-local=METHOD', '[-D, --pgdata=]DATADIR',
                    '--nodename=NODENAME', '-E, --encoding=ENCODING',
                    '--locale=LOCALE', '--dbcompatibility=DBCOMPATIBILITY',
                    '--lc-collate=, --lc-ctype=, --lc-messages=LOCALE',
                    '--lc-monetary=, --lc-numeric=, --lc-time=LOCALE',
                    '--no-locale', '--pwfile=FILE', '-T',
                    '-U, --username=NAME', '-W, --pwprompt',
                    '-w, --pwpasswd=PASSWD', '-C, --enpwdfiledir=DIR',
                    '-X, --xlogdir=XLOGDIR', '-S, --security', '-d, --debug',
                    '-L DIRECTORY ', '-n, --noclean', '-s, --show',
                    '-H, --host-ip', '-V, --version', '-?, --help']
        for content in msg_list:
            self.assertTrue(msg2.find(content) > -1)

    def tearDown(self):
        Logger.info('---Opengauss_Function_gs_initdb_Case0035 finish---')

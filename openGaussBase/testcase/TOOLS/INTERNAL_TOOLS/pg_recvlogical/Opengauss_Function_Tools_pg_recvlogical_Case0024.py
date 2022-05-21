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
Case Type   : 系统内部使用工具
Case Name   : 逻辑复制pg_recvlogical 指定参数--help,输出帮助信息，随后立即退出
Description :
        1.指定参数--help,查看帮助信息
        pg_recvlogical --help
Expect      :
        1.输出版本信息，随后立即退出
History     :
"""
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Tools_pg_recvlogical_Case0024 start-')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')

    def test_standby(self):
        text = '--step1:逻辑复制pg_recvlogical 指定参数--help;' \
               'expect:输出帮助信息--'
        self.log.info(text)
        execute_cmd = f'source {macro.DB_ENV_PATH};' \
                      f'pg_recvlogical --help '
        self.log.info(execute_cmd)
        exec_msg = self.primary_node.sh(execute_cmd).result()
        self.log.info(exec_msg)
        msg_list = ['Options:', '-f, --file=FILE', '-n, --no-loop',
                    '-v, --verbose',
                    '-V, --version', '-?, --help', 'Connection options:',
                    '-d, --dbname=DBNAME', '-h, --host=HOSTNAME',
                    '-p, --port=PORT',
                    '-U, --username=NAME', '-w, --no-password',
                    '-W, --password',
                    'Replication options:', '-F  --fsync-interval=INTERVAL',
                    '-P, --plugin=PLUGIN', '-S, --slot=SLOT',
                    '-I, --startpos=PTR',
                    '-s, --status-interval=INTERVAL',
                    '-o, --option=NAME[=VALUE]',
                    'Action to be performed:', '--create', '--start', '--drop']
        for content in msg_list:
            self.assertTrue(exec_msg.find(content) > -1)

    def tearDown(self):
        self.log.info('--无需恢复环境--')
        self.log.info(
            '-Opengauss_Function_Tools_pg_recvlogical_Case0024 finish--')

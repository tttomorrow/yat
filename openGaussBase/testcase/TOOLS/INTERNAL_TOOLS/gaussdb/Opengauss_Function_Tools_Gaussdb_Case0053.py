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
Case Type   : 基础功能
Case Name   : 启动gaussdb进程时，使用--help参数是否显示正确帮助信息
Description :
    1.使用gaussdb工具显示正确帮助信息
Expect      :
    1.使用gaussdb工具显示正确帮助信息成功
History     :
"""
import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant


class Gaussdbclass(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("Opengauss_Function_Tools_Gaussdb_Case0053 start")
        self.constant = Constant()
        self.commonshpri = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.primary_user_node = Node(node='PrimaryDbUser')

    def test_gaussdb(self):
        text = '----step1: 初始化一个数据库&关闭正在运行的数据库 expect:成功----'
        self.log.info(text)
        cmd = f"source {macro.DB_ENV_PATH}; " \
            f"gaussdb --help"
        self.log.info(cmd)
        result = self.primary_user_node.sh(cmd).result()
        self.log.info(result)
        flg = ['-B NBUFFERS        number of shared buffers',
               '-b BINARY UPGRADES flag used for binary upgrades',
               '-c NAME=VALUE      set run-time parameter',
               '-C NAME            print value of run-time parameter, '
               'then exit',
               '-d 1-5             debugging level',
               '-D DATADIR         database directory',
               '-e                 use European date input format (DMY)',
               '-F                 turn fsync off',
               '-h HOSTNAME        host name or IP address to listen on',
               '-i                 enable TCP/IP connections',
               '-k DIRECTORY       Unix-domain socket location',
               '-l                 enable SSL connections',
               '-N MAX-CONNECT     maximum number of allowed connections',
               '-M SERVERMODE      the database start as the '
               'appointed server mode',
               '-o OPTIONS         pass "OPTIONS" to each server '
               'process (obsolete)',
               '-p PORT            port number to listen on',
               '-s                 show statistics after each query',
               '-S WORK-MEM        set amount of memory for sorts (in kB)',
               '-u NUM             set the num of kernel '
               'version before upgrade',
               '-V, --version      output version information, then exit',
               '--NAME=VALUE       set run-time parameter',
               '--describe-config  describe configuration '
               'parameters, then exit',
               '--securitymode     allow database system run '
               'in security mode',
               '--single_node      A SingleDN mode is being activated',
               '-?, --help         show this help, then exit',
               'primary        database system starts as a primary server, '
               'send xlog to standby server',
               'standby        database system starts as a standby server, '
               'receive xlog from primary server',
               'pending        database system starts as a pending server, '
               'wait for promoting to primary or demoting to standby',
               '-f s|i|n|m|h       forbid use of some plan types',
               '-n                 do not reinitialize shared '
               'memory after abnormal exit',
               '-O                 allow system table structure changes',
               '-P                 disable system indexes',
               '-t pa|pl|ex        show timings after each query',
               '-T                 send SIGSTOP to all backend '
               'processes if one dies',
               '-W NUM             wait NUM seconds to allow '
               'attach from a debugger',
               '--localxid         use local transaction id '
               '(used only by gs_initdb)',
               '--single           selects single-user mode '
               '(must be first argument)',
               'DBNAME             database name (defaults to user name)',
               '-d 0-5             override debugging level',
               '-E                 echo statement before execution',
               '-j                 do not use newline as interactive '
               'query delimiter',
               '-r FILENAME        send stdout and stderr to given file',
               'Options for bootstrapping mode:',
               '--boot             selects bootstrapping mode '
               '(must be first argument)',
               '-r FILENAME        send stdout and stderr to given file',
               '-x NUM             internal use',
               'Node options:',
               '--single_node      start a single node database.'
               ' This is default setting.']
        for i in flg:
            self.assertIn(i, result,  '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        self.log.info("-Opengauss_Function_Tools_Gaussdb_Case0053 end-")

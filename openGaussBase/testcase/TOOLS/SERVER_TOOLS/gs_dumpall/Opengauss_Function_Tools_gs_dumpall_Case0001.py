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
Case Type   : 服务端工具
Case Name   : gs_dumpall工具显示帮助信息(正常)
Description :
    1.显示帮助信息(-？)
    2.显示帮助信息(--help)
Expect      :
    1.显示正确
    2.显示正确
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_Tools_gs_dumpall_Case0001start-------------------')
        self.dbuserNode = Node('dbuser')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------显示帮助信息------------------')
        cmd_list = ['-?', '--help']
        for cmd in cmd_list:
            check_cmd1 = f'''source {macro.DB_ENV_PATH}
                        gs_dumpall {cmd}'''
            logger.info(check_cmd1)
            msg1 = self.dbuserNode.sh(check_cmd1).result()
            logger.info(msg1)
            logger.info('--------------校验语法------------------')
            self.assertIn('gs_dumpall [OPTION]...', msg1)
            logger.info('--------------校验参数存在与否------------------')
            start_index = msg1.find('General options:')
            options_list = []
            for i in msg1[start_index:].split('\n'):
                for j in i.split(' '):
                    if len(j) != 0:
                        if j[0] == '-':
                            options_list.append(j)
                        else:
                            pass
                    else:
                        pass
            logger.info(options_list)
            parameter =[
                '-f,', '--file=FILENAME', '-v,', '--verbose', '-V,', '--version', '--lock-wait-timeout=TIMEOUT', '-?,',
                '--help', '-a,', '--data-only', '-c,', '--clean', '-g,', '--globals-only', '-o,', '--oids', '-O,',
                '--no-owner', '-r,', '--roles-only', '-s,', '--schema-only', '-S,', '--sysadmin=NAME', '-t,',
                '--tablespaces-only', '-x,', '--no-privileges', '--column-inserts/--attribute-inserts',
                '--disable-dollar-quoting', '--disable-triggers', '--inserts', '--no-security-labels',
                '--no-tablespaces', '--no-unlogged-table-data', '--include-alter-table', '--quote-all-identifiers',
                '--dont-overwrite-file', '--use-set-session-authorization', '--with-encryption=AES128', '--with-key=KEY',
                '--include-templatedb', '--binary-upgrade', '--binary-upgrade-usermap="USER1=USER2"', '--non-lock-table',
                '--tablespaces-postfix', '--parallel-jobs', '-h,', '--host=HOSTNAME', '-l,', '--database=DBNAME', '-p,',
                '--port=PORT', '-U,', '--username=NAME', '-w,', '--no-password', '-W,', '--password=PASSWORD',
                '--role=ROLENAME', '--rolepassword=ROLEPASSWORD']
            if len(options_list) == len(parameter):
                for opt in options_list:
                    if opt in parameter:
                        logger.info(f'{opt}---------参数校验通过---------')
                    else:
                        logger.error(f'{opt}---------参数校验不通过---------')
            else:
                logger.error('---------参数校验有误---------')
    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_dumpall_Case0001finish------------------')
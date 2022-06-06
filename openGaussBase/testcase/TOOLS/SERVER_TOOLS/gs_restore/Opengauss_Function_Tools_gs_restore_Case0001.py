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
Case Name   : gs_restore工具显示帮助信息(正常)
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
        logger.info('--------------Opengauss_Function_Tools_gs_restore_Case0001start-------------------')
        self.dbuserNode = Node('dbuser')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------显示帮助信息------------------')
        cmd_list = ['-?', '--help']
        for cmd in cmd_list:
            check_cmd1 = f'''source {macro.DB_ENV_PATH}
                        gs_restore {cmd}'''
            logger.info(check_cmd1)
            msg1 = self.dbuserNode.sh(check_cmd1).result()
            logger.info(msg1)
            logger.info('--------------校验语法------------------')
            self.assertIn('gs_restore [OPTION]... FILE', msg1)
            logger.info('-------------截取General options:后面的参数-------------------')
            start_index1 = msg1.find('General options:')
            logger.info('--------------定义一个空的列表，将获取的参数写入这个列表，并打印出该列表-------------------')
            options_list1 = []
            for i in msg1[start_index1:].split('\n'):
                for j in i.split(' '):
                    if len(j) != 0:
                        if j[0] == '-':
                            options_list1.append(j)
                        else:
                            pass
                    else:
                        pass
            logger.info(options_list1)
            logger.info('--------------判断参数存在与否-------------------')
            parameter = ['-d,', '--dbname=NAME', '-f,', '--file=FILENAME', '-F,', '--format=c|d|t', '-l,', '--list',
                         '-v,', '--verbose', '-V,', '--version', '-?,', '--help', '-a,', '--data-only', '-c,', '--clean',
                         '-C,', '--create', '-e,', '--exit-on-error', '-I,', '--index=NAME', '-j,', '--jobs=NUM', '-L,',
                         '--use-list=FILENAME', '-n,', '--schema=NAME', '-O,', '--no-owner', '-P,', '--function=NAME(args)',
                         '-s,', '--schema-only', '-S,', '--sysadmin=NAME', '-t,', '--table=NAME', '-T,', '--trigger=NAME',
                         '-x,', '--no-privileges/--no-acl', '-1,', '--single-transaction', '--disable-triggers',
                         '--no-data-for-failed-tables', '--no-security-labels', '--no-tablespaces', '--section=SECTION',
                         '--use-set-session-authorization', '--with-key=KEY', '-h,', '--host=HOSTNAME', '-p,',
                         '--port=PORT', '-U,', '--username=NAME', '-w,', '--no-password', '-W,', '--password=PASSWORD',
                         '--role=ROLENAME', '--rolepassword=ROLEPASSWORD']
            if len(options_list1) == len(parameter):
                for opt in options_list1:
                    if opt in parameter:
                        logger.info(f'{opt}---------参数校验通过---------')
                    else:
                        logger.error(f'{opt}---------参数校验不通过---------')
            else:
                logger.error('---------参数校验有误---------')

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_restore_Case0001finish------------------')
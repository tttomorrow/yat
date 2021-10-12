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
Case Type   : 服务端工具
Case Name   : gs_collector工具显示帮助信息(正常)
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
        logger.info('--------------Opengauss_Function_Tools_gs_collector_Case0001start-------------------')
        self.dbuserNode = Node('dbuser')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------显示帮助信息------------------')
        cmd_list = ['-?', '--help']
        for cmd in cmd_list:
            check_cmd1 = f'''source {macro.DB_ENV_PATH}
                        gs_collector {cmd}'''
            logger.info(check_cmd1)
            msg1 = self.dbuserNode.sh(check_cmd1).result()
            logger.info(msg1)

            start_index1 = msg1.find('Usage:')+len('Usage:')
            start_index2 = msg1.find('General options:')
            temp = msg1[start_index1:start_index2].split('\n')
            logger.info(temp)
            options_list1 = []
            for j in temp[1:-2]:
                options_list1.append(j.strip())
            logger.info(options_list1)
            grammar = ['gs_collector -? | --help',
                       'gs_collector -V | --version',
                       'gs_collector --begin-time="BEGINTIME" --end-time="ENDTIME" [-h HOSTNAME | -f HOSTFILE]',
                       '[--keyword=KEYWORD] [--speed-limit=SPEED] [-o OUTPUT] [-l LOGFILE]']
            if len(options_list1) == len(grammar):
                for opt in options_list1:
                    if opt in grammar:
                        logger.info(f'{opt}---------语法校验通过---------')
                    else:
                        logger.error(f'{opt}---------语法校验不通过---------')
            else:
                logger.error('---------语法校验有误---------')

            options_list2 = []
            for i in msg1[start_index2:].split('\n'):
                for j in i.split(' '):
                    if len(j) != 0:
                        if j[0] == '-':
                            options_list2.append(j)
                        else:
                            pass
                    else:
                        pass
            logger.info(options_list2)
            parameter =  ['--begin-time=BEGINTIME', '--end-time=ENDTIME', '--speed-limit=SPEED', '-h', '-f',
                          '--keyword=KEYWORD', '-o', '-l', '-?,', '--help', '-V,', '--version', '-C']
            if len(options_list2) == len(parameter):
                for opt in options_list2:
                    if opt in parameter:
                        logger.info(f'{opt}---------参数校验通过---------')
                    else:
                        logger.error(f'{opt}---------参数校验不通过---------')
            else:
                logger.error('---------参数校验有误---------')


    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_collector_Case0001finish------------------')

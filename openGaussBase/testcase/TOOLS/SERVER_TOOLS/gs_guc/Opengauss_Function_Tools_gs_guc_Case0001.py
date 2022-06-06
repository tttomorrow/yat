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
Case Name   : gs_guc工具显示帮助信息(正常)
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
        logger.info('--------------Opengauss_Function_Tools_gs_guc_Case0001start-------------------')
        self.dbuserNode = Node('dbuser')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------显示帮助信息------------------')
        cmd_list = ['-?', '--help']
        for cmd in cmd_list:
            check_cmd1 = f'''source {macro.DB_ENV_PATH}
                        gs_guc {cmd}'''
            logger.info(check_cmd1)
            msg1 = self.dbuserNode.sh(check_cmd1).result()
            logger.info(msg1)

            logger.info('--------------从Checking GUC parameters:开始截取msg1-------------------')
            logger.info('-------------截取Checking GUC parameters:到Common options:部分的语法-------------------')
            start_index1 = msg1.find('Checking GUC parameters:') + len('Checking GUC parameters:')
            start_index2 = msg1.find('Common options:')
            temp = msg1[start_index1:start_index2].split('\n')
            options_list1 = []
            for j in temp:
                if j.lstrip().startswith('gs_guc'):
                    options_list1.append(j.strip())
                else:
                    pass
            else:
                pass
            logger.info(options_list1)
            grammar = ['gs_guc check [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} {-c "parameter", -c "parameter", ...}',
                       'gs_guc check [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} {-c parameter, -c parameter, ...}',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} {-c "parameter = value" -c "parameter = value" ...}',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} {-c " parameter = value " -c " parameter = value " ...}',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} {-c "parameter = \'value\'" -c "parameter = \'value\'" ...}',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} {-c " parameter = \'value\' " -c " parameter = \'value\' " ...}',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} {-c "parameter" -c "parameter" ...}',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} -h "HOSTTYPE DATABASE USERNAME IPADDR IPMASK AUTHMEHOD authentication-options"',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} -h "HOSTTYPE DATABASE USERNAME IPADDR-WITH-IPMASK AUTHMEHOD authentication-options"',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} -h "HOSTTYPE DATABASE USERNAME HOSTNAME AUTHMEHOD authentication-options"',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} -h "HOSTTYPE DATABASE USERNAME IPADDR IPMASK"',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} -h "HOSTTYPE DATABASE USERNAME IPADDR-WITH-IPMASK "',
                       'gs_guc {set | reload} [-N NODE-NAME] {-I INSTANCE-NAME | -D DATADIR} -h "HOSTTYPE DATABASE USERNAME HOSTNAME"',
                       'gs_guc encrypt [-M keymode] -K password [-U username] -D DATADIR',
                       'gs_guc generate [-o prefix] -S cipherkey -D DATADIR']
            if len(options_list1) == len(grammar):
                for opt in options_list1:
                    if opt in grammar:
                        logger.info(f'{opt}---------语法校验通过---------')
                    else:
                        logger.error(f'{opt}---------语法校验不通过---------')
            else:
                logger.error('---------语法校验有误---------')

            logger.info('--------------定义一个空的列表，将获取的参数写入这个列表，并打印出该列表-------------------')
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
            parameter = ['-N', '-I', '-D,', '--pgdata=DATADIR', '-c', '-c', '-h', '-?,', '--help', '-V,', '--version',
                         '-M,', '--keymode=MODE', '-K', '-U,', '--keyuser=USER', '-o', '-S']
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
        logger.info('------------------Opengauss_Function_Tools_gs_guc_Case0001finish------------------')
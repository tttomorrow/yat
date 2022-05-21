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
Case Name   : gs_checkos工具显示帮助信息(正常)
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
        logger.info('--------------Opengauss_Function_Tools_gs_checkos_Case0001start-------------------')
        self.rootNode = Node('default')
        self.Constant = Constant()

    def test_server_tools1(self):
        logger.info('------------------显示帮助信息------------------')
        logger.info('--------------执行命令获取帮助信息--------------')
        cmd_list = ['-?', '--help']
        for cmd in cmd_list:
            check_cmd1 = f'''source {macro.DB_ENV_PATH}
                        gs_checkos {cmd}'''
            logger.info(check_cmd1)
            msg1 = self.rootNode.sh(check_cmd1).result()
            logger.info(msg1)
            logger.info('--------------从Usage:开始截取msg1---------------')
            start_index1 = msg1.find('Usage:')+len('Usage:')
            start_index2 = msg1.find('General options:')
            start_index3 = msg1.find('Item number description:')+len('Item number description:')
            logger.info('--------------截取语法部分---------------')
            temp1 = msg1[start_index1:start_index2].split('\n')
            options_list1 = []
            for i in temp1[1:-2]:
                options_list1.append(i.strip())
            logger.info(options_list1)
            grammar = ['gs_checkos -? | --help',
                       'gs_checkos -V | --version',
                       'gs_checkos -i ITEM [-f HOSTFILE] [-h HOSTNAME] [-X XMLFILE] [--detail] [-o OUTPUT] [-l LOGFILE]']

            if len(options_list1) == len(grammar):
                for opt in options_list1:
                    if opt in grammar:
                        logger.info(f'{opt}---------语法校验通过---------')
                    else:
                        logger.error(f'{opt}---------语法校验不通过---------')
            else:
                logger.error('---------语法校验有误---------')

            logger.info('--------------截取中间参数部分---------------')
            options_list2 = []
            for i in msg1[start_index2:start_index3].split('\n'):
                for j in i.split(' '):
                    if len(j) != 0:
                        if j[0] == '-':
                            options_list2.append(j)
                        else:
                            pass
                    else:
                        pass
            logger.info(options_list2)
            parameter1 = ['-i', '-f', '-h', '-X', '--detail', '-o', '-l', '-?', '--help', '-V', '--version']
            if len(options_list2) == len(parameter1):
                for opt in options_list2:
                    if opt in parameter1:
                        logger.info(f'{opt}---------参数校验通过---------')
                    else:
                        logger.error(f'{opt}---------参数校验不通过---------')
            else:
                logger.error('---------参数校验有误---------')

            logger.info('--------------截取最后面参数部分---------------')
            temp2 = msg1[start_index3:].split('\n')
            logger.info(temp2)
            options_list3 = []
            for j in temp2[1:]:
                options_list3.append(j.strip())
            logger.info(options_list3)
            parameter2 =[
                "'A1':[ OS version status ]","'A2':[ Kernel version status ]","'A3':[ Unicode status ]",
                "'A4':[ Time zone status ]","'A5':[ Swap memory status ]","'A6':[ System control parameters status ]",
                "'A7':[ File system configuration status ]","'A8':[ Disk configuration status ]",
                "'A9':[ Pre-read block size status ]","'A10':[ IO scheduler status ]","'A11':[ Network card configuration status ]",
                "'A12':[ Time consistency status ]","'A13':[ Firewall service status ]","'A14':[ THP service status ]",
                "'B1':[ Set system control parameters ]","'B2':[ Set file system configuration value ]","'B3':[ Set pre-read block size value ]",
                "'B4':[ Set IO scheduler value ]","'B5':[ Set network card configuration value ]","'B6':[ Set THP service ]",
                "'B7':[Set RemoveIPC value]","'B8':[Set Session Process]"]
            if len(options_list3) == len(parameter2):
                for opt in options_list3:
                    if opt in parameter2:
                        logger.info(f'{opt}---------参数校验通过---------')
                    else:
                        logger.error(f'{opt}---------参数校验不通过---------')
            else:
                logger.error('---------参数校验有误---------')

    def tearDown(self):
        logger.info('--------------无需清理环境-------------------')
        logger.info('------------------Opengauss_Function_Tools_gs_checkos_Case0001finish------------------')
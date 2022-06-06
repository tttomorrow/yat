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
Case Name   : 指定--help参数显示gs_backup帮助信息是否成功
Description :
    1.执行命令显示关于gs_backup命令行参数的帮助文件
Expect      :
    1.信息打印成功
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0006开始执行---')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('------------------显示帮助信息------------------')
        cmd_list = ['--help']
        for cmd in cmd_list:
            check_cmd1 = f'''source {macro.DB_ENV_PATH};
                gs_backup {cmd};
                '''
            LOG.info(check_cmd1)
            msg1 = self.PrimaryNode.sh(check_cmd1).result()
            LOG.info(msg1)

            LOG.info('---截取Usage到General options部分的语法------')
            start_index1 = msg1.find('Usage:') + len('Usage:')
            start_index2 = msg1.find('General options:')
            temp = msg1[start_index1:start_index2].split('\n')
            options_list1 = []
            for j in temp[1:-2]:
                options_list1.append(j.strip())
            else:
                pass
            LOG.info(options_list1)
            grammar = [
                'gs_backup -? | --help',
                'gs_backup -V | --version',
                'gs_backup -t backup --backup-dir=BACKUPDIR [-h HOSTNAME] \
                [--parameter]',
                'gs_backup -t restore --backup-dir=BACKUPDIR [-h HOSTNAME] \
                [--parameter]',
                '[--binary] [--all] [-l LOGFILE]',
                '[--force]']
            if len(options_list1) == len(grammar):
                for opt in options_list1:
                    if opt in grammar:
                        LOG.info(f'{opt}----语法校验通过----')
                    else:
                        LOG.error(f'{opt}----语法校验不通过----')
            else:
                LOG.error('---------语法校验有误---------')

            LOG.info('--定义一个空的列表，将获取的参数写入这个列表--')
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
            LOG.info(options_list2)
            parameter = ['-t', '--backup-dir=BACKUPDIR', '-h',
                         '--parameter', '--binary', '--all',
                         '--force', '-l', '-?, --help',
                         '-V, --version']
            if len(options_list2) == len(parameter):
                for opt in options_list2:
                    if opt in parameter:
                        LOG.info(f'{opt}-------参数校验通过--------')
                    else:
                        LOG.error(f'{opt}------参数校验不通过------')
            else:
                LOG.error('---------参数校验有误---------')

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        # 无须清理环境
        LOG.info('---Opengauss_Function_Tools_gs_backup_Case0006执行完成---')

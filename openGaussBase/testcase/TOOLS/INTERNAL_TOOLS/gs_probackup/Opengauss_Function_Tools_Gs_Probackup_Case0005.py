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
Case Name   : 查看gs_probackup init命令的摘要信息
Description :
    1.查看gs_probackup init命令的摘要信息
Expect      :
    1.查看gs_probackup init命令的摘要信息成功
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
        LOG.info('---Opengauss_Function_Tools_Gs_Probackup_Case0004开始执行---')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.except_msg = ['gs_probackup init -B backup-path', '',
                           '-B, --backup-path=backup-path    '
                           'location of the backup '
                           'storage area']

    def test_system_internal_tools(self):
        LOG.info('------------------显示帮助信息------------------')
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_probackup init --help;
            '''
        LOG.info(check_cmd1)
        msg1 = self.PrimaryNode.sh(check_cmd1).result()
        LOG.info(msg1)
        temp = msg1.splitlines()
        options_list1 = []
        for j in temp:
            options_list1.append(j.strip())
        LOG.info(options_list1)
        self.assertEqual(options_list1, self.except_msg)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        # 无须清理环境
        LOG.info('---Opengauss_Function_Tools_Gs_Probackup_Case0005执行完成---')

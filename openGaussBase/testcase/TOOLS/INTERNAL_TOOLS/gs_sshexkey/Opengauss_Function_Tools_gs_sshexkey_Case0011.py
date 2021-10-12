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
Case Type   : 系统内部使用工具 gs_sshexkey
Case Name   : root用户下，执行gs_sshexkey --help 命令
Description :
    1、root用户下，执行gs_sshexkey --help
    2、检查选项和用法
Expect      :
    1、命令执行成功
    2、用法和参数选项齐全且描述正确
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class ToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.commonsh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryRoot')
        logger.info("======SetUp：检查数据库状态是否正常======")
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_gs_sshexkey(self):
        logger.info("===Opengauss_Function_Tools_gs_sshexkey_Case0011开始执行===")

        num_list = []
        result = ['-f', '-h', '-l', '--skip-hostname-set',
                  '-?', '--help', '-V', '--version']

        logger.info("======root用户下执行gs_sshexkey --help命令======")
        gs_cmd = f'''source {macro.DB_ENV_PATH}
            gs_sshexkey --help
            '''
        logger.info(gs_cmd)
        gs_res = self.user_node.sh(gs_cmd).result()
        logger.info(gs_res)

        logger.info("======提取结果，检查选项和用法======")
        for i in gs_res.split('\n')[9:]:
            for j in i.split():
                if j.strip().startswith('-'):
                    num_list.append(j.strip().strip(','))
        self.assertEqual(num_list, result)

    def tearDown(self):
        logger.info("======No Need Clean && No Need Recovery======")
        logger.info("===Opengauss_Function_Tools_gs_sshexkey_Case0011执行结束===")

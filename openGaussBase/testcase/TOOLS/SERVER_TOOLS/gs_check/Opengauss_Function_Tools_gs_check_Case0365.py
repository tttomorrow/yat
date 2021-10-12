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
Case Name   : 检查结果输出指定文件夹路径，以binary_upgrade场景为例
Description :
     1.检查结果输出指定文件夹路径，以binary_upgrade场景为例
Expect      :
     1.检查完成并在指定路径下产生日志文件
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info('---Opengauss_Function_Tools_gs_check_Case0365start---')
        self.dbusernode = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        self.log.info('---------步骤1：binary_upgrade场景检查结果输出到指定文件夹路径---------')
        self.log.info('----------步骤1.1：创建指定文件夹路径---------')
        mkdir_cmd = f'mkdir {macro.DB_INSTANCE_PATH}/checkresult;'
        self.log.info(mkdir_cmd)
        mkdir_msg = self.dbusernode.sh(mkdir_cmd).result()
        self.log.info(mkdir_msg)
        self.log.info('-----------步骤1.2：检查结果输出到指定文件夹路径---------')
        check_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_check ' \
            f'-e binary_upgrade ' \
            f'-o {macro.DB_INSTANCE_PATH}/checkresult;'
        self.log.info(check_cmd1)
        msg1 = self.dbusernode.sh(check_cmd1).result()
        self.log.info(msg1)
        flag = (self.constant.GS_CHECK_SUCCESS_MSG2[0] in msg1 or
                self.constant.GS_CHECK_SUCCESS_MSG2[1] in msg1) and \
                self.constant.GS_CHECK_SUCCESS_MSG2[2] in msg1
        self.assertTrue(flag)
        self.log.info('---------------判断是否产生结果报告---------------')
        cat_cmd = f'cd  {macro.DB_INSTANCE_PATH}/checkresult;' \
            f'tar -xvf CheckReport_binary_upgrade*.tar.gz; ' \
            f'cat CheckResult*;'
        cat_msg = self.dbusernode.sh(cat_cmd).result()
        self.log.info(cat_msg)
        self.assertIn('All check items run completed', cat_msg)

    def tearDown(self):
        self.log.info('-------无需清理环境------')
        self.log.info('------清理生成结果报告-------')
        clear_cmd1 = f'rm -rf {macro.DB_INSTANCE_PATH}/checkresult;'
        self.log.info(clear_cmd1)
        clear_msg1 = self.dbusernode.sh(clear_cmd1).result()
        self.log.info(clear_msg1)
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0365finish--')

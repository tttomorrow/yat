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
Case Name   :
    参数-e 执行binary_upgrade（就地升级前巡检），参数--skip-root-items参数
    跳过root权限检查项，-l 指定生成log文件路径,-o 指定检查结果输出文件夹路径
Description :
    1.参数-e 执行binary_upgrade（就地升级前巡检），参数--skip-root-items参数
    跳过root权限检查项，-l 指定生成log文件路径,-o 指定检查结果输出文件夹路径
    2.步骤2.查看log日志是否生成
    3.清理环境
Expect      :
    1.巡检成功
    2.log日志生成成功
    3.清理环境成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0383start--')
        self.dbuser_node = Node('dbuser')
        self.primary_root = Node('PrimaryRoot')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.log.info('---步骤1.参数-e 执行binary_upgrade（就地升级前巡检），'
                      '使用--skip-root-items参数跳过root权限检查项，'
                      '-l 指定生成log文件路径，'
                      '-o 指定检查结果输出文件夹路径---')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_check -e binary_upgrade --skip-root-items ' \
            f'-l {macro.DB_INSTANCE_PATH}/test_check/check.log ' \
            f'-o {macro.DB_INSTANCE_PATH}/test_check/'
        self.log.info(check_cmd)
        check_msg = self.dbuser_node.sh(check_cmd).result()
        self.log.info(check_msg)
        self.assertTrue(self.constant.GS_CHECK_SUCCESS_MSG2[0]
            in check_msg or self.constant.GS_CHECK_SUCCESS_MSG2[1]
            in check_msg and self.constant.GS_CHECK_SUCCESS_MSG2[2])

        self.log.info('-------步骤2.查看log日志是否生成-------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'cat {macro.DB_INSTANCE_PATH}/test_check/check*;'
        self.log.info(check_cmd)
        check_msg = self.dbuser_node.sh(check_cmd).result()
        self.log.info(check_msg)
        self.assertIn('Analysis the check result successfully', check_msg)

    def tearDown(self):
        self.log.info("------------步骤3.清理环境---------------")
        rm_cmd = f'rm -rf {macro.DB_INSTANCE_PATH}/test_check/'
        self.log.info(rm_cmd)
        rm_msg = self.primary_root.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('--Opengauss_Function_Tools_gs_check_Case0383finish--')
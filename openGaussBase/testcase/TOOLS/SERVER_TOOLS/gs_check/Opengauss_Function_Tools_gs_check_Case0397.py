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
Case Name   : omm用户进行longtime场景巡检场景检查（longtime）
Description :
     omm用户进行longtime巡检场景检查：gs_check -e longtime
Expect      :
     检查完成
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('----Opengauss_Function_Tools_gs_check_Case0397start----')
        self.dbuserNode = Node('dbuser')
        self.rootNode = Node('default')
        self.Constant = Constant()
        self.result_msg = f'Start to health check for the cluster. ' \
            f'Total Items:5'

    def test_server_tools1(self):
        LOG.info('----------------longtime巡检场景检查---------------')
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_check -e  longtime;
            '''
        LOG.info(check_cmd1)
        msg1 = self.dbuserNode.sh(check_cmd1).result()
        LOG.info(msg1)
        flag = (self.Constant.GS_CHECK_SUCCESS_MSG2[0] in msg1 or \
                self.Constant.GS_CHECK_SUCCESS_MSG2[1] in msg1) and \
               self.Constant.GS_CHECK_SUCCESS_MSG2[2] in msg1
        self.assertTrue(flag)
        self.assertIn(self.result_msg, msg1)

    def tearDown(self):
        LOG.info('--------------需清理环境-------------------')
        clear_cmd = f'rm -rf /tmp/check*;' \
            f'rm -rf {macro.DB_INSTANCE_PATH}/../tool/script/gspylib' \
            f'/inspection/output/CheckReport*;'
        LOG.info(clear_cmd)
        clear_msg = self.rootNode.sh(clear_cmd).result()
        LOG.info(clear_msg)
        LOG.info('-----------------产生的文件清理完成------------------')
        LOG.info('---Opengauss_Function_Tools_gs_check_Case0397finish---')

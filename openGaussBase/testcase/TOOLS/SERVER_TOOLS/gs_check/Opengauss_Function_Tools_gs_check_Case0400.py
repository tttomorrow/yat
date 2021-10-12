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
Case Name   : root用户install安装场景检查
Description : root用户install安装场景检查：gs_check -e install
Expect      : 检查失败
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
        LOG.info('---Opengauss_Function_Tools_gs_check_Case0400start---')
        self.defaultNode = Node('default')
        self.rootNode = Node('dbuser')
        self.Constant = Constant()

    def test_server_tools1(self):
        LOG.info('---------root用户install安装场景检查----------')
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
            gs_check -e  install;
            '''
        LOG.info(check_cmd1)
        msg1 = self.defaultNode.sh(check_cmd1).result()
        LOG.info(msg1)
        self.assertIn(self.Constant.GS_CHECK_ERROR_MSG1, msg1)

    def tearDown(self):
        LOG.info('------清理环境-------')
        clear_cmd1 = f'rm -rf /tmp/check*;' \
            f'rm -rf {macro.DB_INSTANCE_PATH}/../tool/script/gspylib' \
            f'/inspection/output/CheckReport*;'
        LOG.info(clear_cmd1)
        clear_msg1 = self.rootNode.sh(clear_cmd1).result()
        LOG.info(clear_msg1)
        LOG.info('---Opengauss_Function_Tools_gs_check_Case0400finish---')

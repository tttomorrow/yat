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
Case Type   : 系统内部使用工具
Case Name   : 使用gaussdb工具gaussdb的版本信息然后退出
Description :
    1.使用gaussdb工具打印版本信息
Expect      :
    1.使用gaussdb工具打印版本信息成功
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        LOG.info('----------------this is setup-----------------------')
        LOG.info(
            '---Opengauss_Function_Tools_Gaussdb_Case0048开始执行-----')
        self.constant = Constant()
        self.user_node = Node('dbuser')
        self.env_path = macro.DB_ENV_PATH
        self.user_node = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info(
            '---------------------查看版本信息-------------------------')
        excute_cmd = f'''
                    source {self.env_path};
                    gaussdb -V;
                    '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.opengauss, msg)

    def tearDown(self):
        LOG.info('----------------this is tearDown-----------------------')
        # 无需清理环境
        LOG.info(
            '-----Opengauss_Function_Tools_Gaussdb_Case0048执行完成---')

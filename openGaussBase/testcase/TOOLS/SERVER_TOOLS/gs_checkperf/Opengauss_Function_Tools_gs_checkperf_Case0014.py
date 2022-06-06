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
Case Name   : root用户检查SSD性能(-U用户不存在)
Description :
    1.root用户检查SSD性能(-U用户不存在)
Expect      :
    1.执行报错,用户不存在
History     : 
"""
import unittest

from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-----Opengauss_Function_Tools_gs_checkperf_Case0014_开始-----')
        self.root_node = Node('default')
        self.u_checkperf = 'u_checkperf_0014'
        self.assert_msg = f'User {self.u_checkperf} does not exist'

    def test_tools_checkperf(self):
        text = '----step1:root用户检查SSD性能(-U用户不存在);expect:执行报错,用户不存在----'
        self.log.info(text)
        checkperf_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkperf ' \
            f'-U {self.u_checkperf} ' \
            f'-i SSD;'
        self.log.info(checkperf_cmd)
        checkperf_msg = self.root_node.sh(checkperf_cmd).result()
        self.log.info(checkperf_msg)
        self.assertIn(self.assert_msg, checkperf_msg, '执行失败:' + text)

    def tearDown(self):
        self.log.info('-----------无需清理环境----------')
        self.log.info(
            '-----Opengauss_Function_Tools_gs_checkperf_Case0014_结束-----')

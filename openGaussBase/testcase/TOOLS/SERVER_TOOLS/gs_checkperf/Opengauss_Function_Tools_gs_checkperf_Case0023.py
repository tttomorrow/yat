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
Case Name   : opengauss安装用户检查数据库性能并显示检查结果的详情
Description :
    1.opengauss安装用户检查数据库性能并显示检查结果的详情
Expect      :
    1.正常显示检查结果
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
            '-----Opengauss_Function_Tools_gs_checkperf_Case0023_开始-----')
        self.dbuser_node = Node('dbuser')

    def test_tools_checkperf(self):
        text = '----step1:opengauss安装用户检查数据库性能并显示检查结果的详情;expect:正常显示检查结果----'
        self.log.info(text)
        checkperf_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkperf ' \
            f'-U {self.dbuser_node.ssh_user} ' \
            f'-i PMK ' \
            f'--detail;'
        self.log.info(checkperf_cmd)
        checkperf_msg = self.dbuser_node.sh(checkperf_cmd).result()
        self.log.info(checkperf_msg)
        self.assertIn('Cluster statistics information', checkperf_msg,
                      '执行失败' + text)
        self.assertIn('Node statistics information', checkperf_msg,
                      '执行失败' + text)
        self.assertIn('Session statistics information', checkperf_msg,
                      '执行失败' + text)

    def tearDown(self):
        self.log.info('-----------无需清理环境----------')
        self.log.info(
            '-----Opengauss_Function_Tools_gs_checkperf_Case0023_结束-----')

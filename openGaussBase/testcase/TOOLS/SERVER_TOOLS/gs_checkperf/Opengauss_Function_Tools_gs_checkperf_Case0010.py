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
Case Name   : opengauss安装用户检查openGauss性能(不使用-U参数)
Description :
    1.opengauss安装用户检查openGauss性能(不使用-U参数)
    gs_checkperf  -i  PMK
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
            '-----Opengauss_Function_Tools_gs_checkperf_Case0010_开始-----')
        self.dbuser_node = Node('dbuser')

    def test_tools_checkperf(self):
        text = '----step1:opengauss安装安装用户检查openGauss性能;expect:正常显示检查结果----'
        self.log.info(text)
        checkperf_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkperf ' \
            f'-i PMK;'
        self.log.info(checkperf_cmd)
        checkperf_result = self.dbuser_node.sh(checkperf_cmd).result()
        self.log.info(checkperf_result)
        result_list1 = checkperf_result.splitlines()
        result_list = []
        for i in result_list1:
            if ':' in i:
                result_list.append(i.split(':')[0].strip())
        self.log.info(result_list)
        checkperf_result = ['Cluster statistics information',
                            'Host CPU busy time ratio',
                            'MPPDB CPU time % in busy time',
                            'Shared Buffer Hit ratio',
                            'In-memory sort ratio',
                            'Physical Reads',
                            'Physical Writes',
                            'DB size',
                            'Total Physical writes',
                            'Active SQL count',
                            'Session count']
        self.assertEqual(checkperf_result.sort(), result_list.sort(),
                         '执行失败:' + text)

    def tearDown(self):
        self.log.info('-----------无需清理环境----------')
        self.log.info(
            '-----Opengauss_Function_Tools_gs_checkperf_Case0010_结束-----')

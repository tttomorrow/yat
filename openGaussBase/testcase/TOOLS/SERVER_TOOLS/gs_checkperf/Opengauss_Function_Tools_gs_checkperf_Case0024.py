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
Case Name   : opengauss安装用户检查数据库性能并指定检查报告输出到指定的文件
Description :
    1.创建检查报告输出路径
    2.opengauss安装用户检查openGauss性能并指定检查报告输出到指定的文件
    gs_checkperf  -U 运行openGauss的用户名称 -i PMK -o 检查报告输出到指定的文件
    3.清理环境
Expect      :
    1.创建成功
    2.检查报告存储到指定的文件中
    3.清理环境成功
History     : 
"""
import os
import unittest

from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Toofind(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-----Opengauss_Function_Tools_gs_checkperf_Case0024_开始-----')
        self.dbuser_node = Node('dbuser')
        self.report_path = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'checkperf')
        self.report = os.path.join(self.report_path, 'report.txt')

    def test_tools_checkperf(self):
        text = '----step1:创建检查报告存储路径;expect:创建成功----'
        self.log.info(text)
        is_dir_exists_cmd = f'''if [ ! -d "{self.report_path}" ]
                                then
                                    mkdir -p {self.report_path}
                                fi'''
        result = self.dbuser_node.sh(is_dir_exists_cmd).result()
        self.log.info(result)
        self.assertEqual(result, '')

        text = '----step2:opengauss安装用户检查数据库性能并指定检查报告输出到指定的文件;' \
               'expect:检查报告存储到指定的文件中----'
        self.log.info(text)
        checkperf_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_checkperf ' \
            f'-U {self.dbuser_node.ssh_user} ' \
            f'-i PMK ' \
            f'-o {self.report};'
        self.log.info(checkperf_cmd)
        msg = self.dbuser_node.sh(checkperf_cmd).result()
        self.log.info(msg)
        cat_cmd = f'cat {self.report} ;'
        self.log.info(cat_cmd)
        cat_msg = self.dbuser_node.sh(cat_cmd).result()
        self.log.info(cat_msg)
        self.assertIn('Cluster statistics information', cat_msg,
                      '执行失败' + text)

    def tearDown(self):
        text = '----step3:清理环境;expect:清理环境成功----'
        self.log.info(text)
        rm_cmd = f'rm -rf {self.report_path};'
        self.log.info(rm_cmd)
        result = self.dbuser_node.sh(rm_cmd).result()
        self.log.info(result)
        self.assertEqual('', result, '执行失败:' + text)
        self.log.info(
            '-----Opengauss_Function_Tools_gs_checkperf_Case0024_结束-----')

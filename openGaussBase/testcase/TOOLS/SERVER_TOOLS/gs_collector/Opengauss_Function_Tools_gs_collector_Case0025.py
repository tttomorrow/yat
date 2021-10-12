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
Case Name   : 收集ClusterManager信息
Description :
        1.创建收集内容的配置文件,文件内容是json 格式
        2.收集log类型信息下的ClusterManager信息
        3.清理环境
Expect      :
        1.写入完成
        2.收集成功
        3.清理完成
History     :
"""

import os
import time
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.dbuser_node = Node('PrimaryDbUser')
        self.constant = Constant()
        self.config_path = os.path.join(macro.DB_INSTANCE_PATH,
                                        'collector_config')
        self.result_path = os.path.join(macro.DB_INSTANCE_PATH,
                                        'collector_result')

    def test_server_tools(self):
        self.log.info(
            '-----Opengauss_Function_Tools_gs_collector_Case0025start-----')
        text = '---step1:创建收集内容的配置文件，文件内容是json 格式;expect:写入成功---'
        self.log.info(text)
        config_content = r'''{{"Collect":[{{"TypeName": "Log", "Content":
                    "ClusterManager", "Interval":"0", "Count":"1"}}]}}'''
        shell_cmd = f'''echo '{config_content}' > {self.config_path}'''
        self.log.info(shell_cmd)
        shell_msg = self.dbuser_node.sh(shell_cmd).result()
        self.log.info(shell_msg)
        du_cmd = f'''du -h {self.config_path};'''
        self.log.info(du_cmd)
        du_msg = self.dbuser_node.sh(du_cmd).result()
        self.log.info(du_msg)
        dumsg_list = du_msg.split()[0]
        self.log.info(dumsg_list)
        self.assertTrue(float(dumsg_list[:-1]) > 0)

        text = '---step2:收集log类型信息下的ClusterManager信息;expect:收集成功---'
        self.log.info(text)
        self.log.info('获取信息手机的开始和结束时间')
        start_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        self.log.info(start_time)
        time.sleep(60)
        end_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        self.log.info(end_time)
        collector_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_collector ' \
            f'--begin-time="{start_time}" ' \
            f'--end-time="{end_time}" ' \
            f'-C {self.config_path} ' \
            f'-o {self.result_path};'
        self.log.info(collector_cmd)
        collector_msg = self.dbuser_node.sh(collector_cmd).result()
        self.log.info(collector_msg)
        tar_cmd = f'source {macro.DB_ENV_PATH};' \
            f'cd {self.result_path};' \
            f'tar -zxvf collector*.tar.gz;'
        self.log.info(tar_cmd)
        tar_msg = self.dbuser_node.sh(tar_cmd).result()
        self.log.info(tar_msg)
        self.assertIn('Summary.log', tar_msg)
        self.assertIn('Detail.log', tar_msg)

    def tearDown(self):
        text = '--------------step3:清理环境;expect:清理环境完成-------------'
        self.log.info(text)
        self.log.info('------------删除配置文件和收集结果-------------')
        rm_cmd = f'rm -rf {self.config_path};' \
            f'rm -rf {self.result_path}; '
        self.log.info(rm_cmd)
        rm_msg = self.dbuser_node.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info(
            '-----Opengauss_Function_Tools_gs_collector_Case0025finish-----')
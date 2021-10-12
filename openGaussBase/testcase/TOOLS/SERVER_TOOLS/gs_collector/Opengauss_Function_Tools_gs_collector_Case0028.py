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
Case Name   : 通过时间筛选收集xlog
Description :
        1.创建收集内容的配置文件，文件内容是json 格式
        2.通过时间筛选收集xlog
        3.删除创建收集内容的配置文件
Expect      :
        1.写入完成
        2.收集成功
        3.删除成功
History     :
"""


import os
import time
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')

class Tools(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-----Opengauss_Function_Tools_gs_collector_Case0028start-----')
        self.dbusernode = Node('PrimaryDbUser')
        self.constant = Constant()
        self.path = os.path.join(macro.DB_INSTANCE_PATH, 'collector_config')
        self.result_path = os.path.join(macro.DB_INSTANCE_PATH,
                                        'collector_result')

    def test_server_tools1(self):
        self.log.info('-----------步骤1：创建收集内容的配置文件，文件内容是json 格式---------')
        test_str = r'''{{"Collect":[{{"TypeName": "XLog", "Content":
            "DataNode","Interval":"3", "Count":"2"}}]}}'''
        shell_cmd = f'''echo '{test_str}' > {self.path}'''
        self.log.info(shell_cmd)
        shell_msg = self.dbusernode.sh(shell_cmd).result()
        self.log.info(shell_msg)
        self.log.info('-----------获取收集日志的时间---------')
        current_date = time.strftime("%Y%m%d", time.localtime())
        self.log.info(current_date)
        current_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        self.log.info(current_time)
        self.log.info('-----步骤2：通过时间筛选收集xlog-----')
        collector_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_collector --begin-time="{current_date} 00:00" ' \
            f'--end-time="{current_time}" ' \
            f'-C {self.path} -o {self.result_path};'
        self.log.info(collector_cmd)
        collector_msg = self.dbusernode.sh(collector_cmd).result()
        self.log.info(collector_msg)
        tar_cmd = f'source {macro.DB_ENV_PATH};' \
            f'cd {self.result_path};' \
            f'tar -zxvf collector*.tar.gz;'
        self.log.info(tar_cmd)
        tar_msg = self.dbusernode.sh(tar_cmd).result()
        self.log.info(tar_msg)
        self.assertIn('Summary.log', tar_msg)
        self.assertIn('Detail.log', tar_msg)

    def tearDown(self):
        self.log.info('--------------清理环境-------------------')
        self.log.info('------------步骤3：配置文件和结果文件-------------')
        rm_cmd = f'rm -rf {macro.DB_INSTANCE_PATH}/collector_config;' \
            f'rm -rf {macro.DB_INSTANCE_PATH}/collector_result; '
        self.log.info(rm_cmd)
        rm_msg = self.dbusernode.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info(
            '-----Opengauss_Function_Tools_gs_collector_Case0028finish-----')
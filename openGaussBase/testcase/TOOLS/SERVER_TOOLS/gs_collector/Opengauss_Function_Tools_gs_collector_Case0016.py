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
Case Name   : 收集日志信息时指定主机名称列表文件（hostfile中是主机IP）
Description :
        1.将主机IP写入主机名称列表文件
        2.收集日志信息时指定主机名称列表文件（hostfile中是主机IP）
        3.删除主机名称列表文件
Expect      :
        1.写入完成
        2.收集失败
        3.删除成功
History     :
"""

import time
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger



class Tools(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info(
            '------Opengauss_Function_Tools_gs_collector_Case0016start------')
        self.dbusernode = Node('PrimaryDbUser')
        self.constant = Constant()

    def test_server_tools1(self):
        self.log.info('-----------步骤1：将主机IP写入主机名称列表文件---------')
        echo_cmd = f'echo "{self.dbusernode.db_host}" > ' \
            f'{macro.DB_INSTANCE_PATH}/hostfile.txt;'
        self.log.info(echo_cmd)
        echo_msg = self.dbusernode.sh(echo_cmd).result()
        self.log.info(echo_msg)
        current_date = time.strftime("%Y%m%d", time.localtime())
        self.log.info(current_date)
        current_time = time.strftime("%Y%m%d %H:%M", time.localtime())
        self.log.info(current_time)
        self.log.info('-----步骤2：收集日志信息时指定主机名称列表文件（hostfile中是主机IP）-----')
        collector_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_collector --begin-time="{current_date} 00:00" ' \
            f' --end-time="{current_time}" ' \
            f'-f {macro.DB_INSTANCE_PATH}/hostfile.txt;'
        self.log.info(collector_cmd)
        collector_msg = self.dbusernode.sh(collector_cmd).result()
        self.log.info(collector_msg)
        self.assertIn('The host name ' + f"[{self.dbusernode.db_host}]" +
                      ' is not in the cluster', collector_msg)

    def tearDown(self):
        self.log.info('--------------清理环境-------------------')
        self.log.info('--------------步骤3：删除主机名称列表文件---------------')
        rm_cmd = f'rm -rf {macro.DB_INSTANCE_PATH}/hostfile.txt; '
        self.log.info(rm_cmd)
        rm_msg = self.dbusernode.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.log.info('Opengauss_Function_Tools_gs_collector_Case0016finish')
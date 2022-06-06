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
Case Name   : 查询指定服务器所有节点的信息并将结果输出到指定文件
Description :
    1.查询指定服务器所有节点的信息并将结果输出到指定文件
    2.查看输出文件是否生成
    3.删除输出文件
Expect      :
    1.查询成功
    2.输出文件生成成功
    3.删除成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0075start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.logger.info('------查询指定服务器所有节点的信息并将结果输出到指定文件-------')
        self.logger.info('-----查看主机名称-----')
        check_cmd = f'hostname'
        self.logger.info(check_cmd)
        hostname = self.dbuser_node.sh(check_cmd).result()
        self.logger.info(hostname)
        om_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om ' \
            f'-t status ' \
            f'-h {hostname} ' \
            f'--all  ' \
            f'-o {macro.DB_INSTANCE_PATH}/output.txt; '
        self.logger.info(om_cmd1)
        om_msg1 = self.dbuser_node.sh(om_cmd1).result()
        self.logger.info(om_msg1)
        self.logger.info('------查询是否结果输出到指定文件-------')
        cat_cmd = f'cat {macro.DB_INSTANCE_PATH}/output.txt;'
        cat_msg = self.dbuser_node.sh(cat_cmd).result()
        self.logger.info(cat_msg)
        self.assertIn('cluster_state',  cat_msg)

    def tearDown(self):
        self.logger.info('--------------清理环境-------------------')
        clear_cmd = f'rm -rf {macro.DB_INSTANCE_PATH}/output.txt;'
        self.logger.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        self.logger.info(clear_msg)
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0075finish--')

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
Case Name   : 指定--bindir参数打印用户可执行文件的路径是否成功
Description :
    1.执行命令打印用户可执行文件信息
Expect      :
    1.执行命令打印用户可执行文件信息成功
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('-------------------this is setup--------------------')
        LOG.info('---Opengauss_Function_Tools_pg_config_Case0001开始执行---')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('--------------截取cluster路径-------------------')
        instance_path1 = f'{macro.DB_INSTANCE_PATH}'
        instance_path = instance_path1.rstrip('/')
        LOG.info('实例路径为：' + instance_path)
        index1 = instance_path.find('/')
        index2 = instance_path.rfind('/')
        self.cluster_path = instance_path[index1:index2]
        LOG.info(self.cluster_path)

        LOG.info('----------执行命令打印用户可执行文件信息-----------')
        bin_cmd = f'''source {macro.DB_ENV_PATH};
            pg_config --bindir;'''
        LOG.info(bin_cmd)
        bin_msg = self.PrimaryNode.sh(bin_cmd).result()
        LOG.info(bin_msg)
        bin_path = self.cluster_path + '/app/bin'
        LOG.info(bin_path)
        self.assertIn(bin_path, bin_msg)

    def tearDown(self):
        LOG.info('-----------------this is tearDown-------------------')
        # 无需清理环境
        LOG.info('---Opengauss_Function_Tools_pg_config_Case0001执行完成---')

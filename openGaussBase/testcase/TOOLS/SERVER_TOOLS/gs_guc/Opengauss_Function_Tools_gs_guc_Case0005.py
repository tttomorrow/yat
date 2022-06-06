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
Case Name   : 检查配置文件中参数，指定主机名称-N不指定数据库实例路径-D/实例名称-I
Description :
    1.检查指定主机
    2.检查所有主机
Expect      :
    1.执行失败：-D or -I are mandatory for executing gs_guc.
    2.执行失败：-D or -I are mandatory for executing gs_guc.
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0005开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        LOG.info('------------------检查指定主机------------------')
        check_cmd = f'''hostname'''
        LOG.info(check_cmd)
        hostname = self.dbuser_node.sh(check_cmd).result()
        check_cmd1 = f'''source {macro.DB_ENV_PATH};
                        gs_guc check -N {hostname} -c "track_activities"'''
        LOG.info(check_cmd1)
        msg1 = self.dbuser_node.sh(check_cmd1).result()
        LOG.info(msg1)
        self.assertIn('ERROR: -D or -I are mandatory for executing gs_guc.',
                      msg1)

        LOG.info('------------------检查所有主机------------------')
        check_cmd2 = f'''source {macro.DB_ENV_PATH}
                     gs_guc check -N all  -c "track_activities"'''
        LOG.info(check_cmd2)
        msg2 = self.dbuser_node.sh(check_cmd2).result()
        LOG.info(msg2)
        self.assertIn('ERROR: -D or -I are mandatory for executing gs_guc.',
                      msg2)

    def tearDown(self):
        LOG.info('-----无需清理环境-----')
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0005执行结束-----')

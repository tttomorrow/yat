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
Case Name   : 修改配置文件的参数，指定主机名称-N不指定数据库实例路径-D/实例名称-I
Description :
    1.查看authentication_timeout参数:
    2.设置authentication_timeout参数为59s:
Expect      :
    1.查看成功
    2.设置失败
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
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0010开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools1(self):
        LOG.info('------查看authentication_timeout参数------')
        excute_cmd = f"source {macro.DB_ENV_PATH};" \
            f"cat {macro.DB_INSTANCE_PATH}/postgresql.conf|grep " \
            f"authentication_timeout"
        LOG.info(excute_cmd)
        msg1 = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg1)
        self.assertIn('1min', msg1)
        LOG.info('----设置authentication_timeout参数为59s-----')
        excute_cmd2 = f'''source {macro.DB_ENV_PATH};
            gs_guc set -N all -c "authentication_timeout= 59s" '''
        LOG.info(excute_cmd2)
        msg1 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg1)
        self.assertIn("ERROR: -D or -I are mandatory for executing gs_guc.",
            msg1)

    def tearDown(self):
        LOG.info('----------------无需清理环境-----------------------')
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0010执行结束-----')

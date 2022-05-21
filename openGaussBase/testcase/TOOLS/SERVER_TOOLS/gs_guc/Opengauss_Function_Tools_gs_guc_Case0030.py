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
Case Name   : 修改配置文件中参数时不使用set
Description :
    1.查看logging_collector默认值
    2.设置logging_collector
Expect      :
    1.显示成功
    2.执行失败
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
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0030开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()

    def test_server_tools(self):
        LOG.info('----查看logging_collector默认值----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc check -N all -D {macro.DB_INSTANCE_PATH} -c \
        " logging_collector";'''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('logging_collector=on', msg)

        LOG.info('----设置logging_collector为off----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                        gs_guc  -N all -I all -c "logging_collector =off";
                        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('gs_guc: no operation specified', msg)

    def tearDown(self):
        LOG.info('----------------无需清理环境-----------------------')
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0030执行结束----')

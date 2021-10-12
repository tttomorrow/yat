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
Case Name   : reload 方式设置认证参数：HOSTTYPE DATABASE USERNAME HOSTNAME
Description :
    1.设置认证参数
    2.查看是否设置成功
    3.删除已经设置的客户端认证策略
Expect      :
    1.设置认证参数成功
    2.查看成功
    3.删除已经设置的客户端认证策略成功
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
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0025开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools(self):
        LOG.info('-----设置认证参数并查看是否设置成功-----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc reload -N all -I all -h "hostssl all all ctupopenga00011  md5";
        cat {macro.DB_INSTANCE_PATH}/pg_hba.conf | grep 'hostssl'|\
        grep 'ctupopenga00011';'''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('Success to perform gs_guc!', msg)
        self.assertIn('hostssl all all ctupopenga00011  md5', msg)

    def tearDown(self):
        LOG.info('---------删除的认证策略---------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
        sed -i 's/\hostssl all all ctupopenga00011  \
md5/\ /g' {macro.DB_INSTANCE_PATH}/pg_hba.conf;
        cat {macro.DB_INSTANCE_PATH}/pg_hba.conf | grep 'hostssl'|\
        grep 'ctupopenga00011';'''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('', msg)

        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0025执行结束-----')

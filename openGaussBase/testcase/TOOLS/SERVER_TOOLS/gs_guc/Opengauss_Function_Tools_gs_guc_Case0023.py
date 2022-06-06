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
Case Name   : reload 方式设置认证参数：HOSTTYPE DATABASE USERNAME IPADDR IPMASK
Description :
    1.设置认证参数
    2.设置认证参数
    3.查看是否设置成功
    4.注释已经设置的客户端认证策略
Expect      :
    1.设置失败
    2.设置完成
    3.设置成功
    4.注释成功
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
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0023开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools(self):
        LOG.info('------------------设置认证参数，合理报错------------------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc reload -N all -I all -h "local all all 127.0.0.1 
        255.255.255.255  reject"'''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('ERROR: Invalid argument as invalid '
                      'authentication method "127.0.0.1"', msg)

        LOG.info('------------------设置认证参数并查看是否设置成功------------------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
    gs_guc reload -N all -I all -h "local all all  reject";
    cat {macro.DB_INSTANCE_PATH}/pg_hba.conf | grep 'reject'| grep 'local'
    '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('Success to perform gs_guc!', msg)
        self.assertIn('local all all  reject', msg)

        LOG.info('-----注释已经设置的客户端认证策略并查看是否注释成功-----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc reload -N all -I all -h "local all all";
    cat {macro.DB_INSTANCE_PATH}/pg_hba.conf | grep 'reject'| grep '#local' 
    '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('#local all all  reject', msg)

        LOG.info('----恢复客户端认证策略并查看是否恢复成功----')
        check_cmd = f'''source {macro.DB_ENV_PATH}
        gs_guc reload -N all -I all -h "local all all  trust"
        cat {macro.DB_INSTANCE_PATH}/pg_hba.conf | grep 'trust'| grep 'local'
        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('local all all  trust', msg)

    def tearDown(self):
        LOG.info('----恢复环境----')
        check_cmd = f'''source {macro.DB_ENV_PATH}
                        gs_guc reload -N all -I all -h "local all all  trust"
                        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0023执行结束----')

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
Case Name   : 将已设置的参数值修改为默认值（reload方式）
Description :
    1.查看max_connections的参数值
    2.设置max_connections参数为1000
    3.重启数据库
    4.查看max_connections的参数值
    5.恢复默认值：
    6.重启数据库
    7.恢复设置
    8.重启数据库
    9.查看max_connections的参数值
Expect      :
    1.查看成功
    2.设置完成
    3.数据库重启成功
    4.查看设置成功
    5.恢复默认值设置成功
    6.数据库重启成功
    7.恢复设置成功
    8.数据库重启成功
    9.查看设置成功
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
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0016开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools(self):
        LOG.info('---------查看max_connections的参数值---------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                       gs_guc check -N all -D {macro.DB_INSTANCE_PATH}\
                        -c " max_connections" '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('max_connections=5000', msg)
        LOG.info('---------设置max_connections参数为1000---------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                      gs_guc set  -D {macro.DB_INSTANCE_PATH} \
                      -c "max_connections=1000"'''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('max_connections=1000', msg)
        LOG.info('------------重启数据库-----------')
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        LOG.info('---------查看max_connections的参数值---------')
        check_cmd = f'''source {macro.DB_ENV_PATH}
                        gs_guc check -N all -D {macro.DB_INSTANCE_PATH} \
                        -c "max_connections" '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('max_connections=1000', msg)
        LOG.info('---------恢复默认值---------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                        gs_guc reload  -D {macro.DB_INSTANCE_PATH} \
                        -c "max_connections=5000"'''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('max_connections=5000', msg)
        LOG.info('---------查看max_connections的参数值---------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                        gs_guc check -N all -D {macro.DB_INSTANCE_PATH} \
                        -c " max_connections" '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('max_connections=5000', msg)

    def tearDown(self):
        LOG.info('---------恢复默认值---------')
        check_cmd = f'''source {macro.DB_ENV_PATH};
                        gs_guc reload  -D {macro.DB_INSTANCE_PATH} \
                        -c "max_connections=5000"'''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('max_connections=5000', msg)
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0016执行结束-----')

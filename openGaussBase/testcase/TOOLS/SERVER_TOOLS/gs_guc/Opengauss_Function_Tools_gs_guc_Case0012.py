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
Case Name   : 修改配置文件的参数，指定参数名称-c
Description :
    1.查看authentication_timeout参数
    2.设置时-c不指定具体的参数：
    3.设置authentication_timeout参数为59s
    4.重启数据库
    5.查看设置后的参数值authentication_timeout参数
    6.恢复默认值：
    7.重启数据库
    8.查看参数是否生效
Expect      :
    1.检查成功
    2.执行失败
    3.设置成功
    4.数据库重启成功
    5.查看成功
    6.恢复成功
    7.数据库重启成功
    8.参数设置成功
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
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0012开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        LOG.info('-----查看authentication_timeout参数-----')
        excute_cmd = f'''source {macro.DB_ENV_PATH}
                        cat {macro.DB_INSTANCE_PATH}/postgresql.conf|grep \
                        authentication_timeout '''
        LOG.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn('authentication_timeout = 1min\t\t# 1s-600s', msg)
        LOG.info('------设置时-c不指定具体参数------')
        excute_cmd = f'''
                        source {macro.DB_ENV_PATH}
                        gs_guc set  -D {macro.DB_INSTANCE_PATH} -c '''
        LOG.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn("gs_guc: option requires an argument -- 'c'", msg)
        LOG.info('------设置authentication_timeout参数为59s------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
                        gs_guc set  -D {macro.DB_INSTANCE_PATH} -c \
                        "authentication_timeout= 59s" '''
        LOG.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn("gs_guc set: authentication_timeout=59s", msg)
        LOG.info('---------------------重启数据库--------------------')
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        LOG.info('-----查看authentication_timeout参数-----')
        sql_cmd = '''show authentication_timeout;'''
        excute_cmd = f'''
        source {macro.DB_ENV_PATH};
        gsql -d {self.dbuser_node.db_name} -p {self.dbuser_node.db_port}\
         -c "{sql_cmd}"'''
        LOG.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn('59s', msg)
        LOG.info('---------------------恢复默认值--------------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH}
        gs_guc set  -D {macro.DB_INSTANCE_PATH} -c\
        "authentication_timeout= 1min" '''
        LOG.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn("gs_guc set: authentication_timeout=1min", msg)
        LOG.info('---------------------重启数据库--------------------')
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        LOG.info('-----查看authentication_timeout参数-----')
        excute_cmd = f'''
        source {macro.DB_ENV_PATH}
cat {macro.DB_INSTANCE_PATH}/postgresql.conf|grep authentication_timeout 
'''
        LOG.info(excute_cmd)
        msg1 = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg1)
        self.assertIn('authentication_timeout = 1min\t\t# 1s-600s', msg1)

    def tearDown(self):
        LOG.info('---------------------恢复默认值--------------------')
        excute_cmd = f'''
                        source {macro.DB_ENV_PATH}
                        gs_guc set  -D {macro.DB_INSTANCE_PATH} -c \
                        "authentication_timeout= 1min" '''
        LOG.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn("gs_guc set: authentication_timeout=1min", msg)
        LOG.info('---------------------重启数据库--------------------')
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0012执行结束-----')

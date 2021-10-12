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
Case Name   : 修改配置文件的参数，不指定主机名称-N指定数据库实例路径-D/实例路径-I
Description :
    1.查看authentication_timeout参数:
    2.设置authentication_timeout参数为59s:
    3.重启数据库
    4.连接数据库
    5.查看设置后的参数值authentication_timeout参数:
    6.退出数据库
    7.恢复默认值
    8.重启数据库
    9.查看参数是否生效
Expect      :
    1.查看成功
    2.设置成功
    3.数据库重启成功
    4.数据库连接成功
    5.查看成功
    6.退出数据库成功
    7.恢复成功
    8.数据库重启成功
    9.参数设置成功
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
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0011开始执行-----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        LOG.info('-----查看authentication_timeout参数-----')
        excute_cmd1 = f"source {macro.DB_ENV_PATH};" \
            f"cat {macro.DB_INSTANCE_PATH}/postgresql.conf|grep " \
            f"authentication_timeout;"
        LOG.info(excute_cmd1)
        msg1 = self.dbuser_node.sh(excute_cmd1).result()
        LOG.info(msg1)
        self.assertIn('1min', msg1)
        LOG.info('-----设置authentication_timeout参数为59s-----')
        excute_cmd2 = f'''source {macro.DB_ENV_PATH}
            gs_guc set -D {macro.DB_INSTANCE_PATH} -c \
            "authentication_timeout= 59s" 
            '''
        LOG.info(excute_cmd2)
        msg2 = self.dbuser_node.sh(excute_cmd2).result()
        LOG.info(msg2)
        self.assertIn('gs_guc set: authentication_timeout=59s', msg2)
        LOG.info('---------------------重启数据库--------------------')
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        LOG.info('-----查看authentication_timeout参数-----')
        sql_cmd = "show authentication_timeout;"
        excute_cmd3 = f'''source {macro.DB_ENV_PATH} ;
            gsql -d {self.dbuser_node.db_name} \
            -p {self.dbuser_node.db_port} -c "{sql_cmd}"
            '''
        LOG.info(excute_cmd3)
        msg = self.dbuser_node.sh(excute_cmd3).result()
        LOG.info(msg)
        self.assertIn('59s', msg)

    def tearDown(self):
        LOG.info('---------------------恢复默认值--------------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_guc set  -D {macro.DB_INSTANCE_PATH} \
            -c"authentication_timeout= 1min" 
            '''
        LOG.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg)
        LOG.info('---------------------重启数据库--------------------')
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)
        LOG.info("-----Opengauss_Function_Tools_gs_guc_Case0011执行结束-----")

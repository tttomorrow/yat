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
Case Name   : 开启关闭集群内安装kerberos服务端客户端认证时指定日志文件及存放路径
Description :
    1.开启集群内安装kerberos服务端认证时指定日志文件及存放路径
    2.查看日志文件生成与否
    3.开启集群内安装kerberos客户端认证时指定日志文件及存放路径
    4.查看日志文件
    5.关闭集群内安装kerberos认证时指定日志文件及存放路径
    6.查看日志文件
    7.删除日志文件
Expect      :
    1.开启成功
    2.查看成功
    3.开启成功
    5.查看成功
    6.关闭成功
    7.查看成功
    8.删除成功
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
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0093start--')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()
        self.gs_om_succuss_msg = 'Successfully'

    def test_server_tools1(self):
        self.logger.info('------开启集群内安装kerberos服务端认证时指定日志文件及存放路径-------')
        om_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om ' \
            f'-t kerberos ' \
            f'-m install ' \
            f'-U {self.dbuser_node.ssh_user} ' \
            f'-l {macro.DB_INSTANCE_PATH}/logserver/gs_om.log --krb-server;'
        self.logger.info(om_cmd1)
        om_msg1 = self.dbuser_node.sh(om_cmd1).result()
        self.logger.info(om_msg1)
        self.assertIn(self.gs_om_succuss_msg, om_msg1)
        find_cmd1 = f'find {macro.DB_INSTANCE_PATH}/logserver ' \
            f'-type f ' \
            f'-name "*.log";'
        find_msg1 = self.dbuser_node.sh(find_cmd1).result()
        self.logger.info(find_msg1)
        self.assertIn('log', find_msg1)
        self.logger.info('------开启集群内安装kerberos客户端认证时指定日志文件及存放路径-------')
        om_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om ' \
            f'-t kerberos ' \
            f'-m install ' \
            f'-U {self.dbuser_node.ssh_user} ' \
            f'-l {macro.DB_INSTANCE_PATH}/logclient/gs_om.log' \
            f' --krb-client;'
        self.logger.info(om_cmd2)
        om_msg2 = self.dbuser_node.sh(om_cmd2).result()
        self.logger.info(om_msg2)
        self.assertIn(self.gs_om_succuss_msg, om_msg2)
        find_cmd2 = f'find {macro.DB_INSTANCE_PATH}/logclient ' \
            f'-type f ' \
            f'-name "*.log";'
        find_msg2 = self.dbuser_node.sh(find_cmd2).result()
        self.logger.info(find_msg2)
        self.assertIn('log', find_msg2)
        self.logger.info('------卸载集群内kerberos认证时指定日志文件及存放路径-------')
        om_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om' \
            f' -t kerberos' \
            f' -m uninstall' \
            f' -U {self.dbuser_node.ssh_user}' \
            f' -l {macro.DB_INSTANCE_PATH}/logun/gs_om.log;'
        self.logger.info(om_cmd2)
        om_msg2 = self.dbuser_node.sh(om_cmd2).result()
        self.logger.info(om_msg2)
        self.assertIn(self.gs_om_succuss_msg, om_msg2)
        find_cmd2 = f'find {macro.DB_INSTANCE_PATH}/logun ' \
            f'-type f ' \
            f'-name "*.log";'
        find_msg2 = self.dbuser_node.sh(find_cmd2).result()
        self.logger.info(find_msg2)
        self.assertIn('log', find_msg2)

    def tearDown(self):
        self.logger.info('--------------清理环境-------------------')
        clear_cmd = f'rm -rf {macro.DB_INSTANCE_PATH}/logserver;' \
            f'rm -rf {macro.DB_INSTANCE_PATH}/logclient;' \
            f'rm -rf {macro.DB_INSTANCE_PATH}/logun;'
        self.logger.info(clear_cmd)
        clear_msg = self.dbuser_node.sh(clear_cmd).result()
        self.logger.info(clear_msg)
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0093finish--')

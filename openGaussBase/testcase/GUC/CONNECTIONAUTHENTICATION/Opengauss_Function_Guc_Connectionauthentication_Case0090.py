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
Case Type   : GUC
Case Name   : unix_socket_directory参数使用gs_guc set设置为空值
Description :
              1、查看unix_socket_directory默认值；
              source /opt/opengauss810/env;
              gs_guc check -D {cluster/dn1} -c unix_socket_directory
              2、使用数据库用户在有权限的目录下创建测试目录；
              mkdir -p /home/testdn/cluster/tmp
              3、使用设置gs_guc set设置unix_socket_directory
              gs_guc set -D {cluster/dn1} -c "unix_socket_directory=' '"
Expect      :
              1、显示默认值；
              2、创建成功；
              3、参数修改失败；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0090开始==')
        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_startdb(self):
        self.log.info("获取默认值")
        getcmd = f"source {macro.DB_ENV_PATH};" \
                 f"gsql -d {self.db_user_node.db_name} " \
                 f"-p {self.db_user_node.db_port} " \
                 f"-c \"show unix_socket_directory;\" | grep \/"
        self.log.info(getcmd)
        self.res11 = self.db_user_node.sh(getcmd).result()
        self.log.info(self.res11)

        self.log.info("设置unix_socket_directory，重启使其生效")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'unix_socket_directory=\' \'')
        self.log.info(result)
        self.assertTrue(result)
        self.log.info("重启使其生效，并校验预期结果")
        result = COMMONSH.restart_db_cluster()
        self.log.info(result)
        self.assertFalse(result)

        self.log.info("校验参数是否修改成功")
        result = COMMONSH.execute_gsguc('check', self.res11,
                                       'unix_socket_directory')
        self.log.info(result)
        self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'unix_socket_directory=\'{self.res11}\'')
        self.log.info(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Guc_Connectionauthentication_Case0090完成==')

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
Case Type   : GUC
Case Name   : 修改unix_socket_directory，并观察其预期结果
Description :
              1、查看unix_socket_directory默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c unix_socket_directory
              2、socket链接数据库
              gsql -d {self.db_user_node.db_name} -p 55810
              -r -h /opt/opengauss810/cluster/cluster/tmp
              3、使用数据库用户在有权限的目录下创建测试目录；
              mkdir -p /home/testdn/cluster/tmp
              4、设置unix_socket_directory
              gs_guc set -D {cluster/dn1}
              -c "unix_socket_directory='/home/testdn/cluster/tmp'"
              gs_guc set  -N all -D {cluster/dn1}
              -c "unix_socket_directory='/home/testdn/cluster/tmp'"
              5、重启数据库；
              gs_om -t stop && gs_om -t start
              6、socket链接数据库
              gsql -d {self.db_user_node.db_name}
              -p 55810 -r -h /home/testdn/cluster/tmp
              7、正常链接数据库
              gsql -d {self.db_user_node.db_name} -p 55810 -r
Expect      :
              1、显示默认值；
              2、链接数据库成功；
              3、创建成功；
              4、设置成功；
              5、重启成功；
              6、链接成功；
              7、连接失败；
History     :
"""

import os
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
        self.log.info('==Guc_Connectionauthentication_Case0093开始==')
        self.db_user_node = Node(node='PrimaryDbUser')
        self.newpath = os.path.join(macro.DB_INSTANCE_PATH, 'pathTemp')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_startdb(self):
        self.log.info("获取默认值")
        getcmd = f"source {macro.DB_ENV_PATH};" \
                 f"gsql -d {self.db_user_node.db_name} " \
                 f"-p {self.db_user_node.db_port} " \
                 f"-c \"show unix_socket_directory\" | grep \/"
        self.log.info(getcmd)
        self.res11 = self.db_user_node.sh(getcmd).result()
        self.log.info(self.res11)
        self.log.info("socket链接数据库")
        checksql = f"source {macro.DB_ENV_PATH};" \
                   f"gsql -d {self.db_user_node.db_name} " \
                   f"-p {self.db_user_node.db_port} " \
                   f"-c 'show unix_socket_directory';"
        self.log.info(checksql)
        checkresult = self.db_user_node.sh(checksql).result()
        self.assertIn(self.res11, checkresult)

        self.log.info("使用数据库用户在有权限的目录下创建测试目录")
        sql_cmd = self.db_user_node.sh(f'''source {macro.DB_ENV_PATH};
        gs_ssh -c "rm -rf {self.newpath};
        mkdir {self.newpath};ls {self.newpath}"''').result()
        self.log.info(sql_cmd)
        self.assertIn(self.constant.gs_ssh_success_msg, sql_cmd)

        self.log.info("设置unix_socket_directory，重启使其生效")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'unix_socket_directory=\'{self.newpath}\'')
        self.log.info(result)
        self.assertTrue(result)

        COMMONSH.restart_db_cluster()
        self.log.info("socket链接数据库")
        checksql = f"source {macro.DB_ENV_PATH};" \
                   f"gsql -d {self.db_user_node.db_name} " \
                   f"-p {self.db_user_node.db_port} " \
                   f"-h {self.newpath} " \
                   f"-c 'show unix_socket_directory';"
        self.log.info(checksql)
        checkresult = self.db_user_node.sh(checksql).result()
        self.assertIn(self.newpath, checkresult)

        self.log.info("正常连接数据库")
        checksql = f"source {macro.DB_ENV_PATH};" \
                   f"gsql -d {self.db_user_node.db_name} " \
                   f"-p {self.db_user_node.db_port} " \
                   f"-c 'show unix_socket_directory';"
        self.log.info(checksql)
        checkresult = self.db_user_node.sh(checksql).result()
        self.assertIn('failed', checkresult)

        self.log.info("校验参数是否修改成功")
        result = COMMONSH.execute_gsguc('check', self.newpath,
                                       'unix_socket_directory')
        self.log.info(result)
        self.assertTrue(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        result = COMMONSH.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'unix_socket_directory=\'{self.res11}\'')
        self.log.info(result)
        COMMONSH.restart_db_cluster()
        result = self.db_user_node.sh(f'''source {macro.DB_ENV_PATH};
        gs_ssh -c "rm -rf {self.newpath};
        ls {self.newpath}"''').result()
        self.log.info(result)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.assertIn(self.constant.NO_FILE_MSG, result)
        self.log.info('==Guc_Connectionauthentication_Case0093完成==')

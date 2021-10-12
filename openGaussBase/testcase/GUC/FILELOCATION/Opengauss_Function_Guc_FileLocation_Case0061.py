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
Case Name   : 使用ALTER SYSTEM SET修改参数external_pid_file为非字符类型12345
Description : 
              1、查看external_pid_file默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c external_pid_file
              2、 使用ALTER SYSTEM SET修改参数external_pid_file为非字符类型
              ALTER SYSTEM SET external_pid_file to 123456;
Expect      :
              1、显示默认值；
              2、参数修改失败；
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
        self.log.info('==Guc_FileLocation_Case0061开始==')

        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        check = COMMONSH.execut_db_sql(f'''show external_pid_file;''')
        self.log.info(check)
        self.assertEqual("", check.split("\n")[-2].strip())

        self.log.info("设置external_pid_file为非字符类型")
        altersql1 = "source " + macro.DB_ENV_PATH \
                    + f";gsql -d {self.db_user_node.db_name} -p " \
                    + self.db_user_node.db_port \
                    + " -c \"ALTER SYSTEM " \
                      "set external_pid_file to 12345;\""
        self.log.info(altersql1)
        sqlresult1 = self.db_user_node.sh(altersql1).result()
        self.log.info(sqlresult1)
        self.assertIn('ALTER SYSTEM SET', sqlresult1)
        self.log.info("重启使其生效，观察预期结果")
        COMMONSH.restart_db_cluster()
        self.log.info("在相应配置文件中查看校验配置")
        showcmd = '''source ''' + macro.DB_ENV_PATH \
                  + ''';gs_guc check -D ''' + macro.DB_INSTANCE_PATH \
                  + ''' -c external_pid_file'''
        self.log.info(showcmd)
        check = self.db_user_node.sh(showcmd).result()
        self.log.info(check)
        self.assertIn('12345', check)

    def tearDown(self):
        self.log.info("恢复该参数默认值")
        gucsetcmd = '''source ''' + macro.DB_ENV_PATH \
                    + ''';gs_guc set -D ''' + macro.DB_INSTANCE_PATH \
                    + ''' -c "external_pid_file=\'\'"'''
        self.log.info(gucsetcmd)
        self.db_user_node.sh(gucsetcmd)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_FileLocation_Case0061完成==')

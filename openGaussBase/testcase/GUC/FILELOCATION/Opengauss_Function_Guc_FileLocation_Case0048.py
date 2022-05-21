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
Case Name   : 使用ALTER SYSTEM SET修改参数ident_file为空值
Description :
              1、查看ident_file默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c ident_file
              2、使用ALTER SYSTEM SET修改数据库参数ident_file为空值
              ALTER SYSTEM SET ident_file to ;
              3、重启使其生效，观察预期结果；
              gs_om -t stop && gs_om -t start
Expect      :
              1、显示默认值；
              2、参数修改成功；
              3、重启成功，预期结果正常；
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
        self.log.info('==Guc_FileLocation_Case0048开始==')

        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        check = COMMONSH.execut_db_sql(f'''show ident_file;''')
        self.log.info(check)
        self.assertIn(f"{macro.DB_INSTANCE_PATH}/pg_ident.conf", check)

        self.log.info("使用aLTER SYSTEM SET设置ident_file为空值")
        altersql1 = "source " + macro.DB_ENV_PATH \
                    + f";gsql -d {self.db_user_node.db_name} -p " \
                    + self.db_user_node.db_port \
                    + " -c \"ALTER SYSTEM set ident_file to ' ';\""
        self.log.info(altersql1)
        sqlresult1 = self.db_user_node.sh(altersql1).result()
        self.log.info(sqlresult1)
        self.assertIn('ALTER SYSTEM SET', sqlresult1)

        self.log.info("重启数据库校验预期结果")
        COMMONSH.restart_db_cluster()
        result = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in result or "Degraded" in result)

    def tearDown(self):
        self.log.info("恢复该参数默认值")
        gucsetcmd = '''source ''' + macro.DB_ENV_PATH \
                    + ''';gs_guc set -N all -I all -c "ident_file=\'''' \
                    + macro.DB_INSTANCE_PATH + '''/pg_ident.conf\'"'''
        self.log.info(gucsetcmd)
        self.db_user_node.sh(gucsetcmd)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_FileLocation_Case0048完成==')

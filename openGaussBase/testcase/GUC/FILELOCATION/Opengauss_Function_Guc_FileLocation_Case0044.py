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
Case Name   : ident_file参数使用gs_guc reload设置为非字符类型
Description :
              1、查看ident_file默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c ident_file
              2、使用设置s_guc set设置ident_file为12345
              gs_guc reload -D {cluster/dn1} -c "ident_file=12345"
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
        self.log.info('==Guc_FileLocation_Case0044开始==')

        self.db_user_node = Node(node='PrimaryDbUser')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        check = COMMONSH.execut_db_sql(f'''show ident_file;''')
        self.log.info(check)
        self.assertIn(f"{macro.DB_INSTANCE_PATH}/pg_ident.conf", check)

        self.log.info("ident_file参数使用gs_guc reload设置为非字符类型")
        gucsetcmd = '''source ''' + macro.DB_ENV_PATH \
                    + ''';gs_guc reload -D ''' + macro.DB_INSTANCE_PATH \
                    + ''' -c "ident_file=12345"'''
        self.log.info(gucsetcmd)
        gucresult = self.db_user_node.sh(gucsetcmd).result()
        self.assertIn('ERROR', gucresult)

    def tearDown(self):
        self.log.info("恢复该参数默认值")
        gucsetcmd = '''source ''' + macro.DB_ENV_PATH \
                    + ''';gs_guc set -N all -I all -c "ident_file=\'''' \
                    + macro.DB_INSTANCE_PATH + '''/pg_ident.conf\'"'''
        gucresult = self.db_user_node.sh(gucsetcmd).result()
        self.log.info(gucresult)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info('==Guc_FileLocation_Case0044完成==')

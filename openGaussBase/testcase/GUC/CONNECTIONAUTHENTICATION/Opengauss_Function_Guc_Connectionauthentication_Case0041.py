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
Case Name   : 使用ALTER SYSTEM SET修改数据库参数max_connections
Description : 1、查看max_connections默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c max_connections
              2、使用ALTER SYSTEM SET修改数据库参数max_connections;
              （不可小于等于max_wal_senders）
              ALTER SYSTEM set max_connections to 55810;
              3、重启使其生效，观察预期结果。
              gs_om -t stop && gs_om -t start
Expect      : 1、显示默认值；
              2、参数修改成功；
              3、重启生效，预期结果正常。
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH('PrimaryDbUser')


class GucTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Connectionauthentication_Case0041.py start==')

    def test_startdb(self):
        self.log.info("查看max_connections默认值，并校验；")
        result = COMMONSH.execute_gsguc('check', '5000', 'max_connections')
        self.assertTrue(result)
        checksql = COMMONSH.execut_db_sql('''show max_wal_senders;''')
        self.log.info(checksql)
        self.defaultResult = checksql.split("\n")[-2].strip()

        self.log.info("设置max_wal_senders参数并据此设置max_connections")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                        f'max_wal_senders=4')
        self.assertTrue(result)
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = COMMONSH.execut_db_sql(
            f'''ALTER SYSTEM set max_connections to '5810';''')
        self.log.info(sql_cmd)
        self.assertIn("ALTER SYSTEM SET", sql_cmd)
        self.log.info("重启使其生效，并校验预期结果")
        COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        checksql = COMMONSH.execut_db_sql('''show max_connections;''')
        self.log.info(checksql)
        self.assertEqual("5810", checksql.split("\n")[-2].strip())

    def tearDown(self):
        self.log.info("恢复默认值")
        checksql = COMMONSH.execut_db_sql(
            '''show max_wal_senders;show max_connections;''')
        self.log.info(checksql)
        if f'''{self.defaultResult}''' not in checksql \
                or "5000" not in checksql:
            COMMONSH.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'''max_wal_senders={self.defaultResult}''')
            COMMONSH.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'max_connections=5000')
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0041.py finish==')

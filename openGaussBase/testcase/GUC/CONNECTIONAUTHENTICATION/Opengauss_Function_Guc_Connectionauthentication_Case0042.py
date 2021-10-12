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
Case Name   : max_connections参数使用gs_guc set设置为超边界值
Description : 1、查看max_connections默认值；
              source /opt/opengauss810/env
              gs_guc check -D {cluster/dn1} -c max_connections
              2、使用设置gs_guc set设置max_connections为超边界值
              gs_guc set -D {cluster/dn1} -c "max_connections=666666"
              gs_guc set -N all  -D {cluster/dn1} -c "max_connections=666666"
              3、校验是否修改成功；
              show max_wal_senders;
              4、恢复默认值
Expect      : 1、显示默认值；
              2、参数修改成功；
              3、查看参数修改失败，重启失败；
              4、修改成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

COMMONSH = CommonSH('PrimaryDbUser')


class Deletaduit(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Connectionauthentication_Case0042.py start==')
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_startdb(self):
        self.log.info("查看max_connections默认值，并校验；")
        result = COMMONSH.execute_gsguc('check', '5000', 'max_connections')
        self.assertTrue(result)
        sql_cmd = COMMONSH.execut_db_sql('''show max_wal_senders;''')
        self.log.info(sql_cmd)
        self.defaultWalSenders = sql_cmd.split("\n")[-2].strip()

        self.log.info("设置max_wal_senders参数，"
                      "并设置max_connections为超边界值，重启使其生效")
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                        f'max_wal_senders=4')
        self.assertTrue(result)
        result = COMMONSH.execute_gsguc('set', self.constant.GSGUC_SUCCESS_MSG,
                                        f'max_connections=666666')
        self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql(
            '''show max_wal_senders;show max_connections;''')
        self.log.info(sql_cmd)
        if f'{self.defaultWalSenders}' not in sql_cmd \
                or '5000' not in sql_cmd:
            COMMONSH.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'max_wal_senders={self.defaultWalSenders}')
            COMMONSH.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'max_connections=5000')
            COMMONSH.restart_db_cluster()
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0042.py finish==')

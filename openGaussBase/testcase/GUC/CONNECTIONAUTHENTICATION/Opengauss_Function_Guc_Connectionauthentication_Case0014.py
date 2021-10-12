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
Case Type   : GUC参数--连接认证
Case Name   : port参数使用gs_guc set设置为无效值
Description : 1、查看port默认值；
              source /opt/opengauss810/env
              show  port;
              2、使用set修改port为边界值、浮点型，负数，字符，并校验其修改结果。
              gs_guc set -D {cluster/dn1} -c "port= 0"
              gs_guc set -D {cluster/dn1} -c "port= 65536"
              gs_guc set -D {cluster/dn1} -c "port= 65.536"
              gs_guc set -D {cluster/dn1} -c "port= -65536"
              gs_guc set -D {cluster/dn1} -c "port= 'abc'"
              3、恢复默认值
Expect      : 1、显示默认值为安装数据库时指定端口；
              2、超边界值、浮点型和负数修改失败，预期结果正常
              3、恢复默认值成功；
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

COMMONSH = CommonSH('PrimaryDbUser')


class Deletaduit(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('==Connectionauthentication_Case0014.py start==')
        self.user_node = Node("PrimaryDbUser")
        self.constant = Constant()

    def test_startdb(self):
        self.log.info("查看port默认值")
        sql_cmd = COMMONSH.execut_db_sql('show port;')
        self.assertIn(str(self.user_node.db_port), sql_cmd)
        self.log.info("依次设置port为边界值，并校验修改结果")
        invalid_value = ['0', 65536, 65.536, '-65536', 'abc']
        for i in invalid_value:
            result = COMMONSH.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"port={i}")
            self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        msg = COMMONSH.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     f'port={str(self.user_node.db_port)}')
        self.log.info(msg)
        msg = COMMONSH.restart_db_cluster()
        self.log.info(msg)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0014.py finish==')

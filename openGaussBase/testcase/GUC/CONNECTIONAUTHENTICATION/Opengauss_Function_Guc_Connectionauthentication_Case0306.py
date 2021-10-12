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
Case Name   : max_connections参数使用gs_guc set设置为无效值
Description : 1、查看max_connections默认值；
              2、修改gs_guc set为无效值
              3、恢复默认值
Expect      : 1、显示默认值为5000（资料描述是200，om安装时om工具修改）
              2、合理报错
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
        self.log.info('==Connectionauthentication_Case0306.py start==')
        self.user_node = Node("PrimaryDbUser")
        self.constant = Constant()

    def test_startdb(self):
        self.log.info("查看max_connections默认值")
        sql_cmd = COMMONSH.execut_db_sql('show max_connections;')
        self.assertTrue(sql_cmd)
        self.df_value = sql_cmd.split("\n")[-2].strip()
        self.log.info("依次设置max_connections为无效值")
        invalid_value = ['9', '262144', '5000.985', ""]
        for i in invalid_value:
            result = COMMONSH.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"max_connections={i}")
            self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql('show max_connections;')
        self.log.info(sql_cmd)
        if self.df_value != sql_cmd.split('\n')[2].strip():
            msg = COMMONSH.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'max_connections={self.df_value}')
            self.log.info(msg)
            msg = COMMONSH.restart_db_cluster()
            self.log.info(msg)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Connectionauthentication_Case0306.py finish==')

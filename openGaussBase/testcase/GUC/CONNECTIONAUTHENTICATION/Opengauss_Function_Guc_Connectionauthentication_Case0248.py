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
Case Name   : 修改参数comm_usable_memory为无效值
Description :
              1、查看comm_usable_memory默认值；
              show comm_usable_memory;
              2、修改comm_usable_memory分别为102399、102400.25、'test'
              校验其预期结果；
Expect      :
              1、显示默认值为4000MB；
              2、参数修改失败；
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

COMMONSH = CommonSH('PrimaryDbUser')


class GucTest(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.constant = Constant()
        self.log.info('==Guc_Connectionauthentication_Case0248开始==')
        self.db_user_node = Node(node='PrimaryDbUser')

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        sql_cmd = COMMONSH.execut_db_sql('show comm_usable_memory;')
        self.log.info(sql_cmd)
        self.assertEqual('4000MB', sql_cmd.split('\n')[2].strip())
        self.log.info("修改comm_usable_memory为无效值")
        for i in invalid_value:
            result = COMMONSH.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"comm_usable_memory={i}")
            self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql('show comm_usable_memory;')
        self.log.info(sql_cmd)
        if '4000MB' != sql_cmd.split('\n')[2].strip():
            msg = COMMONSH.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"comm_usable_memory='4000MB'")
            self.log.info(msg)
            msg = COMMONSH.restart_db_cluster()
            self.log.info(msg)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Guc_Connectionauthentication_Case0248完成==')

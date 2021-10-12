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
Case Name   : 修改参数comm_max_receiver为无效值
Description :
              1、查看comm_max_receiver默认值；
              show comm_max_receiver;
              2、修改comm_max_receiver分别为0、51、25.25、'test'
              校验其预期结果；
Expect      :
              1、显示默认值为4；
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
        self.log.info('==Guc_Connectionauthentication_Case0244开始==')
        self.db_user_node = Node(node='PrimaryDbUser')

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        sql_cmd = COMMONSH.execut_db_sql('show comm_max_receiver;')
        self.log.info(sql_cmd)
        self.assertEqual('4', sql_cmd.split('\n')[2].strip())
        self.log.info("修改comm_max_receiver为无效值")
        invalid_value = ['0', '51', '25.25' 'test']
        for i in invalid_value:
            result = COMMONSH.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"comm_max_receiver={i}")
            self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql('show comm_max_receiver;')
        self.log.info(sql_cmd)
        if '4' != sql_cmd.split('\n')[2].strip():
            msg = COMMONSH.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'comm_max_receiver=4')
            self.log.info(msg)
            msg = COMMONSH.restart_db_cluster()
            self.log.info(msg)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Guc_Connectionauthentication_Case0244完成==')

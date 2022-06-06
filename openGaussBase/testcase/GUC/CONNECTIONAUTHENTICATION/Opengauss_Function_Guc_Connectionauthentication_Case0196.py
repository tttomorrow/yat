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
Case Type   : GUC参数--连接认证
Case Name   :ssl_renegotiation_limit参数使用gs_guc reload设置为无效值(为保持
             版本兼容保留此参数，修改参数配置不再起作用)
Description :
              1、查看ssl_renegotiation_limit默认值；
              show ssl_renegotiation_limit;
              2、修改ssl_renegotiation_limit分别为-1、2147483648、100.25、
              'test'和空串，校验其预期结果；
Expect      :
              1、显示默认值为0;
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
        self.log.info('==Guc_Connectionauthentication_Case0196开始==')
        self.db_user_node = Node(node='PrimaryDbUser')

    def test_startdb(self):
        self.log.info("查询该参数默认值")
        sql_cmd = COMMONSH.execut_db_sql('show ssl_renegotiation_limit;')
        self.log.info(sql_cmd)
        self.assertEqual('0', sql_cmd.split('\n')[2].strip())
        self.log.info("修改ssl_renegotiation_limit为无效值")
        invalid_value = ['-1', '2147483648', '100.25', 'test', "''"]
        for i in invalid_value:
            result = COMMONSH.execute_gsguc('reload',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"ssl_renegotiation_limit={i}")
            self.assertFalse(result)

    def tearDown(self):
        self.log.info("恢复默认值")
        sql_cmd = COMMONSH.execut_db_sql('show ssl_renegotiation_limit;')
        self.log.info(sql_cmd)
        if '0' != sql_cmd.split('\n')[2].strip():
            msg = COMMONSH.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'ssl_renegotiation_limit=0')
            self.log.info(msg)
            msg = COMMONSH.restart_db_cluster()
            self.log.info(msg)
        status = COMMONSH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('==Guc_Connectionauthentication_Case0196完成==')

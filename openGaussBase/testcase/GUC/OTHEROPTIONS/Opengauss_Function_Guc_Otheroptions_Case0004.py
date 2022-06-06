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
Case Name   : 修改server_version_num，观察预期结果；
Description :
    1、查询server_version_num默认值,show server_version_num;
    2、修改server_version_num为10100，
       gs_guc set -D {cluster/dn1} -c "server_version_num=10100"
    3、恢复默认值；
Expect      :
    1、显示默认值
    2、参数修改失败，固定参数，用户无法修改此参数；
    3、恢复默认值成功
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('PrimaryDbUser')


class GucTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0004开始执行===")
        self.Constant = Constant()
        self.userNode = Node('PrimaryDbUser')
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("======查询server_version_num,默认值为90204======")
        sql_cmd = commonsh.execut_db_sql('''show server_version_num;''')
        logger.info(sql_cmd)
        self.assertEqual("90204", sql_cmd.split("\n")[-2].strip())

        logger.info("======修改server_version为10100，期望：修改失败======")
        result = commonsh.execute_gsguc('set',
                                        self.Constant.GSGUC_SUCCESS_MSG,
                                       "server_version=10100")
        self.assertFalse(result)

    def tearDown(self):
        logger.info("======No Need Clean && No Need Recovery======")
        logger.info("===Opengauss_Function_Guc_Otheroptions_Case0004执行结束===")

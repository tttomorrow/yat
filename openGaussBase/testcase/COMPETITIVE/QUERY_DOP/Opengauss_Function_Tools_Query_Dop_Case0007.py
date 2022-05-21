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
Case Type   : Query_Dop并行查询
Case Name   : 将并行查询参数设置为非法字符*
Description :
    1、更改query_dop参数的值为非法字符*
Expect      :
    1、更改参数失败，报错
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class QueryDopCase(unittest.TestCase):

    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            "---Opengauss_Function_Tools_Query_Dop_Case0007开始执行---")
        self.commonsh = CommonSH("PrimaryDbUser")

    def test_query_dop(self):
        step_text = "---step1:更改query_dop参数的值为非法字符*;expect:更改参数失败，报错---"
        self.logger.info(step_text)
        assert_info = "The parameter(*) exists illegal character:*"
        guc_cmd = self.commonsh.execute_gsguc("set",
                                              assert_info,
                                              "query_dop = *")
        self.logger.info(guc_cmd)
        self.assertTrue(guc_cmd, "执行失败:" + step_text)

    def tearDown(self):
        self.logger.info("---无需清理环境---")
        self.logger.info(
            "---Opengauss_Function_Tools_Query_Dop_Case0007执行结束---")

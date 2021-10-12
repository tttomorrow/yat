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
Case Type   : keyword
Case Name   : opengauss关键字options(非保留)，查询表结构验证字段是否存在
Description :
    1.查看系统表GS_WLM_PLAN_OPERATOR_INFO中options字段
    2.查看系统表PLAN_TABLE_DATA中options字段
Expect      :
    1.系统表GS_WLM_PLAN_OPERATOR_INFO中options字段存在
    2.系统表PLAN_TABLE_DATA中options字段存在
History     :
"""
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Hostname(unittest.TestCase):
    def setUp(self):
        logger.info("-------------------- Opengauss_Function_Keyword_Options_Case0036 开始执行------------------------")

    def test_before_1(self):
        logger.info("------------------------查看系统表GS_WLM_PLAN_OPERATOR_INFO中options字段------------------------")
        SqlMdg = commonsh.execut_db_sql('''select options from GS_WLM_PLAN_OPERATOR_INFO;''')
        logger.info(SqlMdg)
        self.assertIn('options', SqlMdg)
        logger.info("------------------------查看系统表PLAN_TABLE_DATA中options字段--------------------------")
        SqlMdg = commonsh.execut_db_sql('''select options from PLAN_TABLE_DATA;''')
        logger.info(SqlMdg)
        self.assertIn('options', SqlMdg)

    def tearDown(self):
        logger.info("------------------------ 无需清理环境--------------------------")
        logger.info("--------------------- Opengauss_Function_Keyword_Options_Case0036 执行结束-------------------------")

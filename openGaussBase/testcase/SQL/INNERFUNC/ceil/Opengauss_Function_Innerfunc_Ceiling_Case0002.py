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
Case Type   : 功能测试
Case Name   : ceiling入参给正负浮点型
Description : ceiling(dp or numeric)描述：不小于参数的最小整数（ceil的别名）。
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.执行ceil函数取整并断言校验
    步骤 3.清理环境并删除测试表
Expect      :
    步骤 1：数据库状态正常
    步骤 2：环境清理成功
    步骤 3：返回结果正确
History     :
"""

import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

logger = Logger()
common = Common()
commonsh = CommonSH('dbuser')
constant = Constant()


class Ceiling_002(unittest.TestCase):

    def setUp(self):
        logger.info("----------Opengauss_Function_Innerfunc_Function_Ceiling_Case0002开始执行-----------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_ceiling_002(self):
        SqlMdg = commonsh.execut_db_sql('drop table if exists data_01;')
        logger.info(SqlMdg)
        self.assertTrue(SqlMdg.find(constant.TABLE_DROP_SUCCESS) > -1)
        SqlMdg = commonsh.execut_db_sql('create table data_01 (clo1 float,clo2 float);')
        logger.info(SqlMdg)
        self.assertTrue(SqlMdg.find(constant.TABLE_CREATE_SUCCESS) > -1)
        SqlMdg = commonsh.execut_db_sql('insert into data_01 values (21.9224,-125.89);')
        logger.info(SqlMdg)
        self.assertTrue(SqlMdg.find('INSERT 0 1') > -1)
        SqlMdg = commonsh.execut_db_sql('select  ceiling(clo1) , ceiling(clo2) from data_01;')
        common.equal_sql_mdg(SqlMdg, 'ceiling | ceiling', '---------+---------', '22 |    -125', '(1 row)')

    def tearDown(self):
        logger.info("------------------------drop table------------------")
        SqlMdg = commonsh.execut_db_sql('drop table if exists data_01;')
        logger.info(SqlMdg)
        self.assertTrue(SqlMdg.find(constant.TABLE_DROP_SUCCESS) > -1)
        logger.info("--------Opengauss_Function_Innerfunc_Function_Ceiling_Case0002执行结束---------")

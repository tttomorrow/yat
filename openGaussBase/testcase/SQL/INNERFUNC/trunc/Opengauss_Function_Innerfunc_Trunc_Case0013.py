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
Case Name   : trunc只有一个参数且这个参数为整型、浮点型、0、负数
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.执行trunc函数取整并断言校验
    步骤 3.清理环境并删除测试表
Expect      :
    步骤 1：数据库状态正常
    步骤 2：函数返回结果正常
    步骤 3：环境清理成功
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


class Trunc_006(unittest.TestCase):

    def setUp(self):
        logger.info("------Opengauss_Function_Innerfunc_Trunc_Case0013开始执行-------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

    def test_trunc_006(self):

        SqlMdg1 = commonsh.execut_db_sql('drop table if exists data_01;')
        logger.info(SqlMdg1)
        self.assertTrue(SqlMdg1.find(constant.TABLE_DROP_SUCCESS) > -1)
        SqlMdg2 = commonsh.execut_db_sql('create table data_01 (clo1 float,clo2 float);')
        logger.info(SqlMdg2)
        self.assertTrue(SqlMdg2.find(constant.TABLE_CREATE_SUCCESS) > -1)
        SqlMdg3 = commonsh.execut_db_sql('insert into data_01 values (12,12.3);')
        logger.info(SqlMdg3)
        self.assertTrue(SqlMdg3.find('INSERT 0 1') > -1)
        SqlMdg4 = commonsh.execut_db_sql('select trunc(clo1),trunc(clo2) from data_01;')
        logger.info(SqlMdg4)
        common.equal_sql_mdg(SqlMdg4, 'trunc | trunc', '12 |    12', '(1 row)', flag='1')
        SqlMdg5 = commonsh.execut_db_sql('SELECT trunc(-42.8);')
        logger.info(SqlMdg5)
        common.equal_sql_mdg(SqlMdg5, 'trunc', '-42', '(1 row)', flag='1')
        SqlMdg6 = commonsh.execut_db_sql('SELECT trunc(0);')
        logger.info(SqlMdg6)
        common.equal_sql_mdg(SqlMdg6, 'trunc', '0', '(1 row)', flag='1')

    def tearDown(self):
        logger.info("------------------------drop table------------------")
        SqlMdg = commonsh.execut_db_sql('drop table if exists data_01;')
        logger.info(SqlMdg)
        self.assertTrue(SqlMdg.find(constant.TABLE_DROP_SUCCESS) > -1)
        logger.info('--------------Opengauss_Function_Innerfunc_Trunc_Case0013执行结束-----------------')
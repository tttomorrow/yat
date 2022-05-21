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
Case Name   : last_day函数入参是二进制类型，合理报错
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.入参是二进制类型
Expect      :
    步骤 1：数据库状态正常
    步骤 2：不支持二进制类型，合理报错
History     :
"""
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Length_function(unittest.TestCase):

    def setUp(self):
        logger.info("------------Opengauss_Function_Innerfunc_Last_Day_Case0006开始执行--------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):
        logger.info("-------------------入参给二进制，合理报错---------------------")
        sql_cmd1 = r"""drop table if exists tb_test;
                      create table tb_test(COL_1 bytea ,COL_2 raw(100));
                      insert into tb_test values(E'\\\\xDEADBEEF',HEXTORAW('DEADBEEF'));"""
        msg = self.commonsh.execut_db_sql(sql_cmd1)
        logger.info(msg)
        self.assertTrue("INSERT" in msg)

        sql_cmd2 = """select last_day(COL_1) from tb_test;
                      select last_day(COL_2) from tb_test;
                      drop table tb_test CASCADE;"""
        msg2 = self.commonsh.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertTrue("ERROR:  function last_day(bytea) does not exist" in msg2)
        self.assertTrue("ERROR:  function last_day(raw) does not exist" in msg2)

    def tearDown(self):
        logger.info('--------------Opengauss_Function_Innerfunc_Last_Day_Case0006执行结束-------------')

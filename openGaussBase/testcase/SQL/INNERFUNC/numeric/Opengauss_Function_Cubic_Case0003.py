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
Case Type   : 功能测试
Case Name   : cubi函数对于整型数据可以开立方开尽和无法开尽的数据进行运算校验
Description : 描述
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.执行SELECT ||/ {int} AS RESULT;进行开立方并且校验所得结果
Expect      : 
    步骤 1：数据库状态正常
    步骤 2：环境清理成功
    步骤 3：函数返回结果正确
History     : 
"""
import os
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()
common = Common()
commonsh = CommonSH('dbuser')

class Cubic_003(unittest.TestCase):

    def setUp(self):

        logger.info("------------------------Opengauss_Function_Cubic_Case0003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

        global clear_sql
        clear_sql = 'drop table if exists data_01;'
        SqlMdg1 = commonsh.execut_db_sql(clear_sql)
        logger.info(SqlMdg1)

    def test_cubic_003(self):
        sql_cmd = '''create table data_01 (clo1 float,clo2 float);
                insert into data_01 values (1, 124);
                select  ||/clo1 from data_01;
                select  ||/clo2 from data_01;
                SELECT ||/ 101 AS RESULT;
            '''
        SqlMdg2 = commonsh.execut_db_sql(sql_cmd)
        logger.info(SqlMdg2)
        common.equal_sql_mdg(SqlMdg2, 'CREATE TABLE', 'INSERT 0 1', '?column?', '----------', \

    def tearDown(self):
        SqlMdg = commonsh.execut_db_sql(clear_sql)
        logger.info(SqlMdg)
        logger.info('-----------------------Opengauss_Function_Cubic_Case0003执行结束--------------------------')
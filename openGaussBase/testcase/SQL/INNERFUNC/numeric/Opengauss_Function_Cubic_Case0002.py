"""
Case Type   : 功能测试
Case Name   : cubi函数对于浮点型数据可以开立方开尽和无法开尽的数据进行运算校验
Description : 描述
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.执行SELECT ||/ {float} AS RESULT;进行开立方并且校验所得结果
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

class Cubic_002(unittest.TestCase):

    def setUp(self):

        logger.info("------------------------Opengauss_Function_Cubic_Case0002开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        commonsh.ensure_dbstatus_normal()

        global clear_sql
        clear_sql = 'drop table if exists data_01;'
        SqlMdg = commonsh.execut_db_sql(clear_sql)
        logger.info(SqlMdg)

    def test_cubic_002(self):
        sql_cmd = '''create table data_01 (clo1 float,clo2 float);
                insert into data_01 values (0.001, 125.0);
                select  ||/clo1 from data_01;
                select  ||/clo2 from data_01;
                SELECT ||/ 101.1124 AS RESULT;
            '''
        SqlMdg1 = commonsh.execut_db_sql(sql_cmd)
        logger.info(SqlMdg1)
        common.equal_sql_mdg(SqlMdg1, 'CREATE TABLE', 'INSERT 0 1', '?column?', '----------', \
                     '.1', '(1 row)', '', '?column?', '----------', '5', '(1 row)', '', \
                     'result', '------------------', '4.65873641807426', '(1 row)')

    def tearDown(self):
        SqlMdg2 = commonsh.execut_db_sql(clear_sql)
        logger.info(SqlMdg2)
        logger.info('-----------------------Opengauss_Function_Cubic_Case0002执行结束--------------------------')
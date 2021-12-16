"""
Case Type   : 功能测试
Case Name   : 数字操作符>>(二进制右移)，边界值进行右移
Description : 
    1.对各类整数类型数值的边界进行右移
Expect      : 
    1.返回结果正确
History     : 
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0006开始")
        self.commonsh = CommonSH('dbuser')

    def test_right(self):
        cmd = '''drop table if exists test;
        create table test(c1 tinyint, c2 smallint, c3 integer,c4 BIGINT);
        insert into test values(0,-32768,-2147483648,-9223372036854775808);
        insert into test values(255,32767,2147483647,9223372036854775807);'''
        msg0 = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg0)
        cmd1 = "select c1 >> 2, c2 >> 3, c3 >> 32 , c4 >> 63 from test;"
        msg = self.commonsh.execut_db_sql(cmd1)
        LOG.info(msg)
        line1 = '''0 |    -4096 | -2147483648 |       -1'''
        line2 = '''63 |     4095 |  2147483647 |        0'''
        self.assertTrue(msg.splitlines()[-3].strip() == line1)
        self.assertTrue(msg.splitlines()[-2].strip() == line2)

    def tearDown(self):
        self.commonsh.execut_db_sql('drop table if exists test cascade;')
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0006结束")

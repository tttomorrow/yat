"""
Case Type   : 功能测试
Case Name   : 数字操作符>>(二进制右移)，正负整数型值右移
Description :
    1. 对正负整数型值的列进行二进制右移
    2. 对整数整数型数值进行二进制右移
Expect      :
    1. 返回结果正确
    2. 返回结果正确
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

LOG = Logger()


class Function(unittest.TestCase):

    def setUp(self):
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0002开始")
        self.commonsh = CommonSH('dbuser')

    def test_move_right1(self):
        cmd = '''drop table if exists test;
                 create table test(c1 tinyint, c2 smallint, c3 integer);
                 insert into test values(4,-16,1024);
                 insert into test values(128,-32768,1073741824);'''
        msg = self.commonsh.execut_db_sql(cmd)
        LOG.info(msg)
        cmd1 = "select c1 >> 2, c2 >> 3, c3 >> 5 from test;"
        msg0 = self.commonsh.execut_db_sql(cmd1)
        LOG.info(msg0)
        line1 = '''1 |       -2 |       32'''
        line2 = '''32 |    -4096 | 33554432'''
        self.assertTrue(msg0.splitlines()[-3].strip() == line1)
        self.assertTrue(msg0.splitlines()[-2].strip() == line2)

    def test_move_right2(self):
        move = {'-256': [1, -128], '-32767': [14, -2], '8': [2, 2],
                '32768': [12, 8], '262144': [14, 16]}
        for i in range(len(move)):
            cmd = f"""select {list(move.keys())[i]} >> 
                        {list(move.values())[i][0]};"""
            msg1 = self.commonsh.execut_db_sql(cmd)
            LOG.info(msg1)
            result = msg1.splitlines()[-2].strip()
            expect = str(list(move.values())[i][1])
            self.assertTrue(result == expect)

    def tearDown(self):
        self.commonsh.execut_db_sql('drop table if exists test cascade;')
        LOG.info("Opengauss_Function_Innerfunc_Binary_Move_Right_Case0002结束")

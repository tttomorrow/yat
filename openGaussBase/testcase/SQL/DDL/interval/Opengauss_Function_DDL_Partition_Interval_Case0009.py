"""
Case Type   : 功能测试
Case Name   : interval分区,interval_expr非法值校验
Description :
    1.创建间隔分区，interval_expr给多种非法值
Expect      :
    1.合理报错
History     :
"""
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0009开始')

    def test_interval(self):
        data_type = ['decades', '6099999999999999999999999 minutes',
                     '一 hour', 'hour', '两年', 'hihihihi', '*&^%']
        try:
            for i in data_type:
                cmd1 = f'''drop table if exists table1;
                    create table table1(col1 timestamp with time zone)
                    partition by range (col1) interval ('{i}')
                    (partition table1_p1 values less than ('2020-02-01'));
                    '''
                msg1 = self.commonsh.execut_db_sql(cmd1)
                self.log.info(msg1)
                self.assertIn('ERROR:', msg1)
        finally:
            cmd2 = f'''drop table if exists table1;'''
            msg2 = self.commonsh.execut_db_sql(cmd2)
            self.log.info(msg2)

    def tearDown(self):
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0009结束')

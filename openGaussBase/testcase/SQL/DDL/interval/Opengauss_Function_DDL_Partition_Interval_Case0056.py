"""
Case Type   : 功能测试
Case Name   : interval分区,不支持内存表,合理报错
Description :
    1.创建内存表间隔分区
Expect      :
    1.不支持，合理报错
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

CONSTANT = Constant()

COMMONSH = CommonSH('dbuser')


class Function(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0056开始')

    def test_interval(self):
        self.config_item = "enable_incremental_checkpoint=off"
        check_res = COMMONSH.execut_db_sql('''show 
            enable_incremental_checkpoint;''')
        if 'off' != check_res.split('\n')[-2].strip():
            msg = COMMONSH.execute_gsguc('set',
                                         CONSTANT.GSGUC_SUCCESS_MSG,
                                         "enable_incremental_checkpoint=off")
            self.log.info(msg)
            COMMONSH.restart_db_cluster()
            result = COMMONSH.get_db_cluster_status()
            self.assertTrue("Degraded" in result or "Normal" in result)
        cmd1 = f'''drop foreign table if exists pt9;
            create foreign table pt9(
            col_1 smallint,
            col_2 char(30),
            col_3 int,
            col_4 date not null,
            col_5 boolean,
            col_6 nchar(30),
            col_7 float
            )partition by range (col_4) interval ('1 month')
            (   partition pt9_p1 values less than ('2020-03-01'),
                partition pt9_p2 values less than ('2020-04-01'),
                partition pt9_p3 values less than ('2020-05-01'));'''
        msg1 = COMMONSH.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue('ERROR:  syntax error' in msg1)

    def tearDown(self):
        check_res = COMMONSH.execut_db_sql('''show 
            enable_incremental_checkpoint;''')
        if 'on' != check_res.split('\n')[-2].strip():
            msg = COMMONSH.execute_gsguc('set',
                                         CONSTANT.GSGUC_SUCCESS_MSG,
                                         "enable_incremental_checkpoint=on")
            self.log.info(msg)
            COMMONSH.restart_db_cluster()
            result = COMMONSH.get_db_cluster_status()
            self.assertTrue("Degraded" in result or "Normal" in result)
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0056结束')

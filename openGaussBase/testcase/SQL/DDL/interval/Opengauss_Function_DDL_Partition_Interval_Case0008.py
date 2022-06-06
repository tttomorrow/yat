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
Case Name   : interval分区,interval_expr合法值校验
Description :
    1.创建间隔分区，interval_expr给多种合法值
Expect      :
    1.创建成功
History     :
"""
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0008开始')

    def test_interval(self):
        data_type = ['1 second', '60 minutes',
                     '61 minutes', '1 hour',
                     '24.7 hours', '4 hours 3 minutes',
                     '1 day', '32 days', '2 years 3 months',
                     '1 MON -1 HOUR', '40 days 1 minute',
                     '2 years 13 months']
        try:
            for i in data_type:
                cmd1 = f'''drop table if exists table1;
                    create table table1(col1 timestamp with time zone)
                    partition by range (col1) interval ('{i}')
                    (partition table1_p1 values less than ('2020-02-01'));
                    insert into table1 values ('2020-02-23 pst');
                    select relname, parttype, partstrategy, boundaries \
                    from pg_partition where parentid = \
                    (select oid from pg_class where relname = \
                    'table1') order by relname;
                    '''
                msg1 = self.commonsh.execut_db_sql(cmd1)
                self.log.info(msg1)
                self.assertIn('CREATE TABLE', msg1)
        finally:
            cmd2 = f'''drop table if exists table1;'''
            msg2 = self.commonsh.execut_db_sql(cmd2)
            self.log.info(msg2)

    def tearDown(self):
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0008结束')
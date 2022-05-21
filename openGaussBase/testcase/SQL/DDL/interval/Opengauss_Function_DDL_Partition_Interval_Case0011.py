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
Case Name   : INTERVAL分区，分区键为不支持的数据类型时合理报错
Description :
    1.创建间隔分区，分区键为不支持的数据类型
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
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0011开始')

    def test_interval(self):
        data_type = ['bigint', 'binary_integer', 'blob', 'bool',
                     'bytea', 'char(300)', 'character varying(30)',
                     'character(1000)', 'clob', 'decimal',
                     'decimal(6,2)', 'double precision',
                     'float', 'float8', 'int', 'integer',
                     'interval day to second', 'interval year to month',
                     'time with time zone', 'time without time zone',
                     'nchar(100)', 'number(12,6)', 'numeric',
                     'numeric(12,6)', 'nvarchar2(100)',
                     'raw(100)', 'real', 'smallint', 'text',
                     'varchar(1000)', 'varchar2(50)']
        error_info = 'ERROR:  column col1 cannot serve as a interval ' \
                     'partitioning column because of its datatype'
        for i in data_type:
            cmd1 = f'''drop table if exists table1;
                create table table1(col1 {i})
                partition by range (col1) interval ('1 year' ) 
                (partition table1_p1 values less than ('2020-02-01'));'''
            msg1 = self.commonsh.execut_db_sql(cmd1)
            self.log.info(msg1)
            self.assertIn(error_info, msg1)

    def tearDown(self):
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0011结束')
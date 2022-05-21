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
Case Type   : 功能
Case Name   : 创建宽表并创建hash索引
Description :
        1.建表并创建hash索引
        2.使用索引
        3.清理环境
Expect      :
        1.创建成功
        2.数据量大时走索引扫描
        3.清理环境完成
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0010start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = "t_hash_index_0010"
        self.id_name = "i_hash_index_0010"

    def test_standby(self):
        text = '--step1:建表并创建hash索引;expect:创建成功--'
        self.log.info(text)
        create_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists \
            {self.tb_name};
            create table {self.tb_name}
            (c_integer integer,
            c_tinyint tinyint,
            c_binary_integer binary_integer,
            c_bigint bigint,
            c_numeric numeric(10,4),
            c_serial serial,
            c_bigserial bigserial,
            c_real real,
            c_float float(3),
            c_double_precision double precision,
            c_binary_double binary_double,
            c_dec dec(10,3),
            c_integer1 integer(6,3),
            c_money money,
            c_boolean boolean,
            c_char char(10),
            c_varchar varchar(20),
            c_varchar2 varchar2(20),
            c_nvarchar2 nvarchar2(10),
            c_clob clob,
            c_text text,
            c_name name,
            c_char1 "char",
            c_blob blob,
            c_raw raw,
            c_date date,
            c_time time without time zone ,
            c_time1 time with time zone,
            c_time2 timestamp without time zone,
            c_time3 timestamp with time zone,
            c_time4 interval day(3) to second (4),
            c_time5 interval year (6),
            c_point point,
            c_box box,
            c_path path,
            c_circle circle,
            c_inet inet,
            c_bit bit(10),
            c_tsvector tsvector,
            c_tsquery tsquery,
            c_uuid uuid);
            drop index if exists {self.id_name};
            create index {self.id_name} on {self.tb_name} using hash \
            (c_varchar)''')
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, create_cmd,
                      '执行失败:' + text)

        text = '--step2:插入数据;expect:插入成功--'
        self.log.info(text)
        insert_cmd = self.pri_sh.execut_db_sql(f'''insert into {self.tb_name} \
            values(10,10,5,20,123456.122331,
            default,default,10.365456,123456.1234,321.321,10.365456,
            123.123654,123.1236547,25.98,'yes','数据库',
            'column_'|| generate_series(1,5000),'设计',
            '工程师','测试','测试呀','视图','a',empty_blob(),'deadbeef',
            '11-20-2020','21:21:21','21:21:21 pst',
            '2010-12-12','2013-12-11 pst',interval '3' day,interval '2' year, 
            point '(2.0,0)',box '((0,0),(1,1))',path'((1,0),(0,1),(-1,0))',
            circle '((0,0),10)', '192.168.1.14',b'1011111100',
            to_tsvector('english', 'the fat rats'),
            to_tsquery('fat:ab & cats'),
            'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11');''')
        self.log.info(insert_cmd)
        self.assertIn('INSERT 0 5000', insert_cmd)

        text = '--step3:使用索引;expect:查询计划走索引扫描--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''explain analyze select 
            count(*) from {self.tb_name} where c_varchar ='column_20';''')
        self.log.info(sql_cmd)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step4:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists \
            {self.tb_name};''')
        self.log.info(sql_cmd)
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0010finish--')

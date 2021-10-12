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
Case Type   : 分区表
Case Name   : 创建分区表（带主键）后创建全局索引
Description :
    1、创建普通表&创建全局索引
    2、查看表结构
    3、插入数据&查看数据
    4、清理环境
Expect      :
    1、建表成功，创建全局索引成功;
    2、查看表结构成功，主键索引信息正确，索引列顺序一致;
    3、插入数据成功，查看数据成功;
    4、清理环境成功；
History     :
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class DLTEST(unittest.TestCase):

    def setUp(self):
        text = '------Opengauss_Function_DDL_Partition_Case0078开始执行------'
        logger.info(text)
        self.commonsh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.table_name = 't_partition_0078'
        self.index_name1 = 'i_partition_0078_01'
        self.index_name2 = 'i_partition_0078_02'
        self.procedure_name = 'p_partition_0078'

    def test_ddl_partition(self):
        text = '------step1:创建普通表&创建全局索引; expect:成功------'
        logger.info(text)
        create_cmd = f'''drop table if exists {self.table_name};
            create table {self.table_name} (ppid integer,"date" date not null,
            "ncharacter" nchar (14),"decimal" decimal, 
            primary key ("decimal",ppid)) partition by range ("decimal")
            (partition p00 values less than (1000),
             partition p01 values less than (3000),
             partition p02 values less than (5000),
             partition p03 values less than (7000),
             partition p04 values less than (maxvalue));
            create index {self.index_name1} on {self.table_name} 
            ("date" desc nulls first, "decimal") global;
            create index {self.index_name2} on {self.table_name} 
            ("date" nulls first, "decimal") global;'''
        logger.info(create_cmd)
        create_msg = self.commonsh.execut_db_sql(create_cmd)
        logger.info(create_msg)
        assert_1 = self.constant.CREATE_TABLE_SUCCESS in create_msg
        assert_2 = self.constant.CREATE_INDEX_SUCCESS in create_msg
        self.assertTrue(assert_1 and assert_2, '执行失败:' + text)

        text = '------step2:查看表结构; expect:成功------'
        logger.info(text)
        check_cmd = f'''\d+ {self.table_name}'''
        logger.info(check_cmd)
        check_msg = self.commonsh.execut_db_sql(check_cmd)
        logger.info(check_msg)
        assert_1 = 'btree ("decimal", ppid)' in check_msg.splitlines()[-7]
        self.assertTrue(assert_1, '执行失败:' + text)

        text = '------step3.1:插入数据;  expect:成功------'
        logger.info(text)
        insert_cmd = f'''
            create or replace procedure {self.procedure_name}()
            as
            begin
                for i in 0..20000 loop
                insert into {self.table_name} values(i,'2021-8-12','a_'||i,i);
                end loop;
            end;'''
        logger.info(insert_cmd)
        insert_msg = self.commonsh.execut_db_sql(insert_cmd)
        logger.info(insert_msg)
        assert_1 = self.constant.CREATE_PROCEDURE_SUCCESS_MSG in insert_msg
        logger.info(assert_1)
        self.assertTrue(assert_1, '执行失败' + text)

        text = '------step3.2:查看数据; expect:成功------'
        logger.info(text)
        select_cmd = f'''call {self.procedure_name}();
            select count(*) from {self.table_name};'''
        logger.info(select_cmd)
        select_msg = self.commonsh.execut_db_sql(select_cmd)
        logger.info(select_msg)
        assert_1 = '(1 row)' in select_msg.splitlines()[-6]
        logger.info(assert_1)
        assert_2 = '20001' in select_msg.splitlines()[-2]
        logger.info(assert_2)
        self.assertTrue(assert_1 and assert_2, '执行失败' + text)

    def tearDown(self):
        text = '------step4:清理环境; expect:成功------'
        logger.info(text)
        drop_cmd = f'''drop table {self.table_name} cascade;
            drop procedure {self.procedure_name};'''
        drop_msg = self.commonsh.execut_db_sql(drop_cmd)
        logger.info(drop_msg)
        text = '------Opengauss_Function_DDL_Partition_Case0078执行完成------'
        logger.info(text)

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
Case Type   : 智能运维模块ai_virtual_index
Case Name   : 创建表,结合视图,物化视图进行索引查询和删除
Description :
    1.建表1
    2.建表2
    3.建存储过程
    4.向表中插入1000000条数据并统计数据的数量
    5.修改参数enable_hypo_index为on
    6.创建视图
    7.创建虚拟索引1-2
    8.创建物化视图
    9.创建虚拟索引3
    10.清理环境
Expect      :
    1.建表1成功
    2.建表2成功
    3.建存储过程成功
    4.向表1中插入1000000条数据成功,返回表数据的数量
    5.修改参数enable_hypo_index为on成功
    6.创建视图成功
    7.创建虚拟索引1-2均失败
    8.创建物化视图成功
    9.创建虚拟索引3失败
    10.清理环境成功
History     :
"""

import os
import unittest
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class AI(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Con = Constant()
        self.common = Common()
        self.table1 = 't_ai_virtual_index_0004_01'
        self.table2 = 't_ai_virtual_index_0004_02'
        self.table3 = 'hypopg_create_index'
        self.procedure = 'p_virtual_index_0004'
        self.view = 'v_virtual_index_0004_01'
        self.materialized_view = 'v_virtual_index_0004_02'

    def test_ai_virtual_index(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表1 expect:建表1成功'
        self.logger.info(step)
        create_table1 = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table1};
            create table  {self.table1}(col_int int,col_numeric numeric,
            col_float float,col_char char(10),col_text text,col_time time);''')
        self.logger.info(create_table1)
        self.assertIn(self.Con.TABLE_CREATE_SUCCESS, create_table1,
                      "建表1失败" + step)

        step = 'step2:建表2 expect:建表成功'
        self.logger.info(step)
        create_table2 = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table2};
            create table  {self.table2}(col_int int,col_dec dec,
            col_money money,col_boolean boolean,col_char char(10),
            col_clob clob);''')
        self.logger.info(create_table2)
        self.assertIn(self.Con.TABLE_CREATE_SUCCESS, create_table2,
                      "建表2失败" + step)

        step = 'step3:建存储过程 expect:建存储过程1成功'
        self.logger.info(step)
        create_procedure = self.primary_sh.execut_db_sql(f'''
            create or replace procedure {self.procedure}(a int) is
            V_int int;
            V_numeric numeric;
            V_float float;
            V_char char(10);
            V_text text;
            V_time time;
            begin
            for i in 1..a
            loop
            V_int :=i;
            V_numeric :=i+1.11;
            V_float :=i*5.55;
            V_char :='x_'|| i;
            V_text :='V_text_'|| i;
            V_time :='19:41:20';
            execute immediate 'insert into {self.table1} values
            (:p1,:p2,:p3,:p4,:p5,:p6)
            'using V_int,V_numeric,V_float,V_char,V_text,V_time;
            end loop;
            end;''')
        self.logger.info(create_procedure)
        self.assertIn(self.Con.CREATE_PROCEDURE_SUCCESS_MSG,
                      create_procedure, "建存储过程失败" + step)

        step = 'step4:向表1中插入1000000条数据并统计数据的数量' \
               'expect:向表1中插入1000000条数据成功,返回表1数据的数量'
        self.logger.info(step)
        insert_data = self.primary_sh.execut_db_sql(f'''
            call {self.procedure}(1000000);
            select count(*) from {self.table1} ;''')
        self.logger.info(insert_data)
        self.assertIn('1000000', insert_data, '执行失败' + step)

        step = 'step5:修改参数enable_hypo_index为on' \
               'expect:修改参数enable_hypo_index为on成功'
        self.logger.info(step)
        self.init_param = self.common.show_param(
            'enable_hypo_index')
        if 'on' not in self.init_param:
            modify_param = self.primary_sh.execute_gsguc("reload",
                                                         f'''{self.Con.
                                                         GSGUC_SUCCESS_MSG}'''
                                                         , f"enable_hypo_index"
                                                         f"=on",
                                                         single=False)
            self.logger.info(modify_param)
            self.assertTrue(modify_param, "执行失败" + step)

        step = 'step6:创建视图;expect:创建视图成功'
        self.logger.info(step)
        create_view = self.primary_sh.execut_db_sql(f'''
            create view {self.view} as select * from {self.table1} 
            where {self.table1}.col_int<1000;''')
        self.logger.info(create_view)
        self.assertIn(self.Con.CREATE_VIEW_SUCCESS_MSG, create_view,
                      "执行失败" + step)

        step = 'step7:创建虚拟索引1-2  expect;创建虚拟索引1-2失败'
        self.logger.info(step)
        create_index = self.primary_sh.execut_db_sql(
            f'''select * from {self.table3}('create index on {self.view} 
                (col_int)');

                select * from {self.table3}('create index on {self.view} 
                (col_int,col_text)');''')
        self.logger.info(create_index)
        s = f'ERROR:  hypopg: "{self.view}" is not an ordinary table'
        self.assertEqual(create_index.count(s), 2, "执行失败" + step)

        step = 'step8:创建物化视图 expect:创建物化视图成功'
        self.logger.info(step)
        create_view = self.primary_sh.execut_db_sql(
            f'''create materialized view {self.materialized_view} as  select
                * from {self.table1};''')
        self.logger.info(create_view)
        self.assertIn('CREATE MATERIALIZED VIEW', create_view,
                      "执行失败" + step)

        step = 'step9:创建虚拟索引3 expect:创建虚拟索引3失败'
        self.logger.info(step)
        create_index = self.primary_sh.execut_db_sql(
            f'''select * from {self.table3}('create index on 
                {self.materialized_view}(col_int,col_text)');''')
        self.logger.info(create_index)
        s = f'"{self.materialized_view}" is not an ordinary table'
        self.assertIn(s, create_index, "执行失败" + step)

    def tearDown(self):
        step = 'step10:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(
            f'''drop view {self.view};
                drop materialized view {self.materialized_view};
                drop table {self.table1};
                drop table {self.table2};
                drop procedure {self.procedure};''')
        self.init_param1 = self.common.show_param(
            'enable_hypo_index')
        if self.init_param not in self.init_param1:
            modify_param = self.primary_sh.execute_gsguc("reload",
                                                         f'''{self.Con.
                                                         GSGUC_SUCCESS_MSG}'''
                                                         , f"enable_hypo_index"
                                                         f"={self.init_param}",
                                                         single=False)
            self.logger.info(modify_param)
            self.assertTrue(modify_param, "执行失败" + step)
        self.logger.info(clean_environment)
        self.assertEqual(clean_environment.count(self.Con.TABLE_DROP_SUCCESS),
                         2, "执行失败" + step)
        self.assertIn(self.Con.DROP_PROCEDURE_SUCCESS_MSG, clean_environment,
                      "执行失败" + step)
        self.assertIn('DROP MATERIALIZED VIEW', clean_environment,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

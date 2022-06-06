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
Case Type   : 智能运维ai_indexadv模块
Case Name   : 创建ustore表,组合使用where条件,比较运算符,left join连接,order by
              排序,逻辑运算符与范围查询in进行查询索引推荐
Description :
    1.修改参数enable_default_ustore_table为on,重启数据库
    2.查看参数enable_default_ustore_table,undo_zone_count
    3.建表1
    4.建表2
    5.建存储过程1
    6.建存储过程2
    7.向表1中插入100000条数据,向表2中插入数据并统计数据的数量
    8.使用where条件,比较运算符,left join连接,order by排序,逻辑运算符与范围
      查询in进行查询索引推荐
    9.清理环境
Expect      :
    1.修改参数enable_default_ustore_table为on,重启数据库成功
    2.返回参数enable_default_ustore_table为on,undo_zone_count为200000
    3.建表1成功
    4.建表2成功
    5.建存储过程1成功
    6.建存储过程2成功
    7.向表1中插入100000条数据,向表2中插入数据成功,返回表1,表2数据的数量
    8.返回推荐的索引列
    9.清理环境成功
History     :
"""

import os
import unittest
from yat.test import Node
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class SQL(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.dbuserNode = Node('PrimaryDbUser')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.Con = Constant()
        self.table1 = 't_table_ai_indexadv_ustore_0004'
        self.table2 = 't_table_ai_indexadv1_ustore_0004'
        self.procedure1 = 'p_procedure_ustore_insert_0004'
        self.procedure2 = 'p_procedure_ustore1_insert_0004'
        self.index_advise = 'gs_index_advise'

    def test_ai(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:修改参数enable_default_ustore_table为on,重启数据库 ' \
               'expect:修改参数enable_default_ustore_table为on,重启数据库成功'
        self.logger.info(step)
        self.init_param = self.common.show_param(
            'enable_default_ustore_table')
        if 'on' not in self.init_param:
            modify_para1 = self.primary_sh.execute_gsguc("reload",
                                                         f'''{self.Con.
                                                         GSGUC_SUCCESS_MSG}''',
                                                         f"enable_default_"
                                                         f"ustore_"
                                                         f"table=on",
                                                         single=True)
            self.logger.info(modify_para1)
            self.assertTrue(modify_para1, '执行失败' + step)
        msg = self.primary_sh.restart_db_cluster()
        self.logger.info(msg)
        self.assertTrue(msg, '执行失败:' + step)

        step = 'step2:查看参数enable_default_ustore_table' \
               ' expect:返回参数enable_default_ustore_table为on'
        self.logger.info(step)
        show_para = self.common.show_param(
            'enable_default_ustore_table')
        self.logger.info(show_para)
        self.assertIn('on', show_para, "修改参数enable_default_ustore_table"
                      + step)

        step = 'step3:建表1 expect:建表1成功'
        self.logger.info(step)
        create_table1 = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table1};
            create table  {self.table1}(col_int int,col_numeric numeric,
            col_float float,col_char char(10),col_text text,col_time time
            );''')
        self.logger.info(create_table1)
        self.assertIn(self.Con.TABLE_CREATE_SUCCESS, create_table1,
                      "建表1失败" + step)

        step = 'step4:建表2 expect:建表2成功'
        self.logger.info(step)
        create_table2 = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table2};
            create table {self.table2}(col_int int,col_dec dec,
            col_money money,col_boolean boolean,col_char char(10),
            col_clob clob);''')
        self.logger.info(create_table2)
        self.assertIn(self.Con.TABLE_CREATE_SUCCESS, create_table2,
                      "建表2失败" + step)

        step = 'step5:建存储过程1 expect:建存储过程1成功'
        self.logger.info(step)
        create_procedure1 = self.primary_sh.execut_db_sql(f'''
            create or replace procedure {self.procedure1}(a int) is
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
        self.logger.info(create_procedure1)
        self.assertIn(self.Con.CREATE_PROCEDURE_SUCCESS_MSG,
                      create_procedure1, "建存储过程1失败" + step)

        step = 'step6:建存储过程2 expect:建存储过程2成功'
        self.logger.info(step)
        create_procedure2 = self.primary_sh.execut_db_sql(f'''
            create or replace procedure {self.procedure2}() is
            V_int int;
            V_dec dec;
            V_money money;
            V_boolean boolean;
            V_char char(10);
            V_clob clob;
            begin
            for i in 2000..100000
            loop
            V_int :=i;
            V_dec :=i*8.88;
            V_money :=i*2;
            V_boolean :='t';
            V_char :=i ||'_x';
            V_clob :='V_clob_'|| i;
            execute immediate 'insert into {self.table2} values
            (:p1,:p2,:p3,:p4,:p5,:p6)
            'using V_int,V_dec,V_money,V_boolean,V_char,V_clob;
            end loop;
            end;''')
        self.logger.info(create_procedure2)
        self.assertIn(self.Con.CREATE_PROCEDURE_SUCCESS_MSG,
                      create_procedure2, "建存储过程2失败" + step)

        step = 'step7:向表1中插入100000条数据,向表2中插入数据并统计数据的数量' \
               'expect:向表1中插入100000条数据,向表2中插入数据成功,返回' \
               '表1,表2数据的数量'
        self.logger.info(step)
        insert_data = self.primary_sh.execut_db_sql(f'''
            call {self.procedure1}(100000);
            select count(*) from {self.table1} ;
            call {self.procedure2}();
            select count(*) from {self.table2} ;''')
        self.logger.info(insert_data)
        text = '向表1中插入100000条数据,向表2中插入数据并统计数据的数量失败'
        self.assertIn('p_procedure_ustore_insert_0004', insert_data,
                      text + step)
        self.assertIn('p_procedure_ustore1_insert_0004', insert_data,
                      text + step)
        self.assertIn('100000', insert_data, text + step)
        self.assertIn('98001', insert_data, text + step)

        step = 'step8:使用where条件，比较运算符，left join连接，order by排序,' \
               '逻辑运算符与范围查询in进行查询索引推荐 ' \
               'expect:返回推荐的索引列'
        self.logger.info(step)
        index_advise = self.primary_sh.execut_db_sql(f'''
            select * from {self.index_advise}('select {self.table1}.col_int,
            {self.table1}.col_numeric,{self.table2}.col_money
            from {self.table1} left join {self.table2} 
            on {self.table1}.col_int = {self.table2}.col_int
            where {self.table1}.col_time=''19:41:20'' 
            and {self.table1}.col_char in (''x_10000'', ''x_1000000'') 
            order by {self.table1}.col_int desc limit 20;');

            select * from {self.index_advise}('select {self.table1}.col_int,
            {self.table1}.col_numeric,{self.table2}.col_money
            from {self.table1} left join {self.table2} 
            on {self.table1}.col_int = {self.table2}.col_int
            where {self.table1}.col_int < 3000 and 
            {self.table2}.col_money 
            in (''$5,998.00'', ''$5,960.00'',''$5,982.00'') 
            order by {self.table1}.col_int desc limit 20;');

            select * from {self.index_advise}('select {self.table1}.col_int,
            {self.table1}.col_numeric,{self.table2}.col_money
            from {self.table1} left join {self.table2} 
            on {self.table1}.col_int = {self.table2}.col_int
            where {self.table1}.col_time=''19:41:20'' or {self.table1}.col_char 
            in (''x_10000'', ''x_1000000'') 
            order by {self.table1}.col_int desc limit 20;');

            select * from {self.index_advise}('select {self.table1}.col_int,
            {self.table1}.col_numeric,{self.table2}.col_money
            from {self.table1} left join {self.table2} 
            on {self.table1}.col_int = {self.table2}.col_int
            where {self.table1}.col_int < 3000 or {self.table2}.col_money 
            in (''$5,998.00'', ''$5,960.00'',''$5,982.00'')
            order by {self.table1}.col_int desc limit 20;');''')
        self.logger.info(index_advise)
        str1 = f'{self.table1}  | col_int'
        str2 = f'{self.table2} | col_int'
        self.assertEqual(index_advise.count(str1), 4, "执行失败" + step)
        self.assertEqual(index_advise.count(str2), 4, "执行失败" + step)

    def tearDown(self):
        step = 'step9:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table1};
            drop table {self.table2};''')
        self.logger.info(de_table)
        de_procedure = self.primary_sh.execut_db_sql(f'''
            drop procedure {self.procedure1};
            drop procedure {self.procedure2};''')
        self.logger.info(de_procedure)
        para = self.common.show_param(
            'enable_default_ustore_table')
        self.logger.info(para)
        init_param = self.init_param
        if init_param not in para:
            modify_para = self.primary_sh.execute_gsguc("reload",
                                                        f'''{self.Con.
                                                        GSGUC_SUCCESS_MSG}''',
                                                        f"enable_default_"
                                                        f"ustore_"
                                                        f"table="
                                                        f"{init_param}",
                                                        single=True)
            self.logger.info(modify_para)
            self.assertTrue(modify_para, '执行失败' + step)
        self.assertTrue(de_table.count('DROP TABLE') == 2
                        and de_procedure.count('DROP PROCEDURE') == 2,
                        "执行失败" + step)
        self.logger.info('Opengauss_Function_Ai_Indexadv_Ustore_Case0004 '
                         'finish')

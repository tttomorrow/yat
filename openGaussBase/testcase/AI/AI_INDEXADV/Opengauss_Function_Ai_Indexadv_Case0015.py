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
Case Name   : 结合不同的sql语句进行查询索引推荐
Description :
    1.建表1
    2.建表2
    3.建存储过程1
    4.建存储过程2
    5.向表1中插入100000条数据,向表2中插入数据并统计数据的数量
    6.结合union进行查询索引推荐
    7.结合insert语句进行查询索引推荐
    8.结合updata语句进行查询索引推荐
    9.结合create语句进行查询索引推荐
    10.结合视图进行查询索引推荐
    11.结合子查询进行查询索引推荐
    12.结合空条件进行查询索引推荐
    13.结合多条创建索引语句进行查询索引推荐
    14.清理环境
Expect      :
    1.建表1成功
    2.建表2成功
    3.建存储过程1成功
    4.建存储过程2成功
    5.向表1中插入100000条数据,向表2中插入数据成功,返回表1,表2数据的数量
    6.返回推荐的索引列
    7.报错提示无法为查询提供建议，因为找不到查询语句
    8.报错提示无法为查询提供建议，因为找不到查询语句
    9.报错提示无法为查询提供建议，因为找不到查询语句
    10.报错提示无法为查询提供建议，因为无法识别涉及的表
    11.返回推荐的索引列
    12.报错提示必须输入查询条件
    13.报错提示无法为多个查询提供建议
    14.清理环境成功
History     :
    研发代码变更,优化用例适配代码
"""

import unittest
from yat.test import Node
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class SQL(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.dbuserNode = Node('PrimaryDbUser')
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Con = Constant()
        self.table1 = 't_table_ai_indexadv_0015'
        self.table2 = 't_table_ai_indexadv1_0015'
        self.table3 = 't_table_ai_indexadv_test_0015'
        self.procedure1 = 'p_procedure_insert_0015'
        self.procedure2 = 'p_procedure_insert1_0015'
        self.view = 'v_view_ai_index_0015'
        self.index_advise = 'gs_index_advise'

    def test_ai_virtual_index(self):
        self.logger.info('Opengauss_Function_Ai_Indexadv_Case0015 start')
        step = 'step1:建表1 expect:建表1成功'
        self.logger.info(step)
        create_table1 = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table1};
            create table  {self.table1}(col_int int,col_numeric numeric,
            col_float float,col_char char(10),col_text text,col_time time
            );''')
        self.logger.info(create_table1)
        self.assertIn(self.Con.TABLE_CREATE_SUCCESS, create_table1,
                      "建表1失败" + step)

        step = 'step2:建表2 expect:建表2成功'
        self.logger.info(step)
        create_table2 = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table2};
            create table {self.table2}(col_int int,col_dec dec,
            col_money money,col_boolean boolean,col_char char(10),
            col_clob clob);''')
        self.logger.info(create_table2)
        self.assertIn(self.Con.TABLE_CREATE_SUCCESS, create_table2,
                      "建表2失败" + step)

        step = 'step3:建存储过程1 expect:建存储过程1成功'
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

        step = 'step4:建存储过程2 expect:建存储过程2成功'
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

        step = 'step5:向表1中插入100000条数据,向表2中插入数据并统计数据的数量' \
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
        self.assertIn('p_procedure_insert_0015', insert_data,
                      text + step)
        self.assertIn('p_procedure_insert1_0015', insert_data,
                      text + step)
        self.assertIn('100000', insert_data, text + step)
        self.assertIn('98001', insert_data, text + step)

        step = 'step6:结合union进行查询索引推荐 expect:返回推荐的索引列'
        self.logger.info(step)
        index_advise = self.primary_sh.execut_db_sql(f'''
            select * from {self.index_advise}('select col_int,col_char from 
            {self.table1} union select col_int,col_char  from {self.table2} 
            limit 20;');''')
        self.logger.info(index_advise)
        str1 = 'public | t_table_ai_indexadv_0015  |'
        str2 = 'public | t_table_ai_indexadv1_0015 |'
        self.assertIn(str1, index_advise, "执行失败" + step)
        self.assertIn(str2, index_advise, "执行失败" + step)

        step = 'step7:结合insert语句进行查询索引推荐' \
               'expect:报错提示无法为查询提供建议，因为找不到查询语句'
        self.logger.info(step)
        index_advise = self.primary_sh.execut_db_sql(f'''
            select * from {self.index_advise}('insert into {self.table2}
            (col_int) values(8)');''')
        self.logger.info(index_advise)
        str1 = 'ERROR:  can not advise for the query'
        str2 = 'because not found a select statement.'
        self.assertIn(str1, index_advise, "执行失败" + step)
        self.assertIn(str2, index_advise, "执行失败" + step)

        step = 'step8:结合update语句进行查询索引推荐' \
               'expect:报错提示无法为查询提供建议,因为找不到查询语句'
        self.logger.info(step)
        index_advise = self.primary_sh.execut_db_sql(f'''
            select * from {self.index_advise}('update {self.table2} 
            set col_money =''$8,000.00'' where col_int=2000;');''')
        self.logger.info(index_advise)
        str1 = 'ERROR:  can not advise for the query'
        str2 = 'because not found a select statement.'
        self.assertIn(str1, index_advise, "执行失败" + step)
        self.assertIn(str2, index_advise, "执行失败" + step)

        step = 'step9:结合create语句进行查询索引推荐' \
               'expect:报错提示无法为查询提供建议，因为找不到查询语句'
        self.logger.info(step)
        index_advise = self.primary_sh.execut_db_sql(f'''
            select * from {self.index_advise}('create global temp table 
            {self.table3}(id int, val numeric) on commit preserve rows;');''')
        self.logger.info(index_advise)
        str1 = 'ERROR:  can not advise for the query'
        str2 = 'because not found a select statement.'
        self.assertIn(str1, index_advise, "执行失败" + step)
        self.assertIn(str2, index_advise, "执行失败" + step)

        step = 'step10:结合视图进行查询索引推荐' \
               'expect:报错提示无法为查询提供建议,因为无法识别涉及的表'
        self.logger.info(step)
        index_advise = self.primary_sh.execut_db_sql(f'''
            create view {self.view} as select * from {self.table1} 
            where {self.table1}.col_int<1000;
            select * from {self.index_advise}('select * from {self.view};');
            ''')
        self.logger.info(index_advise)
        str1 = 'ERROR:  can not advise for the query'
        str2 = 'because can not recognize involved tables.'
        self.assertIn(str1, index_advise, "执行失败" + step)
        self.assertIn(str2, index_advise, "执行失败" + step)

        step = 'step11:结合子查询进行查询索引推荐 expect:返回推荐的索引列'
        self.logger.info(step)
        index_advise = self.primary_sh.execut_db_sql(f'''
        select * from {self.index_advise}('select col_int,col_char from 
        (select col_int,col_char from {self.table1} union select col_int,
        col_char  from {self.table2} limit 20) where col_char like 
        ''x_74243%'' group by  col_int,col_char order by col_int,col_char;');
        ''')
        self.logger.info(index_advise)
        str1 = 'public | t_table_ai_indexadv_0015  |'
        str2 = 'public | t_table_ai_indexadv1_0015 |'
        self.assertIn(str1, index_advise, "执行失败" + step)
        self.assertIn(str2, index_advise, "执行失败" + step)

        step = 'step12:结合空条件进行查询索引推荐' \
               'expect:报错提示必须输入查询条件'
        self.logger.info(step)
        index_advise = self.primary_sh.execut_db_sql(f'''
            select * from {self.index_advise}('');''')
        self.logger.info(index_advise)
        str1 = 'ERROR:  you must enter a query statement.'
        self.assertIn(str1, index_advise, "执行失败" + step)

        step = 'step13:多条创建索引语句进行查询索引推荐' \
               'expect:报错提示无法为多个查询提供建议'
        self.logger.info(step)
        index_advise = self.primary_sh.execut_db_sql(f'''
            select * from {self.index_advise}('select {self.table1}.col_int,
            {self.table1}.col_numeric,{self.table2}.col_money from 
            {self.table1} inner join {self.table2} on {self.table1}.col_int =
            {self.table2}.col_int where {self.table1}.col_time=''19:41:20'' 
            order by {self.table1}.col_int desc limit 20;
            select * from {self.table1};');''')
        self.logger.info(index_advise)
        str1 = 'ERROR:  can not advise for multiple queries.'
        self.assertIn(str1, index_advise, "执行失败" + step)

    def tearDown(self):
        step = 'step14:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_enviroment = self.primary_sh.execut_db_sql(f'''
            drop view {self.view};
            drop table {self.table1};
            drop table {self.table2};
            drop procedure {self.procedure1};
            drop procedure {self.procedure2};''')
        self.logger.info(clean_enviroment)
        self.assertEqual(clean_enviroment.count(self.Con.TABLE_DROP_SUCCESS),
                         2, "执行失败" + step)
        self.assertIn(self.Con.DROP_VIEW_SUCCESS_MSG, clean_enviroment,
                      "执行失败" + step)
        self.assertIn(self.Con.DROP_PROCEDURE_SUCCESS_MSG, clean_enviroment,
                      "执行失败" + step)
        self.assertEqual(clean_enviroment.count('DROP PROCEDURE'), 2,
                         "执行失败" + step)
        self.logger.info('Opengauss_Function_Ai_Indexadv_Case0015 finish')

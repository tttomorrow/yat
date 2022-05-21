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
Case Type   : 智能运维model模块
Case Name   : 创建model,from指定不同数据库对象
Description :
    1.创建表1并插入数据
    2.创建表2并插入数据
    3.创建model,from指定分区表
    4.创建model,from指定全局临时表
    5.创建model,from指定表达式
    6.创建视图
    7.创建model,from指定视图
    8.查询系统表
    9.查询视图数据数量
    10.预测表1数据
    11.预测表2数据
    12.清理环境
Expect      :
    1.创建表1并插入数据成功
    2.创建表2并插入数据成功
    3.创建model,from指定分区表成功
    4.创建model,from指定全局临时表成功
    5.创建model,from指定表达式成功
    6.创建视图成功
    7.创建model,from指定视图成功
    8.返回创建model的modelname值
    9.返回视图数据数量
    10.返回预测的表1数据
    11.返回预测的表2数据
    12.清理环境成功
History     :
"""

import os
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
        self.table = 't_model_tab1_0029'
        self.table1 = 't_model_tab2_0029'
        self.table2 = 'gs_model_warehouse'
        self.view = 'v_model_view_0029'
        self.model1 = 'm_model_partition_tab_0029'
        self.model2 = 'm_model_expression_0029'
        self.model3 = 'm_model_view_0029'

    def test_ai(self):
        self.logger.info(f'{os.path.basename(__file__)[:-3]}' + ' start')
        step = 'step1;创建表1并插入数据 expect:创建表1并插入数据成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(
            f'''drop table if exists {self.table} cascade;
                create table {self.table}(co1 int,co2 char(10),co3 char(10),
                co4 char(10),cost int,service int)
                partition by range(co1)
                (
                    partition p1 values less than (10),
                    partition p2 values less than (20),
                    partition p3 values less than (30)
                );
                insert into {self.table} values (generate_series(1,8),
                'column02','column03', 'column04',1000,5);
                insert into {self.table} values (generate_series(1,18),
                'column01','column02','column03',2500,5);
                insert into {self.table} values (generate_series(15,20),
                'column03','column02','column03',80,6);
                insert into {self.table} values (generate_series(10,15),
                'column04','column02','column03',1800,5);''')
        self.logger.info(create_table)
        self.assertTrue(self.Con.TABLE_CREATE_SUCCESS in create_table
                        and self.Con.INSERT_SUCCESS_MSG in create_table
                        and create_table.count('INSERT') == 4,
                        "建表并插入数据失败" + step)

        step = 'step2:创建表2并插入数据 expect:创建表2并插入数据成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(
            f'''drop table if exists {self.table1} cascade;
                create table {self.table1}(id integer not null,second_attack 
                integer , treatment integer ,trait_anxiety integer );
                insert into {self.table1} values (1,1,1, 70),(2,1,1,80),
                (3,1,1,50),(4,1,0, 60),(5,1,0,40),(6,1,0,65),(7,1,0,75),
                (8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),
                (13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),
                (18,0,0,45),(19,0,0,50),(20,0,0,60);''')
        self.logger.info(create_table)
        self.assertTrue(self.Con.TABLE_CREATE_SUCCESS in create_table
                        and self.Con.INSERT_SUCCESS_MSG in create_table,
                        "建表并插入数据失败" + step)

        step = 'step3:创建model,from指定分区表 expect:创建成功'
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model1} using logistic_regression 
                features co1,cost target service from {self.table};''')
        self.logger.info(create_model)
        self.assertIn('MODEL CREATED. PROCESSED 1', create_model,
                      "执行失败" + step)

        step = 'step4:创建model,from指定全局临时表 expect:创建成功'
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model2} using logistic_regression 
                features treatment,trait_anxiety target second_attack 
                from {self.table1};''')
        self.logger.info(create_model)
        self.assertIn('MODEL CREATED. PROCESSED 1', create_model,
                      "执行失败" + step)

        step = 'step5:创建model,from指定表达式 expect:创建成功'
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model3} using logistic_regression 
                features treatment,trait_anxiety target second_attack 
                from (select treatment,trait_anxiety,second_attack from 
                {self.table1});''')
        self.logger.info(create_model)
        self.assertIn('MODEL CREATED. PROCESSED 1', create_model,
                      "执行失败" + step)

        step = 'step6:创建视图 expect:创建成功'
        create_view = self.primary_sh.execut_db_sql(
            f'''drop view if exists {self.view};
                create view {self.view} as select * from {self.table1};''')
        self.logger.info(create_view)
        self.assertIn('CREATE VIEW', create_view, "执行失败" + step)

        step = 'step7:创建model,from指定视图 expect:创建成功'
        create_model = self.primary_sh.execut_db_sql(
            f'''drop model {self.model3};
                create model {self.model3} using logistic_regression 
                features treatment,trait_anxiety target second_attack 
                from {self.view};''')
        self.logger.info(create_model)
        self.assertIn('MODEL CREATED. PROCESSED 1', create_model,
                      "执行失败" + step)

        step = 'step8:查找系统表 expect:返回新建model的modelname值'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select modelname from {self.table2};''')
        self.logger.info(select_model)
        self.assertIn(f'{self.model1}', select_model,
                      "执行失败" + step)
        self.assertIn(f'{self.model2}', select_model,
                      "执行失败" + step)
        self.assertIn(f'{self.model3}', select_model,
                      "执行失败" + step)

        step = 'step9:查询视图数据数量 expect:返回视图数据数量'
        self.logger.info(step)
        select_view = self.primary_sh.execut_db_sql(
            f'''select count(*) from {self.view};''')
        self.logger.info(select_view)
        self.assertIn('(1 row)', select_view, "执行失败" + step)

        step = 'step10:预测表1数据;expect:返回预测的表1数据'
        self.logger.info(step)
        predict_data = self.primary_sh.execut_db_sql(
            f'''select predict by {self.model1}(features co1,cost) 
                from {self.table};''')
        self.logger.info(predict_data)
        self.assertNotIn('(0 row)', predict_data, "执行失败" + step)

        step = 'step11:预测表1数据;expect:返回预测的表1数据'
        self.logger.info(step)
        predict_data = self.primary_sh.execut_db_sql(
            f'''select predict by {self.model2}(features treatment,
                trait_anxiety) from {self.table1};''')
        self.logger.info(predict_data)
        self.assertNotIn('(0 row)', predict_data, "执行失败" + step)

    def tearDown(self):
        step = 'step12:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(f'''
            drop view {self.view};
            drop table {self.table};
            drop table {self.table1};
            drop model {self.model1};
            drop model {self.model2};
            drop model {self.model3};''')
        self.logger.info(clean_environment)
        self.assertTrue(self.Con.TABLE_DROP_SUCCESS in clean_environment
                        and clean_environment.count('DROP TABLE') == 2,
                        '执行失败' + step)
        self.assertTrue('DROP MODEL' in clean_environment
                        and clean_environment.count('DROP MODEL') == 3,
                        "执行失败" + step)
        self.assertIn(self.Con.DROP_VIEW_SUCCESS_MSG, clean_environment,
                      "执行失败" + step)
        self.logger.info(f'{os.path.basename(__file__)[:-3]}' + ' finish')

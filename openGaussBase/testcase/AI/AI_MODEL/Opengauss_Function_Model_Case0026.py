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
Case Name   : 创建model,from指定物化视图
Description :
    1.建表并插入数据
    2.创建物化视图
    3.查找视图中数据的数量
    4.创建model,from指定物化视图
    5.查找系统表
    6.预测表数据
    7.清理环境
Expect      :
    1.建表并插入数据成功
    2.创建物化视图成功
    3.返回视图中数据的数量
    4.创建model,from指定物化视图成功
    5.返回创建model的modelname值
    6.返回预测的表数据
    7.清理环境成功
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
        self.table = 't_model_tab_0026'
        self.table1 = 'gs_model_warehouse'
        self.view = 'v_model_view_0026'
        self.model = 'm_model_materialized_view_0026'

    def test_ai(self):
        self.logger.info(f'{os.path.basename(__file__)[:-3]}' + ' start')
        step = 'step1;建表并插入数据 expect:建表并插入数据成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(
            f'''drop table if exists {self.table} cascade;
                create table  {self.table}(id integer not null,second_attack 
                integer ,treatment integer ,trait_anxiety integer );
                insert into {self.table} values (1,1,1, 70),(2,1,1,80),
                (3,1,1,50),(4,1,0, 60),(5,1,0,40),(6,1,0,65),(7,1,0,75),
                (8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),
                (13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),
                (18,0,0,45),(19,0,0,50),(20,0,0,60);''')
        self.logger.info(create_table)
        self.assertTrue(self.Con.TABLE_CREATE_SUCCESS in create_table
                        and self.Con.INSERT_SUCCESS_MSG in create_table,
                        "建表并插入数据失败" + step)

        step = 'step2:创建物化视图 expect:创建成功'
        self.logger.info(step)
        create_view = self.primary_sh.execut_db_sql(
            f'''drop materialized view if exists {self.view};
                create materialized view {self.view} as select * from 
                {self.table};''')
        self.logger.info(create_view)
        self.assertIn('CREATE MATERIALIZED VIEW', create_view,
                      "执行失败" + step)

        step = 'step3:查找视图中数据的数量' \
               'expect:返回视图中数据的数量'
        self.logger.info(step)
        select_view = self.primary_sh.execut_db_sql(
            f'''select count(*) from {self.view};''')
        self.logger.info(select_view)
        self.assertIn('(1 row)', select_view, "执行失败" + step)

        step = 'step4:创建model,from指定物化视图 expect:创建成功'
        self.logger.info(step)
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model} using logistic_regression features 
                treatment,trait_anxiety target second_attack from 
                {self.table};''')
        self.logger.info(create_model)
        self.assertIn('MODEL CREATED. PROCESSED 1', create_model,
                      "执行失败" + step)

        step = 'step5:查找系统表 expect:返回新建model的modelname值'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select modelname from {self.table1};''')
        self.logger.info(select_model)
        self.assertIn(f'{self.model}', select_model,
                      "执行失败" + step)

        step = 'step6:预测表数据;expect:返回预测的表数据'
        self.logger.info(step)
        predict_data = self.primary_sh.execut_db_sql(
            f'''select predict by {self.model}(features treatment,
                trait_anxiety) from {self.table};''')
        self.logger.info(predict_data)
        self.assertNotIn('(0 row)', predict_data, "执行失败" + step)

    def tearDown(self):
        step = 'step7:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(f'''
            drop materialized view {self.view};
            drop table {self.table};
            drop model {self.model};''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.TABLE_DROP_SUCCESS, clean_environment,
                      '执行失败' + step)
        self.assertIn('DROP MODEL', clean_environment, "执行失败" + step)
        self.assertIn('DROP MATERIALIZED VIEW', clean_environment,
                      "执行失败" + step)
        self.logger.info(f'{os.path.basename(__file__)[:-3]}' + ' finish')

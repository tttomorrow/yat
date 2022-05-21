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
Case Type   : 智能运维模块model
Case Name   : 创建model，from指定外表
Description :
    1.加载postgres_fdw
    2.创建外部服务器
    3.创建用户映射
    4.创建并切换schema,在新建schema下创建表并插入数据
    5.切换schema为public,创建外表
    6.创建model
    7.查询系统表
    8.清理环境
Expect      :
    1.加载postgres_fdw成功
    2.创建外部服务器成功
    3.创建用户映射成功
    4.创建并切换schema,在新建schema下创建表并插入数据成功
    5.切换schema为public成功,创建外表成功
    6.创建model成功
    7.返回新建model的modelname值
    8.清理环境成功
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
        self.extension = 'postgres_fdw'
        self.server = 's_server_loopback'
        self.schema = 's_schema_fdw_test'
        self.table1 = 't_model_tab_0028'
        self.table2 = 't_model_foreign_tab_0028'
        self.model = 'm_model_foreign_0028'

    def test_explain(self):
        self.logger.info(f'{os.path.basename(__file__)[:-3]}' + ' start')
        step = 'step1:加载postgres_fdw;expect:加载postgres_fdw成功'
        self.logger.info(step)
        loading_extension = self.primary_sh.execut_db_sql(
            f'''drop extension if exists {self.extension} cascade;
            create extension {self.extension};''')
        self.logger.info(loading_extension)
        self.assertIn('CREATE EXTENSION', loading_extension,
                      "加载postgres_fdw失败" + step)

        step = 'step2:创建外部服务器;expect:创建外部服务器成功'
        self.logger.info(step)
        create_server = self.primary_sh.execut_db_sql(
            f'''drop server if exists {self.server} cascade;
            create server {self.server} foreign data wrapper {self.extension} 
            options (dbname '{self.dbuserNode.db_name}', 
            port '{self.dbuserNode.db_port}');''')
        self.logger.info(create_server)
        self.assertIn('CREATE SERVER', create_server, "执行失败" + step)

        step = 'step3:创建用户映射;expect:创建用户映射成功'
        self.logger.info(step)
        create_user_mapping = self.primary_sh.execut_db_sql(
            f'''create user mapping for current_user server {self.server};''')
        self.logger.info(create_user_mapping)
        self.assertIn('CREATE USER MAPPING', create_user_mapping,
                      "执行失败" + step)

        step = 'step4:创建并切换schema,在新建schema下创建表并插入数据;' \
               'expect:创建并切换schema,在新建schema下创建表并插入数据成功'
        self.logger.info(step)
        create_schema_table = self.primary_sh.execut_db_sql(
            f'''drop schema if exists {self.schema};
            create schema {self.schema};
            set current_schema={self.schema};
            drop table if exists {self.table1};
            create table {self.table1}(id integer not null,second_attack 
            integer,treatment integer ,trait_anxiety integer );
            insert into {self.table1} values (1,1,1,70),(2,1,1,80),(3,1,1,50),
            (4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),(8,1,0,80),
            (9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),(13,0,1,45),
            (14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),(18,0,0,45),
            (19,0,0,50),(20,0,0,60);''')
        self.logger.info(create_schema_table)
        self.assertIn('CREATE SCHEMA', create_schema_table, "执行失败" + step)
        self.assertIn('SET', create_schema_table, "执行失败" + step)
        self.assertTrue(self.Con.TABLE_CREATE_SUCCESS in create_schema_table
                        and self.Con.INSERT_SUCCESS_MSG in create_schema_table,
                        "执行失败" + step)

        step = 'step5:切换schema为public成功,创建外表;' \
               'expect:切换schema为public成功,创建外表成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(
            f"set current_schema=public;"
            f"drop table if exists {self.table2};"
            f"create foreign  table {self.table2}( id integer not null,"
            f"second_attack "
            f"integer ,treatment integer ,trait_anxiety integer ) "
            f"server {self.server} options (schema_name '{self.schema}',"
            f"table_name '{self.table1}');")
        self.logger.info(create_table)
        self.assertIn('SET', create_table, "执行失败" + step)
        self.assertIn('CREATE FOREIGN TABLE', create_table,
                      "执行失败" + step)

        step = 'step6:创建model;expect:创建model成功'
        self.logger.info(step)
        create_model = self.primary_sh.execut_db_sql(
            f'''
            select * from pg_class where relname = '{self.table1}';
            select * from pg_class where relname = '{self.table2}';
            create model {self.model} using logistic_regression features
            treatment,trait_anxiety target second_attack from {self.table2};
            ''')
        self.logger.info(create_model)
        self.assertIn('MODEL CREATED. PROCESSED 1', create_model,
                      "执行失败" + step)

        step = 'step7:查询系统表;expect:返回新建model的modelname值'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select modelname from gs_model_warehouse;''')
        self.logger.info(select_model)
        self.assertIn(f'{self.model}', select_model, "执行失败" + step)

    def tearDown(self):
        step = 'step8:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(f'''
            drop extension {self.extension} cascade;
            drop schema {self.schema} cascade;
            drop model {self.model};''')
        self.logger.info(clean_environment)
        self.assertIn('DROP EXTENSION', clean_environment, "执行失败" + step)
        self.assertIn('DROP SCHEMA', clean_environment, "执行失败" + step)
        self.assertIn('DROP MODEL', clean_environment, "执行失败" + step)
        self.logger.info(f'{os.path.basename(__file__)[:-3]}' + ' finish')

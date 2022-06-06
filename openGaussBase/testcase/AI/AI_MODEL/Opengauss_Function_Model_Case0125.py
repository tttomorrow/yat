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
Case Name   : 创建mode带正确的超参切换数据库
Description :
    1.创建数据库
    2.在新建数据库中创建表
    3.在新建的表中插入数据
    4.在新建数据库中创建model并在系统表中查找
    5.预测新建数据库中创建的表数据
    6.清理环境
Expect      :
    1.创建数据库成功
    2.在新建数据库中创建表成功
    3.在新建的表中插入数据成功
    4.在新建数据库中创建model成功,返回创建的modelname值
    5.返回新建数据库中创建的表数据
    6.清理环境成功
History     :
"""

import os
import unittest
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class AI(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.Con = Constant()
        self.table = 't_table_model_0125'
        self.model = 'm_model_database_0125'
        self.database = 'd_database_0125'

    def test_ai(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:创建数据库 expect:创建数据库成功'
        self.logger.info(step)
        create_database = self.primary_sh.execut_db_sql(
            f'''drop database if exists {self.database};
                create database {self.database};''')
        self.logger.info(create_database)
        self.assertIn(self.Con.CREATE_DATABASE_SUCCESS, create_database,
                      "执行失败" + step)

        step = 'step2:在新建数据库中创建表 expect:在新建数据库中创建表成功'
        self.logger.info(step)
        s1 = f'''drop table if exists {self.table};
            create table {self.table}(id integer not null,second_attack 
            integer,treatment integer,trait_anxiety integer);'''
        create_table = self.primary_sh.execut_db_sql(s1, dbname=self.database)
        self.logger.info(create_table)
        self.assertIn(self.Con.TABLE_CREATE_SUCCESS, create_table,
                      "在新建数据库中创建表失败" + step)

        step = 'step3:在新建的表中插入数据 expect:在新建的表中插入数据成功'
        self.logger.info(step)
        s2 = f'''insert into {self.table} values (1,1,1,70),(2,1,1,80),
            (3,1,1,50),(4,1,0,60),(5,1,0,40),(6,1,0,65),(7,1,0,75),
            (8,1,0,80),(9,1,0,70),(10,1,0,60),(11,0,1,65),(12,0,1,50),
            (13,0,1,45),(14,0,1,35),(15,0,1,40),(16,0,1,50),(17,0,0,55),
            (18,0,0,45),(19,0,0,50),(20,0,0,60);'''
        insert_data = self.primary_sh.execut_db_sql(s2, dbname=self.database)
        self.logger.info(insert_data)
        self.assertIn(self.Con.INSERT_SUCCESS_MSG, insert_data,
                      "在新建数据库中插入数据失败" + step)

        step = 'step4:在新建数据库中创建model并在系统表中查找' \
               'expect:在新建数据库中创建model成功,返回创建的modelname值'
        self.logger.info(step)
        s3 = f'''create model {self.model} using linear_regression features 
            treatment,trait_anxiety target second_attack from {self.table};

            select modelname from gs_model_warehouse; '''
        create_model = self.primary_sh.execut_db_sql(s3, dbname=self.database)
        self.logger.info(create_model)
        self.assertIn('MODEL CREATED. PROCESSED 1', create_model,
                      "执行失败" + step)
        self.assertIn(self.model, create_model, "执行失败" + step)

        step = 'step5:预测新建数据库中创建的表数据 ' \
               'expect:返回新建数据库中创建的表数据'
        self.logger.info(step)
        s4 = f'''select predict by {self.model}(features treatment,
            trait_anxiety) from {self.table};'''
        predict_data = self.primary_sh.execut_db_sql(s4, dbname=self.database)
        self.logger.info(predict_data)
        self.assertNotIn('(0 row)', predict_data, "执行失败" + step)

    def tearDown(self):
        step = 'step6:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(f'''
            drop database {self.database};''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.DROP_DATABASE_SUCCESS, clean_environment,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

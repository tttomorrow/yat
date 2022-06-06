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
Case Name   : linear_regression创建mode,带超参tolerance
Description :
    1.建表并插入数据
    2.linear_regression创建mode,带超参tolerance
    3.查找系统表gs_model_warehouse中新建model1的hyperparametersvalues值
    4.查找系统表gs_model_warehouse中新建model2的hyperparametersvalues值
    5.查询系统表gs_model_warehouse
    6.清理环境
Expect      :
    1.建表并插入数据成功
    2.创建model成功
    3.返回hyperparametersvalues值中含超参tolerance值1
    4.返回hyperparametersvalues值中含超参tolerance值2
    5.返回全部新建model的modelname
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
        self.table = 't_table_model_mot_0112'
        self.model1 = 'm_model_true_tolerance_0112'
        self.model2 = 'm_model_true_tolerance1_0112'

    def test_ai(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表并插入数据 expect:建表并插入数据成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(
            f'''drop table if exists {self.table} cascade;
                create table  {self.table}(id int, tax int,bedroom int,bath 
                float,price int,size int,lot int);
                insert into {self.table} values (1,590 ,2 ,1 ,5000,770 ,22100),
                (2 ,1050 ,3 ,2,85000 ,1410,12000),(3 ,20 ,3,1,22500,1060,500),
                (4 ,870,2 ,2,90000,1300 ,17500),(5,1320,3,2,33000,1500,30000),
                (6,1350,3,100,90500,820,25700),(7,2790,3,2.5,26000,2130,25000),
                (8,680,2,1,142500,1170,22000),(9,1840,3,2,160000,1500,19000), 
                (10,3680,4,2,240000,2790,20000),(11,1660,3,1,87000,1030,17500),
                (12,1620,3,2,11800,1250,20000),(13,3100,3,2,140000,1760,38000)
                ;''')
        self.logger.info(create_table)
        self.assertTrue(self.Con.TABLE_CREATE_SUCCESS in create_table
                        and self.Con.INSERT_SUCCESS_MSG in create_table,
                        "建表并插入数据失败" + step)

        step = 'step2:linear_regression创建mode带超参tolerance' \
               'expect:创建成功'
        self.logger.info(step)
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model1} using linear_regression features 
                1,tax,bath,size target price from {self.table} with 
                tolerance = 100;
                
                create model {self.model2} using linear_regression features 
                1,tax,bath,size target price from {self.table} 
                with tolerance = 1.7976931e+308;''')
        self.logger.info(create_model)
        str1 = 'MODEL CREATED. PROCESSED 1'
        self.assertTrue(str1 in create_model and create_model.count(str1)
                        == 2, "执行失败" + step)

        step = 'step3:查找系统表gs_model_warehouse中新建model1的' \
               'hyperparametersvalues值' \
               'expect:返回hyperparametersvalues值中含超参tolerance值100'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select hyperparametersvalues from gs_model_warehouse 
                where modelname='{self.model1}';''')
        self.logger.info(select_model)
        self.assertEqual(len(select_model.split(',')), 9, "执行失败" + step)
        self.assertIn('100', select_model.split(',')[6], "执行失败" + step)

        step = 'step4:查找系统表gs_model_warehouse中新建model2的' \
               'hyperparametersvalues值' \
               'expect:返回hyperparametersvalues值中含超参tolerance值' \
               '1.7976931e+308'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select hyperparametersvalues from gs_model_warehouse 
                where modelname='{self.model2}';''')
        self.logger.info(select_model)
        self.assertEqual(len(select_model.split(',')), 9, "执行失败" + step)
        self.assertIn('1.7976931e+308', select_model.split(',')[6],
                      "执行失败" + step)

        step = 'step5:查询系统表 expect:返回新建model的modelname值'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select modelname from gs_model_warehouse;''')
        self.logger.info(select_model)
        self.assertIn(self.model1, select_model, "执行失败" + step)
        self.assertIn(self.model2, select_model, "执行失败" + step)

    def tearDown(self):
        step = 'step5:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(f'''
            drop table {self.table};
            drop model {self.model1};
            drop model {self.model2};''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.TABLE_DROP_SUCCESS, clean_environment,
                      "执行失败" + step)
        self.assertEqual(clean_environment.count('DROP MODEL'), 2,
                         "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

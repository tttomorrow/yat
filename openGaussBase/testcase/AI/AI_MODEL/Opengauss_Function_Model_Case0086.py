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
Case Name   : svm创建mode带超参max_iterations最大值,超参max_iterations最小值
Description :
    1.建表并插入数据
    2.svm创建mode带超参max_iterations最大值
    3.svm创建mode带超参max_iterations最小值
    4.查找系统表gs_model_warehouse中新建model的hyperparametersvalues值
    5.查询系统表gs_model_warehouse
    6.清理环境
Expect      :
    1.建表并插入数据成功
    2.创建成功
    3.创建成功
    4.返回系统表gs_model_warehouse中新建model的hyperparametersvalues值
    5.返回新建model的modelname
    6.清理环境成功
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
        self.table = 't_table_model_mot_0086'
        self.model1 = 'm_model_max_max_iterations_0086'
        self.model2 = 'm_model_min_max_iterations_0086'

    def test_explain(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表并插入数据 expect:建表并插入数据成功'
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

        step = 'step2:svm创建mode带超参max_iterations最大值' \
               'expect:创建成功'
        self.logger.info(step)
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model1} using  svm_classification
                features treatment,trait_anxiety target second_attack from 
                {self.table} with max_iterations =10000;''')
        self.logger.info(create_model)
        self.assertIn('MODEL CREATED. PROCESSED 1', create_model,
                      "执行失败" + step)

        step = 'step3:svm创建mode带超参max_iterations最小值 expect:创建成功'
        self.logger.info(step)
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model2} using  svm_classification
                features treatment,trait_anxiety target second_attack from 
                {self.table} with max_iterations =1;''')
        self.logger.info(create_model)
        self.assertIn('MODEL CREATED. PROCESSED 1', create_model,
                      "执行失败" + step)

        step = 'step4:查找系统表gs_model_warehouse中新建model的' \
               'hyperparametersvalues值 ' \
               'expect:返回系统表gs_model_warehouse中新建model的' \
               'hyperparametersvalues值'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select hyperparametersvalues from gs_model_warehouse 
                where modelname='{self.model1}';

                select hyperparametersvalues from gs_model_warehouse 
                where modelname='{self.model2}';''')
        self.logger.info(select_model)
        self.assertIn('10000', select_model, "执行失败" + step)
        self.assertIn('1', select_model, "执行失败" + step)

        step = 'step5:查询系统表 expect:返回新建model的modelname值'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select modelname from gs_model_warehouse;''')
        self.logger.info(select_model)
        self.assertIn(f'{self.model1}', select_model, "执行失败" + step)
        self.assertIn(f'{self.model2}', select_model, "执行失败" + step)

    def tearDown(self):
        step = 'step6:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(f'''
            drop table {self.table};
            drop model {self.model1};
            drop model {self.model2};
            alter system set enable_incremental_checkpoint to on;''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.TABLE_DROP_SUCCESS, clean_environment,
                      "执行失败" + step)
        self.assertEqual(clean_environment.count('DROP MODEL'), 2,
                         "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

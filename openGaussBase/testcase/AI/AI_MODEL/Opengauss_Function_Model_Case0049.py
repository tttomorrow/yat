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
Case Name   : 创建model,from指定不同对象
Description :
    1.创建model,from直接传入数据
    2.创建model,from直接传入多个array数组
    3.创建model,from直接传入一个array数组
    4.查询系统表
    5.修改参数enable_incremental_checkpoint为off并重启数据库
    6.查看参数enable_incremental_checkpoint
    7.创建mot表并插入数据
    8.创建model
    9.查询系统表
    10.预测mot表数据
    11.清理环境
Expect      :
    1.创建失败,报错提示数据不是浮点8（双精度）数组类型
    2.创建失败，报错提示不能同时指定多个数组
    3.创建成功
    4.返回新建model的modelname值
    5.修改参数成功
    6.返回参数enable_incremental_checkpoint值为off
    7.建mot表并插入数据成功
    8.创建model成功
    9.返回新建model的modelname值
    10.返回预测的mot表数据
    11.清理环境成功
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
        self.table = 't_table_model_mot_0049'
        self.model1 = 'm_model_data_0049'
        self.model2 = 'm_model_multi_array_0049'
        self.model3 = 'm_model_array_0049'
        self.model4 = 'm_model_mot_tab_0049'

    def test_ai(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:创建model,from直接传入数据' \
               'expect:创建失败,报错提示数据不是浮点8（双精度）数组类型'
        self.logger.info(step)
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model1} using kmeans from 
                (select  -67.9280164728999978,-3.90913184339999997,\
                with max_iterations = 49, num_centroids = 10,\
                tolerance = 0.00001, batch_size = 1000, num_features = 7, \
                distance_function = 'L1',seeding_function = 'Random++', \
                verbose = 1, seed = 1254925990;''')
        s = 'k-means exec: data is not of type float8 (double precision) array'
        self.logger.info(create_model)
        self.assertIn(s, create_model, '执行失败:' + step)

        step = 'step2:创建model,from直接传入多个array数组' \
               'expect:创建失败，报错提示不能同时指定多个数组'
        self.logger.info(step)
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model2} using kmeans from 
                (select array[135.529122074100002,1.38498608310000003,\
                75.1363694922999991,-157.490917820600004,-23.7378253056999995,\
                33.6490592628000016,-7.9599672791999998]::double \
                precision[],array[-73.1345967305999949,\
                ,173.55455376110001,138.308886012699986,\
                -37.5366639877000026]::double precision[]) \
                with max_iterations = 49, num_centroids = 10,\
                tolerance = 0.00001, batch_size = 1000, num_features = 7, 
                distance_function = 'L1',seeding_function = 'Random++', 
                verbose = 1, seed = 1254925990;''')
        s = 'k-means exec: relation should contain only a single attribute'
        self.logger.info(create_model)
        self.assertIn(s, create_model, '执行失败:' + step)

        step = 'step3:创建model,from直接传入一个array数组' \
               'expect:创建成功'
        self.logger.info(step)
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model3} using kmeans from\
                (select array[135.529122074100002,1.38498608310000003,\
                75.1363694922999991,-157.490917820600004,\
                -23.7378253056999995,33.6490592628000016,\
                -7.9599672791999998]::double precision[]) \
                with max_iterations = 49, num_centroids = 10,\
                tolerance = 0.00001, batch_size = 1000, num_features = 7, \
                distance_function = 'L1',seeding_function = 'Random++', \
                verbose = 1, seed = 1254925990;''')
        s = 'MODEL CREATED. PROCESSED 1'
        self.logger.info(create_model)
        self.assertIn(s, create_model, '执行失败:' + step)

        step = 'step4:查询系统表 expect:返回新建model的modelname值'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select modelname from gs_model_warehouse;''')
        s = 'm_model_array_0049'
        self.logger.info(select_model)
        self.assertIn(s, select_model, '执行失败:' + step)

        step = 'step5:修改参数enable_incremental_checkpoint为off并重启数据库' \
               'expect:修改成功'
        self.logger.info(step)
        modify_param = self.primary_sh.execut_db_sql(
            f'''alter system set enable_incremental_checkpoint to off;''')
        msg = self.primary_sh.restart_db_cluster()
        self.logger.info(msg)
        self.assertTrue(msg, '执行失败' + step)
        s = 'ALTER SYSTEM SET'
        self.logger.info(modify_param)
        self.assertIn(s, modify_param, '执行失败:' + step)

        step = 'step6:查看参数enable_incremental_checkpoint expect:' \
               'enable_incremental_checkpoint为off'
        self.logger.info(step)
        show_para = self.primary_sh.execut_db_sql(f'''
            show enable_incremental_checkpoint;''')
        self.logger.info(show_para)
        self.assertIn('off', show_para, "修改参数失败" + step)

        step = 'step7:创建mot表并插入数据 expect:创建mot表并插入数据成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop foreign table if exists {self.table};
            create foreign table {self.table}(id integer not null,\
            second_attack integer,treatment integer,trait_anxiety integer);
            insert into  {self.table} values (1,  1, 1, 70),(2,  1, 1, 80),
            (3,  1, 1, 49),(4,  1, 0, 60),(5,  1, 0, 40),(6,  1, 0, 65),
            (7,  1, 0, 75),(8,  1, 0, 80),(9,  1, 0, 70),
            (10, 1, 0, 60),(11, 0, 1, 65),(12, 0, 1, 49),(13, 0, 1, 45),
            (14, 0, 1, 35),(15, 0, 1, 40),(16, 0, 1, 49),(17, 0, 0, 55),
            (18, 0, 0, 45),(19, 0, 0, 49),(20, 0, 0, 60);''')
        self.logger.info(create_table)
        self.assertTrue(self.Con.CREATE_FOREIGN_SUCCESS_MSG in create_table
                        and self.Con.DROP_FOREIGN_SUCCESS_MSG in create_table,
                        "创建mot表并插入数据失败" + step)

        step = 'step8:创建model expect:创建model成功'
        self.logger.info(step)
        create_model = self.primary_sh.execut_db_sql(
            f'''create model {self.model4} using logistic_regression \
                features treatment,trait_anxiety target second_attack \
                from {self.table};''')
        s = 'MODEL CREATED. PROCESSED 1'
        self.logger.info(create_model)
        self.assertIn(s, create_model, '执行失败:' + step)

        step = 'step9:查询系统表 expect:返回新建model的modelname值'
        self.logger.info(step)
        select_model = self.primary_sh.execut_db_sql(
            f'''select modelname from gs_model_warehouse;''')
        s = 'm_model_mot_tab_0049'
        self.logger.info(select_model)
        self.assertIn(s, select_model, '执行失败:' + step)

        step = 'step10:预测mot表数据 expect:返回预测的mot表数据'
        self.logger.info(step)
        predict_data = self.primary_sh.execut_db_sql(
            f'''select predict by {self.model4} (features treatment,\
            trait_anxiety) from {self.table};''')
        self.logger.info(predict_data)
        self.assertIn('(20 rows)', predict_data,
                      "预测mot表数据失败" + step)

    def tearDown(self):
        step = 'step11:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(f'''
            drop foreign table {self.table};
            drop model {self.model3};
            drop model {self.model4};
            alter system set enable_incremental_checkpoint to on;''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.DROP_FOREIGN_SUCCESS_MSG, clean_environment,
                      "执行失败" + step)
        self.assertEqual(clean_environment.count('DROP MODEL'), 2,
                         "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

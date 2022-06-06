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
Case Type   : 智能运维snapshot模块
Case Name   : 创建CSS模式的db4ai-snapshot
Description :
    1.修改参数db4ai_snapshot_mode为CSS
    2.查看参数db4ai_snapshot_mode
    3.建表并插入数据
    4.创建快照1
    5.修改并向表插入数据
    6.创建快照2
    7.查看当前数据表快照
    8.清理环境
Expect      :
    1.修改参数db4ai_snapshot_mode为CSS成功
    2.返回参数db4ai_snapshot_mode为CSS
    3.建表并插入数据成功
    4.创建快照1成功
    5.修改并向表插入数据成功
    6.创建快照2成功
    7.返回前数据表快照
    8.清理环境成功
History     :
"""

import os
import unittest
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
        self.table = 't_snapshot_tab_0001'
        self.snapshot1 = 's_snapshot_s1@1.0'
        self.snapshot2 = 's_snapshot_s1@2.0'

    def test_ai_snapshot(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:修改参数db4ai_snapshot_mode为CSS' \
               'expect:修改参数db4ai_snapshot_mode为CSS成功'
        self.logger.info(step)
        self.parm = self.common.show_param('db4ai_snapshot_mode')
        if 'CSS' not in self.parm:
            modify_param = self.primary_sh.execute_gsguc("reload",
                                                         f'''{self.Con.
                                                         GSGUC_SUCCESS_MSG}''',
                                                         f"db4ai_snapshot_"
                                                         f"mode = 'CSS'")
            self.logger.info(modify_param)
            self.assertTrue(modify_param, "执行失败" + step)

        step = 'step2:查看参数db4ai_snapshot_mode' \
               ' expect:返回参数db4ai_snapshot_mode为CSS'
        self.logger.info(step)
        show_para = self.common.show_param(
            'db4ai_snapshot_mode')
        self.logger.info(show_para)
        self.assertIn('CSS', show_para,
                      "修改参数db4ai_snapshot_mode为CSS失败" + step)

        step = 'step3:建表并插入数据 expect:建表并插入数据成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(
            f'''drop table if exists {self.table};
                create table  {self.table}(id int,name varchar);
                insert into {self.table} values (1,'zhangsan'),(2,'lisi'),
                (3,'wangwu'),(4,'lisa'),(5,'jack');''')
        self.logger.info(create_table)
        self.assertTrue(self.Con.TABLE_CREATE_SUCCESS in create_table
                        and self.Con.INSERT_SUCCESS_MSG in create_table,
                        "建表并插入数据失败" + step)

        step = 'step4:创建快照1 expect:创建快照1成功'
        self.logger.info(step)
        create_snapshot = self.primary_sh.execut_db_sql(
            f'''create snapshot {self.snapshot1} comment is 'first version'
                as select * from {self.table};''')
        self.logger.info(create_snapshot)
        self.assertIn(self.snapshot1, create_snapshot, "执行失败" + step)

        step = 'step5:修改并向表插入数据 expect:修改并向表插入数据成功'
        self.logger.info(step)
        modify_table = self.primary_sh.execut_db_sql(
            f'''update {self.table} set name = 'tom' where id = 4;
                insert into {self.table} values (6,'john');
                insert into {self.table} values (7,'tim');''')
        self.logger.info(modify_table)
        self.assertIn(self.Con.UPDATE_SUCCESS_MSG, modify_table,
                      "执行失败" + step)
        self.assertIn(self.Con.INSERT_SUCCESS_MSG, modify_table,
                      "执行失败" + step)
        self.assertEqual(modify_table.count(self.Con.INSERT_SUCCESS_MSG), 2,
                         "执行失败" + step)

        step = 'step6:创建快照2 expect:创建快照2成功'
        self.logger.info(step)
        create_snapshot = self.primary_sh.execut_db_sql(
            f'''create snapshot {self.snapshot2} from @1.0 comment is 
                'inherits from @1.0' using (insert values(6,'john'), 
                (7,'tim');delete where id = 1);''')
        self.logger.info(create_snapshot)
        self.assertIn(self.snapshot2, create_snapshot, "执行失败" + step)

        step = 'step7:查看当前数据表快照;expect:返回查看当前数据表快照'
        self.logger.info(step)
        select_snapshot = self.primary_sh.execut_db_sql(
            f'''select * from db4ai.snapshot;''')
        self.logger.info(select_snapshot)
        self.assertIn(self.snapshot2, select_snapshot, "执行失败" + step)
        self.assertIn(self.snapshot1, select_snapshot, "执行失败" + step)

    def tearDown(self):
        step = 'step8:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(f'''
            drop table {self.table};
            purge snapshot {self.snapshot2};
            purge snapshot {self.snapshot1};''')
        self.logger.info(clean_environment)
        self.parm1 = self.common.show_param('db4ai_snapshot_mode')
        if self.parm not in self.parm1:
            modify_param = self.primary_sh.execute_gsguc("reload",
                                                         f'''{self.Con.
                                                         GSGUC_SUCCESS_MSG}''',
                                                         f"db4ai_snapshot_"
                                                         f"mode = "
                                                         f"'{self.parm}'")
            self.logger.info(modify_param)
            self.assertTrue(modify_param, "执行失败" + step)
        self.assertIn(self.Con.TABLE_DROP_SUCCESS, clean_environment,
                      "执行失败" + step)
        self.assertIn(f'public | {self.snapshot1}', clean_environment,
                      "执行失败" + step)
        self.assertIn(f'public | {self.snapshot2}', clean_environment,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

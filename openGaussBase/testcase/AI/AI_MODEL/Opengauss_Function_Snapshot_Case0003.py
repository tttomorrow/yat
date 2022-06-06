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
Case Name   : create snapshot ...as,create snapshot ...from创建快照
Description :
    1.建表并插入数据
    2.create snapshot ...as创建快照1
    3.查询数据表快照1
    4.修改表数据
    5.查询表数据
    6.查询数据表快照1
    7.创建快照2
    8.查询数据表快照2
    9.create snapshot ...from创建快照3
    10.查询数据表快照3
    11.对已经创建好的数据表快照3进行继承
    12.查询数据表继承的快照数据
    13.从继承的快照中抽取数据,使用0.5抽样率
    14.发布数据表继承的快照
    15.存档数据表继承的快照
    16.查看当前数据表快照
    17.清理环境
Expect      :
    1.建表并插入数据成功
    2.create snapshot ...as创建快照1成功
    3.返回数据表快照1数据
    4.修改表数据成功
    5.返回表数据
    6.返回数据表快照1数据
    7.创建快照2成功
    8.返回数据表快照2数据
    9.create snapshot ...from创建快照3成功
    10.返回数据表快照3数据
    11.对已经创建好的数据表快照3进行继承成功
    12.返回数据表继承的快照数据
    13.抽取成功
    14.发布数据表继承的快照成功
    15.存档数据表继承的快照成功
    16.返回当前数据表快照
    17.清理环境成功
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
        self.table = 't_snapshot_tab_0003'
        self.snapshot1 = 's_snapshot_s1@1.0'
        self.snapshot2 = 's_snapshot_s1@2.0'
        self.snapshot3 = 's_snapshot_inheriting@1.0'
        self.snapshot4 = 's_snapshot_inheriting@2.0'
        self.snapshot5 = 's_snapshot_inheritingnick@2.0'

    def test_ai_snapshot(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表并插入数据 expect:建表并插入数据成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(
            f'''drop table if exists {self.table};
            create table {self.table}(id int,name varchar);
            insert into {self.table} values (1,'zhangsan'),(2,'lisi'),
            (3,'wangwu'),(4,'lisa'),(5,'jack');''')
        self.logger.info(create_table)
        self.assertTrue(self.Con.TABLE_CREATE_SUCCESS in create_table
                        and self.Con.INSERT_SUCCESS_MSG in create_table,
                        "建表并插入数据失败" + step)

        step = 'step2:create snapshot ...as创建快照1' \
               ' expect:create snapshot ...as创建快照1成功'
        self.logger.info(step)
        create_snapshot = self.primary_sh.execut_db_sql(
            f'''create snapshot {self.snapshot1} as select * from {self.table};
            ''')
        self.logger.info(create_snapshot)
        self.assertIn(self.snapshot1, create_snapshot, "执行失败" + step)

        step = 'step3:查询数据表快照1 expect:返回数据表快照1数据'
        self.logger.info(step)
        select_snapshot = self.primary_sh.execut_db_sql(
            f'''select * from public.{self.snapshot1};''')
        self.logger.info(select_snapshot)
        self.assertIn('(5 rows)', select_snapshot, "执行失败" + step)

        step = 'step4:修改表数据 expect:修改表数据成功'
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

        step = 'step5:查询表数据 expect:返回表数据'
        self.logger.info(step)
        select_table = self.primary_sh.execut_db_sql(
            f'''select * from {self.table};''')
        self.logger.info(select_table)
        self.assertIn('tom', select_table, "执行失败" + step)
        self.assertIn('john', select_table, "执行失败" + step)
        self.assertIn('tim', select_table, "执行失败" + step)

        step = 'step6:查询数据表快照1 expect:返回数据表快照1数据'
        self.logger.info(step)
        select_snapshot = self.primary_sh.execut_db_sql(
            f'''select * from public.{self.snapshot1};''')
        self.logger.info(select_snapshot)
        self.assertNotIn('tom', select_snapshot, "执行失败" + step)
        self.assertNotIn('john', select_snapshot, "执行失败" + step)
        self.assertNotIn('tim', select_snapshot, "执行失败" + step)

        step = 'step7:创建快照2;expect:创建快照2成功'
        self.logger.info(step)
        create_snapshot = self.primary_sh.execut_db_sql(
            f'''create snapshot {self.snapshot2} as select * from {self.table};
            ''')
        self.logger.info(create_snapshot)
        self.assertIn(self.snapshot2, create_snapshot, "执行失败" + step)

        step = 'step8:查询数据表快照2 expect:返回数据表快照2数据'
        self.logger.info(step)
        select_snapshot = self.primary_sh.execut_db_sql(
            f'''select * from public.{self.snapshot2};''')
        self.logger.info(select_snapshot)
        self.assertIn('tom', select_snapshot, "执行失败" + step)
        self.assertIn('john', select_snapshot, "执行失败" + step)
        self.assertIn('tim', select_snapshot, "执行失败" + step)

        step = 'step9:create snapshot ...from创建快照3' \
               'expect:create snapshot ...from创建快照3成功'
        self.logger.info(step)
        create_snapshot = self.primary_sh.execut_db_sql(
            f'''create snapshot {self.snapshot3} comment is 'first version' 
            as select * from {self.table};''')
        self.logger.info(create_snapshot)
        self.assertIn(self.snapshot3, create_snapshot, "执行失败" + step)

        step = 'step10:查询数据表快照3 expect:返回数据表快照3数据'
        self.logger.info(step)
        select_snapshot = self.primary_sh.execut_db_sql(
            f'''select * from public.{self.snapshot3};''')
        self.logger.info(select_snapshot)
        self.assertIn('tom', select_snapshot, "执行失败" + step)
        self.assertIn('john', select_snapshot, "执行失败" + step)
        self.assertIn('tim', select_snapshot, "执行失败" + step)

        step = 'step11:对已经创建好的数据表快照3进行继承' \
               'expect:对已经创建好的数据表快照3进行继承成功'
        self.logger.info(step)
        create_snapshot = self.primary_sh.execut_db_sql(
            f'''create snapshot {self.snapshot4} from @1.0 comment is 
            'inherits from @1.0' using (insert values(6,'john'),(7,'tim');
            delete where id = 1);''')
        self.logger.info(create_snapshot)
        self.assertIn(self.snapshot4, create_snapshot, "执行失败" + step)

        step = 'step12:查询数据表继承的快照数据 ' \
               'expect:返回数据表继承的快照数据'
        self.logger.info(step)
        select_snapshot = self.primary_sh.execut_db_sql(
            f'''select * from public.{self.snapshot4};''')
        self.logger.info(select_snapshot)
        self.assertIn('tom', select_snapshot, "执行失败" + step)
        self.assertIn('john', select_snapshot, "执行失败" + step)
        self.assertIn('tim', select_snapshot, "执行失败" + step)

        step = 'step13:从继承的快照中抽取数据,使用0.5抽样率' \
               'expect:抽取数据成功'
        self.logger.info(step)
        extracting_data = self.primary_sh.execut_db_sql(
            f'''sample snapshot {self.snapshot4} stratify by name 
            as nick at ratio .5;''')
        self.logger.info(extracting_data)
        self.assertIn(self.snapshot5, extracting_data, "执行失败" + step)

        step = 'step14:发布数据表继承的快照 expect:发布数据表继承的快照成功'
        self.logger.info(step)
        publish_snapshot = self.primary_sh.execut_db_sql(
            f'''publish snapshot {self.snapshot4};''')
        self.logger.info(publish_snapshot)
        self.assertIn(self.snapshot4, publish_snapshot, "执行失败" + step)

        step = 'step15:存档数据表继承的快照 expect:存档数据表继承的快照成功'
        self.logger.info(step)
        archiving_snapshot = self.primary_sh.execut_db_sql(
            f'''archive snapshot {self.snapshot4};''')
        self.logger.info(archiving_snapshot)
        self.assertIn(self.snapshot4, archiving_snapshot, "执行失败" + step)

        step = 'step16:查看当前数据表快照;expect:返回数据表的所有快照'
        self.logger.info(step)
        select_snapshot = self.primary_sh.execut_db_sql(
            f'''select * from db4ai.snapshot;''')
        self.logger.info(select_snapshot)
        self.assertIn(self.snapshot1, select_snapshot, "执行失败" + step)
        self.assertIn(self.snapshot2, select_snapshot, "执行失败" + step)
        self.assertIn(self.snapshot3, select_snapshot, "执行失败" + step)
        self.assertIn(self.snapshot4, select_snapshot, "执行失败" + step)
        self.assertIn(self.snapshot5, select_snapshot, "执行失败" + step)

    def tearDown(self):
        step = 'step17:清理环境 expect:清理环境成功'
        self.logger.info(step)
        clean_environment = self.primary_sh.execut_db_sql(f'''
            purge snapshot {self.snapshot1};
            purge snapshot {self.snapshot2};
            purge snapshot {self.snapshot5};
            purge snapshot {self.snapshot4};
            purge snapshot {self.snapshot3};
            drop table {self.table};''')
        self.logger.info(clean_environment)
        self.assertIn(self.Con.TABLE_DROP_SUCCESS, clean_environment,
                      "执行失败" + step)
        self.assertIn(self.snapshot1, clean_environment, "执行失败" + step)
        self.assertIn(self.snapshot2, clean_environment,
                      "执行失败" + step)
        self.assertIn(self.snapshot3, clean_environment, "执行失败" + step)
        self.assertIn(self.snapshot4, clean_environment, "执行失败" + step)
        self.assertIn(self.snapshot5, clean_environment, "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

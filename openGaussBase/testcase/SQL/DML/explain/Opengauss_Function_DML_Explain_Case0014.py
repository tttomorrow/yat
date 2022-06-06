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
Case Type   : explain
Case Name   : explain结合in子查询使用
Description :
    1.建表1
    2.建表2
    3.向表1中插入数据
    4.向表2中插入数据
    5.explain结合in子查询使用，打印执行信息
    6.清理环境
Expect      :
    1.建表1成功
    2.建表2成功
    3.向表1中插入数据成功
    4.向表2中插入数据成功
    5.打印执行信息
    6.清理环境成功
History     :
"""

import os
import unittest
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class SQL(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.table1 = 'explain_table_in1_0014'
        self.table2 = 'explain_table_in2_0014'
        self.Constant = Constant()

    def test_explain(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表1 expect:建表1成功'
        self.logger.info(step)
        create_table1 = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table1};
            create table {self.table1} (name varchar(10),stu_id integer 
            not null,score int );''')
        self.logger.info(create_table1)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table1,
                      "建表1失败" + step)

        step = 'step2:建表2 expect:建表2成功'
        self.logger.info(step)
        create_table2 = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table2};
            create table {self.table2} (cname varchar(10),cid varchar(5) 
            not null, num int ,sname varchar(10));''')
        self.logger.info(create_table2)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table2,
                      "建表2失败" + step)

        step = 'step3:向表1中插入数据 expect:向表1中插入数据成功'
        self.logger.info(step)
        insert_data1 = self.primary_sh.execut_db_sql(f'''
            insert into {self.table1} values('张三',1,50),('李四',2,55),
            ('王五',3,30); ''')
        self.logger.info(insert_data1)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data1,
                      "向表1中插入数据失败" + step)

        step = 'step4:向表2中插入数据 expect:向表2中插入数据成功'
        self.logger.info(step)
        insert_data2 = self.primary_sh.execut_db_sql(f'''
            insert into {self.table2} values('张三',1,50),('李四',2,55),
            ('王五',3,30);''')
        self.logger.info(insert_data2)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data2,
                      "向表2中插入数据失败" + step)

        step = 'step5:explain结合in子查询使用，打印执行信息' \
               'expect:打印执行信息'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            explain performance select * from {self.table1} 
            where name in (select sname from {self.table2} where num >= 50);
            ''')
        self.logger.info(explain)
        self.assertIn(' Hash Join ', explain,
                      "explain无法结合in子查询使用" + step)

    def tearDown(self):
        step = 'step6:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table1};
            drop table {self.table2};''')
        self.logger.info(de_table)
        self.assertTrue(self.Constant.DROP_TABLE_SUCCESS in de_table
                        and de_table.count('DROP TABLE') == 2,
                        "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

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
Case Name   : explain结合create table as 语句使用后rollback回滚
Description :
    1.建表
    2.向表中插入数据
    3.开启事务,explain结合create table as 语句使用,打印执行信息,在系统表pg_class
      中查询表form2,使用rollback回滚，再次在系统表pg_class查询表form2
    4.清理环境
Expect      :
    1.建表成功
    2.向表中插入数据成功
    3.开启事务成功,成功打印执行信息,返回已存在的所有表中包含由create as语句
      创建的表,回滚成功,返回已存在的所有表中不包含由create as语句创建的表
    4.清理环境成功
History     :
"""

import os
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class SQL(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.primary_sh = CommonSH('PrimaryDbUser')
        self.table1 = 'explain_create_tab_as_rollback1_0025'
        self.table2 = 'explain_create_tab_as_rollback2_0025'
        self.systable = 'pg_class'
        self.Constant = Constant()

    def test_explain(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表 expect:建表成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table1} ;
            create table {self.table1}(name varchar(10),stu_id varchar(5) 
            not null,score int );''')
        self.logger.info(create_table)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table,
                      "建表失败" + step)

        step = 'step2:向表中插入数据 expect:向表中插入数据成功'
        self.logger.info(step)
        insert_data = self.primary_sh.execut_db_sql(f'''
            insert into {self.table1} values('数学','01',50),
            ('语文','02',55);''')
        self.logger.info(insert_data)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data,
                      "向表中插入数据失败" + step)

        step = 'step3:开启事务,explain结合create table as 语句使用,' \
               '打印执行信息' \
               '在系统表pg_class中查询表form2,使用rollback回滚，' \
               '再次在系统表pg_class查询表form2' \
               'expect:开启事务成功,成功打印执行信息,' \
               '返回表form2的信息,回滚成功,' \
               '返回信息为空'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''start transaction;
            explain performance create table {self.table2} as table 
            {self.table1};
            select relname from {self.systable} \
            where relname = '{self.table2}';
            rollback;
            select * from {self.table2};''')
        self.logger.info(explain)
        data_spl = str(explain).split('ROLLBACK')
        form_spl = data_spl[0]
        self.logger.info(form_spl)
        self.assertTrue(f'{self.table2}' in form_spl
                        and f'ERROR:  relation "{self.table2}" '
                        f'does not exist ' in data_spl[1],
                        "explain结合create table as语句使用后rollback回滚失败"
                        + step)

    def tearDown(self):
        self.logger.info('清理环境')
        step = 'step4:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table1};''')
        self.logger.info(de_table)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, de_table,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

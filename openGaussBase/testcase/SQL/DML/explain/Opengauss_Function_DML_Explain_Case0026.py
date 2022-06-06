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
Case Name   : explain结合execute语句使用后rollback回滚
Description :
    1.建表1
    2.向表1中插入数据
    3.建表2
    4.为insert语句创建预备语句,开启事务,explain结合execute语句使用,
      打印执行信息,查询表form2数据,进行rollback回滚后再次查询表form2数据
    5.清理环境
Expect      :
    1.建表1成功
    2.向表1中插入数据成功
    3.建表2成功
    4.创建预备语句成功,开启事务成功,成功打印执行信息,返回由execute语句新增的
      数据，回滚成功，返回数据为空
    5.清理环境成功
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
        self.table1 = 'explain_execute_rollback1_0026'
        self.table2 = 'explain_execute_rollback2_0026'
        self.prepare_statement = 'insert_data'
        self.Constant = Constant()

    def test_explain(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表1 expect:建表1成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table1} ;
            create table {self.table1}(name varchar(10),stu_id varchar(5) 
            not null,score int );''')
        self.logger.info(create_table)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table,
                      "建表1失败" + step)

        step = 'step2:向表1中插入数据 expect:向表1中插入数据成功'
        self.logger.info(step)
        insert_data = self.primary_sh.execut_db_sql(f'''
            insert into {self.table1} values('数学','01',50),
            ('语文','02',55);''')
        self.logger.info(insert_data)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data,
                      "向表1中插入数据失败" + step)

        step = 'step3:建表2 expect:建表2成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table2};
            create table {self.table2} as table {self.table1}''')
        self.logger.info(create_table)
        self.assertIn('INSERT', create_table, "建表2失败" + step)

        step = 'step4:为insert语句创建预备语句,开启事务, ' \
               'explain结合execute语句使用,打印执行信息,' \
               '查询表2数据,进行rollback回滚后再次查询表2数据' \
               'expect:创建预备语句成功.开启事务成功,成功打印执行信息,' \
               '返回由excute语句新增的数据，回滚成功，返回数据为空'
        self.logger.info(step)
        explain = self.primary_sh.execut_db_sql(f'''
            prepare {self.prepare_statement}(varchar(10),varchar(5),int) \
            as insert into {self.table2} values (\\$1,\\$2,\\$3);
            start transaction;    
            explain performance execute {self.prepare_statement}\
            ('英语','03',60);
            select * from {self.table2};
            rollback;
            select * from {self.table2};''')
        self.logger.info(explain)
        explain_spl = str(explain).split('ROLLBACK')
        self.assertTrue(' 英语 | 03     |    60' in explain_spl[0] and
                        ' 英语 | 03     |    60' not in explain_spl[1],
                        'explain结合prepare使用回滚执行结果错误')

    def tearDown(self):
        step = 'step5:清理环境 expect:清理环境成功'
        de_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table1};
            drop table {self.table2};''')
        self.logger.info(de_table)
        self.assertTrue(self.Constant.DROP_TABLE_SUCCESS in de_table
                        and de_table.count('DROP TABLE') == 2,
                        "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

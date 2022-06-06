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
Case Name   : explain结合事务使用
Description :
    1.建表
    2.向表中插入数据
    3.开启事务,explain结合事务使用，打印执行信息
    4.清理环境
Expect      :
    1.建表成功
    2.向表中插入数据成功
    3.开启事务成功,打印执行信息
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
        self.table = 'explain_table_trans_0021'
        self.Constant = Constant()

    def test_explain(self):
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        step = 'step1:建表 expect:建表成功'
        self.logger.info(step)
        create_table = self.primary_sh.execut_db_sql(f'''
            drop table if exists {self.table};
            create table {self.table}(name varchar(10),stu_id 
            integer not null,score int );''')
        self.logger.info(create_table)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, create_table,
                      "建表失败" + step)

        step = 'step2:向表中插入数据 expect:向表中插入数据成功'
        self.logger.info(step)
        insert_data = self.primary_sh.execut_db_sql(f'''
            insert into {self.table} values('张三',1,50),
            ('李四',2,55),('王五',3,30);''')
        self.logger.info(insert_data)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, insert_data,
                      "向表中插入数据失败" + step)

        step = 'step3:开启事务,explain结合事务使用,打印执行信息' \
               'expect:开启事务成功,打印执行信息'
        self.logger.info(step)
        start_trans = self.primary_sh.execut_db_sql(f'''
            start transaction;
            explain performance select * from {self.table};
            commit;''')
        self.logger.info(start_trans)
        self.assertIn(self.Constant.START_TRANSACTION_SUCCESS_MSG, start_trans,
                      "开启事务失败" + step)
        self.assertIn('Output: name, stu_id, score', start_trans,
                      "explain结合事务使用失败" + step)
        self.assertIn('COMMIT', start_trans, "提交事务失败" + step)

    def tearDown(self):
        step = 'step4:清理环境 expect:清理环境成功'
        self.logger.info(step)
        de_table = self.primary_sh.execut_db_sql(f'''
            drop table {self.table};''')
        self.logger.info(de_table)
        self.assertIn(self.Constant.DROP_TABLE_SUCCESS, de_table,
                      "执行失败" + step)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

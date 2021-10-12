"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : 功能测试
Case Name   : interval分区,VACUUM PARTITION
Description :
    1. 创建表,建索引,插入数据
    2. 删除索引后vacuum partition
    3. 删除数据后vacuum partition
Expect      :
    1. 创建成功
    2. vacuum成功
    3. vacuum成功
History     :
"""
import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0080开始')

    def test_copy(self):
        self.log.info('---步骤1 创建interval分区表,建索引插入数据---')
        cmd0 = '''drop table if exists test9;
            drop index if exists idx9;
            create table test9(col_4 date not null)
            partition by range (col_4)interval ('1 month')
            (partition test9_p1 values less than ('2020-01-01'));
            create unique index idx9 on test9(col_4);
            insert into test9 values('2018-12-31'),('2019-12-31'),
            ('2020-12-31'),('2021-12-31'),('2022-12-31');
            '''
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('CREATE TABLE') > -1)
        self.assertTrue(msg0.count('INSERT 0 5') == 1)

        self.log.info('--步骤2 删除索引后vacuum partition--')
        cmd1 = f'''drop index idx9;
            vacuum verbose test9 partition (test9_p1);'''
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue(msg1.find('DROP INDEX') > -1)
        self.assertTrue(msg1.find('INFO:  vacuuming "public.test9"') > -1)
        self.assertTrue(msg1.find(
            'DETAIL:  0 dead row versions cannot be removed yet.') > -1)

        self.log.info('--步骤3 删除数据后vacuum partition--')
        cmd2 = f'''delete from test9;
            vacuum verbose test9 partition (test9_p1);'''
        msg2 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg2)
        self.assertTrue(msg2.find('DELETE 5') > -1)
        self.assertTrue(msg2.find('INFO:  vacuuming "public.test9"') > -1)
        self.assertTrue(msg1.count(
            'DETAIL:  2 dead row versions cannot be removed yet.') > -1)

    def tearDown(self):
        self.commonsh.execut_db_sql('drop table if exists test9;'
                                    ' drop index if exists idx9;')
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0080结束')

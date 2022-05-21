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
Case Type   : 功能测试
Case Name   : interval分区,COPY TO后再COPY FROM。
Description :
    1. 创建表,表数据copy to到一个文件
    2. 将上面文件内容再次copy from到表里
Expect      :
    1. 创建成功，copy to成功
    2. copy from成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.user = Node('dbuser')
        self.commonsh = CommonSH('dbuser')
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0076开始')

    def test_copy(self):
        self.log.info('---步骤1 创建interval分区表---')
        cmd0 = '''drop table if exists tb3;
            create table tb3( 
            col_4 date,
            col_5 boolean, 
            col_6 nchar(30),
            col_7 float
            )
            partition by range (col_4)
            interval ('1 month') 
            (
                partition tb3_p1 values less than ('2020-03-01'),
                partition tb3_p2 values less than ('2020-04-01'),
                partition tb3_p3 values less than ('2020-05-01')
            );
            insert into tb3 values ('2020-02-23',true,'aaa',1.1);
            insert into tb3 values ('2020-03-23',false,'bbb',2.2);
            insert into tb3 values ('2020-04-23',true,'ccc',3.3);
            insert into tb3 values ('2020-05-23',false,'ddd',4.4);
            insert into tb3 values ('2020-06-23',true,'eee',5.5);
            insert into tb3 values ('2020-07-23',false,'fff',6.6);
            '''
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('CREATE TABLE') > -1)
        self.assertTrue(msg0.count('INSERT 0 1') == 6)

        self.log.info('--步骤2 创建一个文件,将表数据拷贝进来再将文件拷入表--')
        self.file = os.path.join(macro.DB_INSTANCE_PATH, 'copy1.txt')
        self.user.sh(f"rm -rf {self.file};touch {self.file}")
        cmd1 = f"copy tb3 to '{self.file}';"
        msg1 = self.commonsh.execut_db_sql(cmd1)
        self.log.info(msg1)
        self.assertTrue(msg1.find('COPY 6') > -1)
        msg2 = self.user.sh(f"cat {self.file}").result()
        self.log.info(msg2)
        self.assertTrue(msg2.count('2020-') == 6)

        cmd2 = f"copy tb3 from '{self.file}';"
        msg2 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg2)
        self.assertTrue('COPY 6' in msg2)

        self.log.info('--步骤3 查看表内容,拷贝进来的数据和原有数据相同')
        cmd3 = 'select * from tb3;'
        msg3 = self.commonsh.execut_db_sql(cmd3)
        self.log.info(msg3)
        data = msg3.split('\n')[2:-1]
        self.assertTrue(len(data) == 12 and len(set(data)) == 6)

    def tearDown(self):
        self.commonsh.execut_db_sql('drop table if exists tb3 cascade;')
        self.user.sh(f'rm -rf {self.file}')
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0076结束')
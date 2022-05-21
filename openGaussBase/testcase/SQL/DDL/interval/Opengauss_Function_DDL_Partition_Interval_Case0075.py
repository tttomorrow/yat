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
Case Name   : interval分区,COPY FROM从一个文件拷贝数据到一个表。
Description :
    1. 创建表和一个文件，文件中写入合法数据，执行copy from
Expect      :
    1. 创建成功，copy from成功
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
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0075开始')

    def test_copy(self):
        self.log.info('---步骤1 创建interval分区表---')
        cmd0 = '''drop table if exists tb2;
            create table tb2(col_4 date)
            partition by range (col_4)
            interval ('1 year') 
            (
                partition tb2_p1 values less than ('2020-03-01'),
                partition tb2_p2 values less than ('2020-04-01'),
                partition tb2_p3 values less than ('2020-05-01')
            );
            '''
        msg0 = self.commonsh.execut_db_sql(cmd0)
        self.log.info(msg0)
        self.assertTrue(msg0.find('CREATE TABLE') > -1)

        self.log.info('--步骤2 创建文件并写入合法数据，将文件内容copy到表中')
        self.file = os.path.join(macro.DB_INSTANCE_PATH, 'copy2.txt')
        self.user.sh(f"rm -rf {self.file};touch {self.file}")
        for i in range(2018, 2025):
            cmd1 = f"echo -e '{i}-08-09' >> {self.file}"
            self.log.info(cmd1)
            msg1 = self.user.sh(cmd1).result()
            self.log.info(msg1)
        msg2 = self.user.sh(f"cat {self.file}").result()
        self.log.info(msg2)
        cmd2 = f"copy tb2 from '{self.file}';"
        msg2 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg2)
        self.assertTrue('COPY 7' in msg2)

        self.log.info('--步骤3 查看表内容')
        cmd3 = 'select * from tb2;'
        msg3 = self.commonsh.execut_db_sql(cmd3)
        self.log.info(msg3)
        self.assertTrue(msg3.count('08-09 00:00:00') == 7)

    def tearDown(self):
        self.commonsh.execut_db_sql('drop table if exists tb2 cascade;')
        self.user.sh(f'rm -rf {self.file}')
        self.log.info('Opengauss_Function_DDL_Partition_Interval_Case0075结束')
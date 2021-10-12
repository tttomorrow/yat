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
Case Name   : COPY FROM一个文件拷贝数据到一个有jsonb类型的表
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
from testcase.utils.Constant import Constant


class Copy(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.user = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.file = os.path.join(macro.DB_INSTANCE_PATH, 'copy139.txt')
        self.log.info('Opengauss_Function_Datatype_Jsonb_Case0139开始')

    def test_copy(self):
        self.log.info('---步骤1 创建数据类型为jsonb的表---')
        sql_cmd1 = self.commonsh.execut_db_sql(f"drop table if exists tab139;"
            f"create table tab139"
            f"(id int,name varchar,message jsonb,number text);"
            f"insert into tab139 values(001,'Jane','18',159);"
            f"insert into tab139 values(012,'Joy','19',159);"
            f"insert into tab139 values(023,'Jack','20',159);"
            f"insert into tab139 values(004,'Json','23',159);"
            f"insert into tab139 values(005,'Jim','21',159);")
        self.log.info(sql_cmd1)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd1)

        self.log.info('--步骤2 创建一个文件,将表数据拷贝进来--')
        self.user.sh(f"rm -rf {self.file};touch {self.file}")
        sql_cmd2 = self.commonsh.execut_db_sql(f"copy tab139 to"
                                            f" '{self.file}';")
        self.log.info(sql_cmd2)
        self.assertTrue(sql_cmd2.find('COPY 5') > -1)
        msg2 = self.user.sh(f"cat {self.file}").result()
        self.log.info(msg2)
        self.assertTrue(msg2.count('159') == 5)

        self.log.info('--步骤3 将文件内容copy到表中')
        sql_cmd3 = self.commonsh.execut_db_sql(f"copy tab139 from"
                                               f" '{self.file}';")
        self.log.info(sql_cmd3)
        self.assertTrue('COPY 5' in sql_cmd3)

        self.log.info('--步骤4 查看表内容')
        sql_cmd4 = self.commonsh.execut_db_sql(f'select * from tab139;')
        self.log.info(sql_cmd4)
        self.assertTrue(sql_cmd4.count('159') == 10)

    def tearDown(self):
        self.log.info('--清理环境--')
        sql_cmd5 = self.commonsh.execut_db_sql(f'drop table if exists'
                                               f' tab139 cascade;')
        self.log.info(sql_cmd5)
        self.user.sh(f"rm -rf {self.file};")
        self.log.info('Opengauss_Function_Datatype_Jsonb_Case0139开始结束')
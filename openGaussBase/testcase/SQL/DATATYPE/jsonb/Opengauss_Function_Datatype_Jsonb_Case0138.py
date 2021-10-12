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
Case Name   : COPY TO把一个有jsonb类型的表数据拷贝到一个文件
Description :
    1. 创建表,表数据copy to到一个文件
Expect      :
    1. 创建成功，copy to成功
History     :
"""

import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


class Copy(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.user = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.file = os.path.join(macro.DB_INSTANCE_PATH, 'copy138.txt')
        self.log.info('Opengauss_Function_Datatype_Jsonb_Case0138开始')

    def test_copy(self):
        self.log.info('---步骤1 创建数据类型为jsonb的表---')
        sql_cmd1 = self.commonsh.execut_db_sql(f"drop table if exists tab138;"
            f"create table tab138"
            f"(id int,name varchar,message jsonb,number text);"
            f"insert into tab138 values(001,'Jane','18',159);"
            f"insert into tab138 values(012,'Joy','19',159);"
            f"insert into tab138 values(023,'Jack','20',159);"
            f"insert into tab138 values(004,'Json','23',159);"
            f"insert into tab138 values(005,'Jim','21',159);")
        self.log.info(sql_cmd1)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, sql_cmd1)
        self.log.info('--步骤2 创建一个文件,将表数据拷贝进来--')
        self.user.sh(f"rm -rf {self.file};touch {self.file}")
        sql_cmd2 = self.commonsh.execut_db_sql(f"copy tab138 to"
                                            f" '{self.file}';")
        self.log.info(sql_cmd2)
        self.assertTrue(sql_cmd2.find('COPY 5') > -1)
        msg3 = self.user.sh(f"cat {self.file}").result()
        self.log.info(msg3)
        self.assertTrue(msg3.count('159') == 5)

    def tearDown(self):
        sql_cmd4 = 'drop table if exists tab138'
        excute_cmd4 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.user.db_name} ' \
            f'-p {self.user.db_port} '\
            f'-c "{sql_cmd4}";' \
            f'rm -rf {self.file};'
        self.log.info(excute_cmd4)
        msg4 = self.user.sh(excute_cmd4).result()
        self.log.info(msg4)
        self.log.info('Opengauss_Function_Datatype_Jsonb_Case0138结束')
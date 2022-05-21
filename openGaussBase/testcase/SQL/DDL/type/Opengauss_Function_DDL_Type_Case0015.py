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
'''
--  @testpoint:修改类型所有者为new_owner
'''
import sys
import unittest

from yat.test import macro

sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0015开始执行-----------------------------')

    def test_common_user_permission(self):
        # 创建类型
        sql_cmd1 = commonsh.execut_db_sql('''drop type if exists test2_type cascade;
                                    create type test2_type as(a int,b text);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_TYPE_SUCCESS_MSG, sql_cmd1)
        # 创建用户
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists test_user1;
                                        create user test_user1 with password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        # 建表2
        sql_cmd3 = commonsh.execut_db_sql('''drop table if exists t2_test;
                                      CREATE TABLE t2_test(a int, b t_type4);''')
        logger.info(sql_cmd3)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd3)
        # 修改类型所有者
        sql_cmd4 = commonsh.execut_db_sql('''ALTER TYPE test2_type OWNER TO test_user1;''')
        logger.info(sql_cmd4)
        self.assertIn(constant.ALTER_TYPE_SUCCESS_MSG, sql_cmd4)
        # 查询test_user1的oid
        sql_cmd5 = commonsh.execut_db_sql('''select oid,rolname from pg_authid where rolname  = 'test_user1';''')
        logger.info(sql_cmd5)
        self.assertIn('test_user1', sql_cmd5)
        # 查询类型test2_type的所有者oid为test_user1的oid
        sql_cmd6 = commonsh.execut_db_sql('''select typname,typowner from pg_type where typname = 'test2_type';''')
        logger.info(sql_cmd6)
        self.assertIn('test2_type', sql_cmd6)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd7 = commonsh.execut_db_sql('''drop table if exists t2_test;
                                     drop table if exists t2_test; ''')
        logger.info(sql_cmd7)
        # 删除类型
        sql_cmd8 = commonsh.execut_db_sql('''drop type if exists test2_type cascade;''')
        logger.info(sql_cmd8)
        # 删除用户
        sql_cmd9 = commonsh.execut_db_sql(f'''drop user if exists test_user1;''')
        logger.info(sql_cmd9)
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0015执行结束--------------------------')






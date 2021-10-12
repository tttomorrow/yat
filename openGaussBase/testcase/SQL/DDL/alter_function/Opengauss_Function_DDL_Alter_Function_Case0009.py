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
Case Type   :
Case Name   : 修改函数的新所有者,新所有者已存在
Description :
    1.创建函数
    2.查看函数的proowner
    3.创建新用户
    4.修改函数的所有者为test_u1
    5.修改函数的所有者为test_u1
    6.查看函数的所有者
    7.删除函数和用户
Expect      :
    1.创建函数成功
    2.查看函数的proowner成功
    3.创建新用户成功
    4.修改函数的所有者为test_u1成功
    5.修改函数的所有者为test_u1成功
    6.函数的所有者为test_u1
    7.删除函数和用户成功
History     :添加marco文件
"""
import sys
import unittest
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Alter_Function_Case0009开始执行-----------------------------')

    def test_sysadmin_user_permission(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop FUNCTION if EXISTS u_testfun60(c_int int);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.DROP_FUNCTION_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''
CREATE FUNCTION u_testfun60 (INOUT c_int int) RETURNS int  AS \$\$
        BEGIN
                RETURN (c_int);
        END;
\$\$ LANGUAGE plpgsql;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_FUNCTION_SUCCESS_MSG, sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''select proowner,proname from pg_proc where proname='u_testfun60';''')
        logger.info(sql_cmd3)
        self.assertIn('u_testfun60', sql_cmd3)
        sql = f'''drop user if exists test_u1 cascade;
                create user test_u1 with password '{macro.COMMON_PASSWD}';'''
        sql_cmd4 = commonsh.execut_db_sql(sql)
        logger.info(sql_cmd4)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd4)
        sql_cmd5 = commonsh.execut_db_sql('''ALTER FUNCTION u_testfun60 ( INOUT c_int int) owner to test_u1; ''')
        logger.info(sql_cmd5)
        self.assertIn(constant.ALTER_FUNCTION_SUCCESS_MSG, sql_cmd5)
        sql_cmd6 = commonsh.execut_db_sql('''select proowner,proname from pg_proc where proname='u_testfun60';''')
        logger.info(sql_cmd6)
        self.assertIn('u_testfun60', sql_cmd6)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd7 = commonsh.execut_db_sql(''' drop FUNCTION u_testfun60;
                                       drop user if exists test_u1 cascade;''')
        logger.info(sql_cmd7)
        logger.info('------------------------Opengauss_Function_DDL_Alter_Function_Case0009执行结束--------------------------')






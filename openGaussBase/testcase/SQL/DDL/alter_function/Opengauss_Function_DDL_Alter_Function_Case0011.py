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
Case Type   : 修改函数
Case Name   : 函数的所有者,使用ALTER FUNCTION语句，有权限修改
Description :
    1.创建函数
    2.查看函数的proowner
    3.函数重命名
    4.删除函数
Expect      :
    1.创建函数成功
    2.查询成功
    3.函数重命名成功
    4.函数删除成功
History     :
    修改用例
"""
import sys
import unittest

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class FUNCTION(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Alter_Function_Case0011开始执行-----------------------------')

    def test_user_permission(self):

        sql_cmd1 = commonsh.execut_db_sql(''' drop FUNCTION if EXISTS u_testfun60(c_int int);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.DROP_FUNCTION_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''
    CREATE FUNCTION u_testfun60 (INOUT c_int int) RETURNS int  AS \$\$
        BEGIN
                RETURN (c_int);
        END;
\$\$ LANGUAGE plpgsql;                                   
''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_FUNCTION_SUCCESS_MSG, sql_cmd2)
        # 查看函数的proowner
        sql_cmd3 = commonsh.execut_db_sql('''select proowner,proname from pg_proc where proname='u_testfun60';''')
        logger.info(sql_cmd3)
        self.assertIn('u_testfun60', sql_cmd3)
        sql_cmd4 = commonsh.execut_db_sql('''ALTER FUNCTION u_testfun60(INOUT c_int int)rename to u_testfun60_new; ''')
        logger.info(sql_cmd4)
        self.assertIn(constant.ALTER_FUNCTION_SUCCESS_MSG, sql_cmd4)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd5 = commonsh.execut_db_sql(''' drop FUNCTION u_testfun60_new;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DDL_Alter_Function_Case0011执行结束--------------------------')






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
--  @testpoint:修改函数的新所有者,新所有者不存在，合理报错
'''
import sys
import unittest

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Alter_Function_Case0010开始执行-----------------------------')

    def test_sysadmin_user_permission(self):
        # 创建函数
        sql_cmd1 = commonsh.execut_db_sql(''' drop FUNCTION if EXISTS u_testfun60(c_int int);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.DROP_FUNCTION_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''
       CREATE FUNCTION u_testfun60 ( INOUT c_int int) RETURNS int  AS \$\$
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
       # 清理用户
        sql_cmd4 = commonsh.execut_db_sql(f'''drop user if exists test_u1 cascade;''')
        logger.info(sql_cmd4)
        self.assertIn(constant.DROP_ROLE_SUCCESS_MSG, sql_cmd4)
        # 修改函数的所有者为test_u1
        sql_cmd5 = commonsh.execut_db_sql('''ALTER FUNCTION u_testfun60 ( INOUT c_int int) owner to test_u1; ''')
        logger.info(sql_cmd5)
        self.assertIn('ERROR:  role "test_u1" does not exist', sql_cmd5)
        # 查看函数的所有者,未变化
        sql_cmd6 = commonsh.execut_db_sql('''select proowner,proname from pg_proc where proname='u_testfun60';''')
        logger.info(sql_cmd6)
        self.assertIn('u_testfun60', sql_cmd6)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除函数
        sql_cmd7 = commonsh.execut_db_sql(''' drop FUNCTION u_testfun60;''')
        logger.info(sql_cmd7)
        logger.info('------------------------Opengauss_Function_DDL_Alter_Function_Case0010执行结束--------------------------')






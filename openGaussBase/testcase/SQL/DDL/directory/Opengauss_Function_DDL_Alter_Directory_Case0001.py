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
Case Type   : 
Case Name   : 修改directory属主为sysadmin用户
Description :
    1.创建系统管理员用户
    2.创建目录对象
    3.查询管理员信息
    4.修改directory属主为系统管理员
    5.查询目录信息
    6.删除目录
    7.删除用户
Expect      :
    1.创建系统管理员用户成功
    2.创建目录对象成功
    3.查询管理员信息成功
    4.修改directory属主为系统管理员成功
    5.查询目录信息成功
    6.删除目录成功
    7.删除用户成功
History     :
"""
import unittest
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Alter_Directory_Case0001开始执行-----------------------------')

    def test_common_user_permission(self):
        sql = f'''drop user if exists sys_test1 cascade;
                create user sys_test1 with sysadmin password '{macro.COMMON_PASSWD}';'''
        sql_cmd1 = commonsh.execut_db_sql(sql)
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''drop DIRECTORY if exists test_dir1;
                                       create DIRECTORY test_dir1 as '/tmp/';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_DIRECTORY_SUCCESS_MSG, sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''select oid,rolname,rolsystemadmin from pg_authid where rolname = 'sys_test1';''')
        logger.info(sql_cmd3)
        self.assertIn('sys_test1', sql_cmd3)

        sql_cmd4 = commonsh.execut_db_sql('''ALTER DIRECTORY test_dir1 OWNER TO sys_test1;''')
        logger.info(sql_cmd4)
        self.assertIn(constant.ALTER_DIRECTORY_SUCCESS_MSG, sql_cmd4)
        sql_cmd5 = commonsh.execut_db_sql('''select dirname,owner from PG_DIRECTORY where dirname = 'test_dir1';''')
        logger.info(sql_cmd5)
        self.assertIn('test_dir1', sql_cmd5)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd6 = commonsh.execut_db_sql('''DROP DIRECTORY test_dir1;''')
        logger.info(sql_cmd6)
        self.assertIn(constant.DROP_DIRECTORY_SUCCESS_MSG, sql_cmd6)
        sql_cmd7 = commonsh.execut_db_sql('''drop user sys_test1 cascade;''')
        logger.info(sql_cmd7)
        self.assertIn(constant.DROP_ROLE_SUCCESS_MSG, sql_cmd7)
        logger.info('------------------------Opengauss_Function_DDL_Alter_Directory_Case0001执行结束--------------------------')






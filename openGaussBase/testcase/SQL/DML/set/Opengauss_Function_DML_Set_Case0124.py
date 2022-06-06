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
Case Type   : reset SESSION AUTHORIZATION
Case Name   : 事务中，使用reset SESSION AUTHORIZATION重置当前会话用户
Description :
    1.开启事务;创建用户
    2.设置当前用户为t1_paul
    3.回滚后，查看当前会话用户
    4.事务中，set lcoal命令设置用户为t1_paul
    5.删除用户
Expect      :
    1.用户创建成功
    2.设置成功
    3.数据库连接用户
    4.合理报错
    5.用户删除成功
"""
import unittest

from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----Opengauss_Function_DML_Set_Case0124开始执行-----')

    def test_user(self):
        logger.info('''事务中，查看用户''')
        sql_cmd1 = commonsh.execut_db_sql(f'''start transaction;
           drop user if exists t1_paul cascade;
           create user t1_paul identified by '{macro.COMMON_PASSWD}';
           set session authorization t1_paul password '{macro.COMMON_PASSWD}';
           select session_user, current_user; 
           rollback;
           select session_user, current_user;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('t1_paul', sql_cmd1)
        self.assertIn(constant.ROLLBACK_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql(f'''start transaction;
        set local  authorization t1_paul password '{macro.COMMON_PASSWD}';
        end;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.START_TRANSACTION_SUCCESS_MSG, sql_cmd2)
        self.assertIn(constant.SYNTAX_ERROR_MSG, sql_cmd2)
        self.assertIn(constant.ROLLBACK_MSG, sql_cmd2)

    def tearDown(self):
        logger.info('----------清理环境-------')
        sql_cmd1 = commonsh.execut_db_sql('''drop user if exists t1_paul 
            cascade;''')
        logger.info(sql_cmd1)
        logger.info(
            '------Opengauss_Function_DML_Set_Case0124执行结束---')

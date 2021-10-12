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
Case Name   : 使用reset SESSION AUTHORIZATION语法，重置会话用户
Description :
    1.创建用户并设置当前用户为t_paul;查看当前会话用户
    2.重置当前用户，查看当前会话用户
    3.使用reset等价命令
    4.删除用户
Expect      :
    1.当前用户(t_paul)
    2.当前用户(当前登录的数据库用户)
    3.重置成功
    4.用户删除成功
History     :
    修改用例
"""
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

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0123开始执行-----------------------------')

    def test_index(self):

        sql_cmd1 = commonsh.execut_db_sql(f'''drop user if exists t_t_paul cascade;
       CREATE user t_paul IDENTIFIED BY '{macro.COMMON_PASSWD}';
       SET SESSION AUTHORIZATION t_paul password '{macro.COMMON_PASSWD}';
       RESET SESSION AUTHORIZATION;
       SELECT SESSION_USER, CURRENT_USER; ''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd1)
        self.assertIn('t_paul', sql_cmd1)
        self.assertIn(constant.RESET_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql(f'''SET SESSION AUTHORIZATION t_paul password '{macro.COMMON_PASSWD}';
       SELECT SESSION_USER, CURRENT_USER;
       set SESSION AUTHORIZATION default;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd2)
        self.assertIn('t_paul', sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''DROP USER t_paul cascade;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0123执行结束--------------------------')

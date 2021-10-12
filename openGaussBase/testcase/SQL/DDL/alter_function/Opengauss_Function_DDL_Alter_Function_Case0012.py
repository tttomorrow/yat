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
Case Name   : 系统管理员使用ALTER FUNCTION语句，有权限修改
Description :
        1.创建函数
        2.创建用户并赋予系统管理员权限
        3.切换至系统管理员sysadmin1执行alter语句
        4.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.函数重命名成功
        4.清理环境完成
"""
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class AlterFunction(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----Opengauss_Function_DDL_Alter_Function_Case0012开始执行--')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_user_permission(self):
        logger.info('--创建函数--')
        sql_cmd1 = commonsh.execut_db_sql('''drop function if exists 
            u_testfun44(c_int int);''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.DROP_FUNCTION_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''
        create function u_testfun44 ( INOUT c_int int) RETURNS int  AS \$\$
        begin
                return (c_int);
        end;
        \$\$ LANGUAGE plpgsql;''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_FUNCTION_SUCCESS_MSG, sql_cmd2)
        logger.info('--创建用户并赋予系统管理员权限--')
        sql_cmd3 = commonsh.execut_db_sql(f'''drop user if exists sysadmin1 
        cascade;
        create user sysadmin1 with sysadmin password 
        '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd3)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd3)
        logger.info('-切换至系统管理员sysadmin1执行alter语句,函数重命名成功-')
        sql_cmd4 = ('''alter function u_testfun44( INOUT c_int int)rename to 
        u_testfun45;''')
        excute_cmd1 = f'''source {self.DB_ENV_PATH};
                          gsql -d {self.userNode.db_name} \
                          -p {self.userNode.db_port} \
                          -U sysadmin1 -W '{macro.COMMON_PASSWD}' \
                          -c "{sql_cmd4}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.ALTER_FUNCTION_SUCCESS_MSG, msg1)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''drop function u_testfun45;
        drop user if exists sysadmin1 cascade;''')
        logger.info(sql_cmd4)
        logger.info(
            '----Opengauss_Function_DDL_Alter_Function_Case0012执行结束--')

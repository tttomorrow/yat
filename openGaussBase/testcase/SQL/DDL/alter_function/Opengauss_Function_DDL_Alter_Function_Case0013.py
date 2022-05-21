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
Case Type   : 修改函数
Case Name   : 普通用户，使用ALTER FUNCTION语句，无权限修改
Description :
        1.创建函数
        2.创建普通用户
        3.切换至普通用户执行alter语句
        4.删除函数和用户
Expect      :
        1.创建函数成功
        2.创建普通用户成功
        3.合理报错
        4.删除成功
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class AlterFunction(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Alter_Function_Case0013开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_common_user_permission(self):
        # 创建函数
        sql_cmd1 = commonsh.execut_db_sql('''drop FUNCTION if EXISTS u_testfun44(c_int int);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.DROP_FUNCTION_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''
CREATE FUNCTION u_testfun44 ( INOUT c_int int) RETURNS int  AS \$\$
        BEGIN
                RETURN (c_int);
        END;
\$\$ LANGUAGE plpgsql;
  ''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_FUNCTION_SUCCESS_MSG, sql_cmd2)
       # 创建普通用户
        sql_cmd3 = commonsh.execut_db_sql(f'''drop user if exists jj cascade;
                                       create user jj password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd3)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd3)
        # 切换至普通用户执行alter语句,合理报错
        sql_cmd4 = ('''ALTER FUNCTION u_testfun44( INOUT c_int int)rename to u_testfun45;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U jj -W '{macro.COMMON_PASSWD}' -c "{sql_cmd4}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  permission denied for function u_testfun44', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除函数和用户
        sql_cmd4 = commonsh.execut_db_sql('''drop FUNCTION u_testfun44;
                                           drop user if exists jj cascade;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DDL_Alter_Function_Case0013执行结束--------------------------')






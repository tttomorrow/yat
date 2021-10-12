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
Case Name   : 仅登录权限用户设置group用户
Description :
    1.使用初始用户连gsql，创建用户组 期望:创建赋权成功
    2.使用初始用户连gsql，创建用户，给用户赋登录权限，期望:创建赋权成功
    3.使用role7_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role7_001
    4.使用role7_001连接gsql，执行set role语句设置为group用户group7 期望:设置成功，查询CURRENT_USER为group7
    5.使用初始用户连gsql，清理环境。期望:删除用户成功
Expect      :
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

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_Set_Role_Case0007开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_common_user_permission(self):
        logger.info('------------------------创建用户，给用户赋权为sysadmin，期望:创建赋权成功-----------------------------')
        sql_cmd = commonsh.execut_db_sql(f'''drop group if exists group7;create group group7 password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        sql_cmd = commonsh.execut_db_sql(f'''
                                        drop role if exists role7_001;
                                        create role role7_001 in group group7 password '{macro.COMMON_PASSWD}';
                                        alter role role7_001 with login;
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)

        logger.info('-----------使用role7_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role7_001-------------')
        sql_cmd = ('''SELECT SESSION_USER, CURRENT_USER;''')
        excute_cmd = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role7_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("role7_001", msg)

        logger.info('----------使用role7_001连接gsql，执行set role语句设置为group用户group7 期望:设置成功，查询CURRENT_USER为group7---------')
        sql_cmd = (f'''SET session ROLE group7 password '{macro.COMMON_PASSWD}';SELECT SESSION_USER, CURRENT_USER;''')
        excute_cmd = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role7_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("SET", msg)
        self.assertIn("role7_001", msg)
        self.assertIn("group7", msg)

    def tearDown(self):
        logger.info('---------------------------------清理环境。期望:删除用户成功-----------------------------------')
        sql_cmd = commonsh.execut_db_sql('''drop role if exists role7_001;drop group if exists group7;''')
        logger.info(sql_cmd)
        logger.info('-------------------------Opengauss_Function_Set_Role_Case0007执行结束---------------------------')
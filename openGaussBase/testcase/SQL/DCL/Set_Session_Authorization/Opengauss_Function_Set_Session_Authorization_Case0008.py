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
Case Type   : 功能测试
Case Name   : sysadmin和仅登录用户设置自己
Description :
    1.使用初始用户连gsql，创建用户，给用户赋权为sysadmin，期望:创建赋权成功
    2.使用role8_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role8_001
    3.使用role8_001连接gsql，执行set role语句设置为当前用户 期望:设置成功，查询CURRENT_USER为role8_001
    4.使用role8_002连接gsql，查看当前会话用户。期望:SESSION_USER, CURRENT_USER均为role8_001
    6.使用role8_002连接gsql，执行set role语句设置为当前用户 期望:设置成功，查询CURRENT_USER为role8_002
    7.使用初始用户连gsql，清理环境。期望:删除用户成功
Expect      :
History     :
"""

import sys
import unittest
from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_Set_Session_Authorization_Case0008开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_common_user_permission(self):
        logger.info('------------------------创建用户，给用户赋权为sysadmin，期望:创建赋权成功-----------------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''
                                            drop role if exists role8_001;
                                            drop role if exists role8_002;
                                            create role role8_001 password '{macro.COMMON_PASSWD}';
                                            create role role8_002 password '{macro.COMMON_PASSWD}';
                                            alter role role8_001 with login;
                                            alter role role8_002 with login;
                                            grant all privileges to  role8_001;
                                            ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)

        logger.info('-----------使用role8_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role8_001-------------')
        sql_cmd = ('''
                    SELECT SESSION_USER, CURRENT_USER;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role8_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("role8_001", msg)
        self.assertNotIn("role8_002", msg)

        logger.info('----------使用role8_001连接gsql，执行set role语句设置为当前用户 期望:设置成功，查询SESSION_USER,CURRENT_USER为role8_001---------')
        sql_cmd = (f'''
                    SET SESSION AUTHORIZATION role8_001 password '{macro.COMMON_PASSWD}';
                    SELECT SESSION_USER, CURRENT_USER;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role8_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("SET", msg)
        self.assertIn("role8_001", msg)
        self.assertNotIn("role8_002", msg)

        logger.info('-----------使用role8_002连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role8_002-------------')
        sql_cmd = ('''
                    SELECT SESSION_USER, CURRENT_USER;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role8_002 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("role8_002", msg)
        self.assertNotIn("role8_001", msg)

        logger.info('----------使用role8_002连接gsql，执行set role语句设置为当前用户 期望:设置成功，查询CURRENT_USER为role8_002---------')
        sql_cmd = (f'''
                    SET SESSION AUTHORIZATION role8_002 password '{macro.COMMON_PASSWD}';
                    SELECT SESSION_USER, CURRENT_USER;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role8_002 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                    '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("SET", msg)
        self.assertIn("role8_002", msg)
        self.assertNotIn("role8_001", msg)

    def tearDown(self):
        logger.info('---------------------------------清理环境。期望:删除用户成功-----------------------------------')
        sql_cmd = self.commonsh.execut_db_sql('''
                                            drop role if exists role8_001;
                                            drop role if exists role8_002;
                                            ''')
        logger.info(sql_cmd)
        logger.info('-------------------------Opengauss_Function_Set_Session_Authorization_Case0008执行结束---------------------------')

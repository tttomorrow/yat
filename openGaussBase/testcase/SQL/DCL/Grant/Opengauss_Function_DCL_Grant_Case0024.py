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
Case Name   : 授予系统权限createdb、createrole给用户，其他用户不能继承
Description :
        1.创建用户赋予createdb、createrole权限；
        2.退出当前数据库，用新建用户连接数据库；
        3.查看用户是否有createdb、createrole权限；
        4.将用户权限继承给新建用户；
        5.查看继承用户系统信息；
        6.清理环境；
Expect      :
        1.创建用户成功；
        2.连接成功；
        3.有createdb、createrole权限；
        4.grant成功；
        5.集成用户无相关系统权限；
        6.清理环境成功；
History     :
"""

import sys
import unittest
from yat.test import Node
from yat.test import macro
sys.path.append(sys.path[0] + "/../")
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()

class Tools(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_DCL_Grant_Case0024.py start-------------------')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_server_tools(self):
        logger.info('------------------创建用户赋予createdb、createrole权限------------------')
        self.user = 'p_user04'
        sql_cmd1 =f'''
                    
                    drop user if exists {self.user} cascade;
                    create user {self.user} with createdb createrole identified by '{macro.COMMON_PASSWD}';
                    '''
        msg1 = self.sh_primary.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)

        logger.info('------------退出当前数据库，用新建用户连接数据库,查看用户是否有createdb、createrole权限--------------')
        logger.info('----------------------创建新用户、将p_user04权限继承给新用户----------------------')
        sql_cmd2 = f'''select rolcreatedb,rolcreaterole from pg_roles where rolname = '{self.user}';'''
        sql_cmd3 = f'''
                    drop user if exists p_user_new cascade;
                    create user p_user_new identified by '{macro.COMMON_PASSWD}';
                    grant {self.user} to p_user_new;'''
        execute_cmd2 = f'''
                     source {self.DB_ENV_PATH}; 
                     gsql -d {self.userNode.db_name} -U {self.user} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd2}"
                     gsql -d {self.userNode.db_name} -U {self.user} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd3}"
                    '''
        logger.info(execute_cmd2)
        msg2 = self.userNode.sh(execute_cmd2).result()
        logger.info(msg2)
        self.assertIn('t', msg2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg2)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg2)

        logger.info('----------------------查看继承用户，无相关系统权限----------------------')
        sql_cmd4 = f'''select rolcreatedb,rolcreaterole from pg_roles where rolname = 'p_user_new';'''
        execute_cmd4 = f'''
                        source {self.DB_ENV_PATH}; 
                        gsql -d {self.userNode.db_name} -U {self.user} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd4}"
                        '''
        logger.info(execute_cmd4)
        msg4 = self.userNode.sh(execute_cmd4).result()
        logger.info(msg4)
        self.assertIn('f', msg4)

    def tearDown(self):
        logger.info('--------------清理环境-------------------')
        sql_cmd5 = f'''
                    drop user p_user_new cascade;
                    drop user {self.user} cascade;
                    '''
        msg5 = self.sh_primary.execut_db_sql(sql_cmd5)
        logger.info(msg5)
        logger.info('------------------Opengauss_Function_DCL_Grant_Case0024.py finish------------------')

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
Case Name   : 结合with admin option,被授权的用户可以将权限再次授权给其他用户
Description :
        1.创建用户1，创建表；
        2.查看用户1是否有表的相关操作权限
        3.给用户1赋予指定表的select、insert权限；
        4.退出当前数据库，用新建用户1连接数据库；
        5.使用用户1连接数据库，创建用户2，结合with admin option,将用户1的权限授权给用户2；
        6.使用用户2连接数据库，创建用户3，结合with admin option,将用户2的权限授权给用户3；
        7.用新建用户3连接数据库，对指定表进行select、insert操作；
        8.清理环境；
Expect      :
        1.创建用户1成功，创建表成功；
        2.无相关权限；
        3.授权成功；
        4.连接成功；
        5.创建用户2成功，授权成功；
        6.创建用户3成功，授权成功；
        7.select、insert操作成功；
        8.清理环境成功；
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

class Grant(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_DCL_Grant_Case0030.py start-------------------')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_grant(self):
        logger.info('------------------创建普通用户1,创建表------------------')
        self.user1 = 'p_user10_1'
        self.user2 = 'p_user10_2'
        self.user3 = 'p_user10_3'
        self.table = 'p_table'
        sql_cmd1 =f'''                    
                    drop user if exists {self.user1} cascade;
                    create user {self.user1} with createrole identified by '{macro.COMMON_PASSWD}';
                    drop table if exists {self.table};
                    create table {self.table}(id int,name varchar(100));
                    '''
        msg1 = self.sh_primary.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        self.assertIn(self.Constant.CREATE_TABLE_SUCCESS, msg1)

        logger.info('-------------------查看用户1是否有表的相关操作权限-------------------')
        logger.info('------------------将表的select、insert权限赋予用户1-----------------')
        sql_cmd2 = f'''
                    select privilege_type from information_schema.table_privileges where grantee='{self.user1}';
                    grant select,insert on table {self.table} to {self.user1};
                    '''
        msg2 = self.sh_primary.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn('', msg2)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg2)

        logger.info('------------退出当前数据库，用新建用户1连接数据库--------------')
        logger.info('------------创建用户2，将用户1对表的操作权限赋予用户2--------------')
        sql_cmd3 = f'''drop user if exists {self.user2} cascade;
                       create user {self.user2} with createrole identified by '{macro.COMMON_PASSWD}';
                       grant {self.user1} to {self.user2} with admin option;'''
        execute_cmd3 = f'''
                        source {self.DB_ENV_PATH}; 
                        gsql -d {self.userNode.db_name} -U {self.user1} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd3}"
                        '''
        logger.info(execute_cmd3)
        msg3 = self.userNode.sh(execute_cmd3).result()
        logger.info(msg3)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg3)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg3)

        logger.info('------------退出当前数据库，用新建用户2连接数据库--------------')
        logger.info('------------创建用户3，将用户2对表的操作权限赋予用户3--------------')
        sql_cmd4 = f'''drop user if exists {self.user3} cascade;
                       create user {self.user3} identified by '{macro.COMMON_PASSWD}';
                       grant {self.user2} to {self.user3} with admin option;'''
        execute_cmd4 = f'''
                        source {self.DB_ENV_PATH}; 
                        gsql -d {self.userNode.db_name} -U {self.user2} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd4}"
                           '''
        logger.info(execute_cmd4)
        msg4 = self.userNode.sh(execute_cmd4).result()
        logger.info(msg4)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg4)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg4)

        logger.info('------------退出当前数据库，用新建用户3连接数据库，对表进行已赋权操作--------------')
        sql_cmd5 = f'''insert into {self.table} values(1022,'hello');
                       select * from {self.table};
                    '''
        execute_cmd5 = f'''
                        source {self.DB_ENV_PATH}; 
                        gsql -d {self.userNode.db_name} -U {self.user3} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd5}"
                        '''
        logger.info(execute_cmd5)
        msg5 = self.userNode.sh(execute_cmd5).result()
        logger.info(msg5)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, msg5)
        self.assertIn('hello', msg5)

    def tearDown(self):
        logger.info('--------------清理环境-------------------')
        sql_cmd6 = f'''
                    drop table {self.table} cascade;
                    drop user {self.user1} cascade;
                    drop user {self.user2} cascade;
                    drop user {self.user3} cascade;
                    '''
        msg6 = self.sh_primary.execut_db_sql(sql_cmd6)
        logger.info(msg6)
        logger.info('------------------Opengauss_Function_DCL_Grant_Case0030.py finish------------------')

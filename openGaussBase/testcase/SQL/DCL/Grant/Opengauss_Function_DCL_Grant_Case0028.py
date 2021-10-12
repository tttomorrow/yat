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
Case Name   : 给指定用户赋予all privileges权限，只有系统管理员有权限,非系统管理员提示权限拒绝
Description :
        1.创建普通用户1；
        2.使用sysadmin用户赋予普通用户1 all privileges权限；
        3.回收普通用户1 all privileges权限；
        4.用普通用户1连接数据库；
        5.创建普通用户2，用普通用户1给普通用户2赋予all privileges权限；
        6.清理环境；
Expect      :
        1.创建用户1成功；
        2.授权成功；
        3.回收权限成功；
        4.连接数据库成功；
        5.赋权失败；
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

class Grant(unittest.TestCase):
    def setUp(self):
        logger.info('--------------Opengauss_Function_DCL_Grant_Case0028.py start-------------------')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_grant(self):
        logger.info('------------------1.创建普通用户1，用户2------------------')
        logger.info('------------------2.使用具有sysadmin权限的用户赋予p_user08_1用户all权限------------------')
        logger.info('------------------3.查看p_user08_1是否具有管理员权限------------------')
        logger.info('------------------4.回收p_user08_1用户all权限------------------')
        self.user1 = 'p_user08_1'
        self.user2 = 'p_user08_2'
        sql_cmd1 =f'''                    
                    drop user if exists {self.user1} cascade;
                    drop user if exists {self.user2} cascade;
                    create user {self.user1} identified by '{macro.COMMON_PASSWD}';
                    create user {self.user2} identified by '{macro.COMMON_PASSWD}';
                    grant all privileges to {self.user1};
                    select rolsystemadmin from pg_roles where rolname='{self.user1}';
                    revoke all privileges from {self.user1};
                    '''
        msg1 = self.sh_primary.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, msg1)
        self.assertIn('t', msg1)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, msg1)

        logger.info('------------退出当前数据库，用新建用户1连接数据库--------------')
        logger.info('------------用户1对用户2赋予all权限，提示权限拒绝--------------')
        sql_cmd2 = f'''grant all privileges to {self.user2};'''
        execute_cmd2 = f'''
                     source {self.DB_ENV_PATH}; 
                     gsql -d {self.userNode.db_name} -U {self.user1} -W {macro.COMMON_PASSWD} -p {self.userNode.db_port} -c "{sql_cmd2}"
                    '''
        logger.info(execute_cmd2)
        msg2 = self.userNode.sh(execute_cmd2).result().lower()
        logger.info(msg2)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg2)

    def tearDown(self):
        logger.info('--------------清理环境-------------------')
        sql_cmd3 = f'''
                    drop user {self.user1} cascade;
                    drop user {self.user2} cascade;
                    '''
        msg3 = self.sh_primary.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        logger.info('------------------Opengauss_Function_DCL_Grant_Case0028.py finish------------------')

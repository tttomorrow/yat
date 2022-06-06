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
Case Name   : 在事务中加session设置
Description :     
            1.使用初始用户连gsql，创建用户，给用户赋权为sysadmin，
            期望:创建赋权成功
            2.使用role14_001连接gsql，查看当前会话用户，当前用户。
            期望:SESSION_USER, CURRENT_USER均为role14_001
            3.使用role14_001连接gsql，执行set role语句，加session 
            期望:SESSION_USER,CURRENT_USER为role14_002
            4.查询事务中的属主 期望:SESSION_USER,CURRENT_USER为role14_002
            5.使用初始用户连gsql，清理环境。期望:删除用户成功
Expect      : 
            1、显示默认值；
            2、参数修改成功；
            3、查看参数修改成功；
            4、修改成功；
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOGGER = Logger()


class Privategrant(unittest.TestCase):

    def setUp(self):
        LOGGER.info('==Set_Session_Authorization_Case0014开始执行==')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_common_user_permission(self):
        LOGGER.info('创建用户，给用户赋权为sysadmin，期望:创建赋权成功')
        sql_cmd = self.commonsh.execut_db_sql(f'''
            drop table if exists test_set_role_014;
            drop role if exists role14_001;
            drop role if exists role14_002;
            create role role14_001 password '{macro.COMMON_PASSWD}';
            create role role14_002 password '{macro.COMMON_PASSWD}';
            alter role role14_001 with login;
            alter role role14_002 with login;
            grant all privileges to  role14_001;
            grant all privileges to  role14_002;
            ''')
        LOGGER.info(sql_cmd)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)

        LOGGER.info('使用role14_001连接gsql，查看当前会话用户，当前用户')
        LOGGER.info('期望:SESSION_USER, CURRENT_USER均为role14_001')
        sql_cmd = ('''SELECT SESSION_USER, CURRENT_USER;''')

        excute_cmd = f'''source {self.DB_ENV_PATH};\
        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} \
        -U role14_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"'''
        LOGGER.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        LOGGER.info(msg)
        self.assertIn("role14_001", msg)

        LOGGER.info('使用role14_001连接gsql，执行set role语句加session')
        LOGGER.info('期望:SESSION_USER,CURRENT_USER为role14_002')
        sql_cmd = (f'''
                    begin
                        SET SESSION SESSION AUTHORIZATION role14_002 
                        password '{macro.COMMON_PASSWD}';
                        execute immediate 'drop table if exists 
                        test_set_role_014;
                        SELECT SESSION_USER, CURRENT_USER 
                        into test_set_role_014;';
                    end;
                    
                    SELECT SESSION_USER, CURRENT_USER;
                    ''')

        excute_cmd = f'''source {self.DB_ENV_PATH};\
        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} \
        -U role14_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"'''
        LOGGER.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        LOGGER.info(msg)
        self.assertNotIn("role14_001", msg)
        self.assertIn("role14_002", msg)

        LOGGER.info('查询事务中的属主')
        LOGGER.info('期望:SESSION_USER,CURRENT_USER为role14_002')
        sql_cmd = ('''select * from test_set_role_014;''')
        excute_cmd = f'''source {self.DB_ENV_PATH};\
        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} \
        -U role14_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"'''
        LOGGER.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        LOGGER.info(msg)
        self.assertNotIn("role14_001", msg)
        self.assertIn("role14_002", msg)

    def tearDown(self):
        LOGGER.info('==清理环境。期望:删除用户成功==')
        sql_cmd = self.commonsh.execut_db_sql('''
        drop table if exists test_set_role_014;
        drop role if exists role14_001;
        drop role if exists role14_002;
        ''')
        LOGGER.info(sql_cmd)
        LOGGER.info('==Session_Authorization_Case0014执行结束==')

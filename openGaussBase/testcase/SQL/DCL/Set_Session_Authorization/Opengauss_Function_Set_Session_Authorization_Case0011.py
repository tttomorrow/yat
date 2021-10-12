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
Case Name   : 循环3次执行set role和reset role
Description :
    1.使用初始用户连gsql，创建用户，给用户赋登录权限，期望:创建赋权成功
    2.使用role11_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role11_001
    3.使用role11_001连接gsql，循环3+次执行SET SESSION AUTHORIZATION和RESET SESSION AUTHORIZATION 期望，修改成功，查询CURRENT_USER为role11_002，reset成功，查询CURRENT_USER为role11_001
    3.使用初始用户连gsql，查询4的执行结果
    select * from test_set_role_011_00;
    select * from test_set_role_011_01;
    select * from test_set_role_011_02;
    --期望，此3张表查询SESSION_USER为role11_001, CURRENT_USER为group11
    select * from test_set_role_012_00;
    select * from test_set_role_012_01;
    select * from test_set_role_012_02;
    --期望，此3张表查询SESSION_USER为role11_001, CURRENT_USER为role11_001
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


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_Set_Session_Authorization_Case0011开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_common_user_permission(self):
        logger.info('------------------------创建用户，期望:创建成功-----------------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''
                                            drop table if exists test_set_role_011_00,test_set_role_011_01,test_set_role_011_02,test_set_role_012_00,test_set_role_012_01,test_set_role_012_02 cascade;
                                            drop role if exists role11_001;
                                            drop role if exists role11_002;
                                            create role role11_001  password '{macro.COMMON_PASSWD}';
                                            create role role11_002  password '{macro.COMMON_PASSWD}';
                                            alter role role11_001 with login;
                                            alter role role11_002 with login;
                                            grant all  privileges to role11_001;
                                            grant all  privileges to role11_002;
                                            ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)

        logger.info('-----------使用role11_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role11_001-------------')
        sql_cmd = ('''
                    SELECT SESSION_USER, CURRENT_USER;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role11_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("role11_001", msg)

        logger.info('----------使用role11_001连接gsql，循环3+次执行SET SESSION AUTHORIZATION和RESET SESSION AUTHORIZATION 期望，修改成功，查询CURRENT_USER为role11_002，reset成功，查询CURRENT_USER为role11_001---------')
        sql_cmd = (f'''
                    begin
                        for i in 0..2 loop
                            SET SESSION AUTHORIZATION role11_002 password '{macro.COMMON_PASSWD}';
                            execute immediate 'drop table if exists test_set_role_011_0'||i||';SELECT SESSION_USER, CURRENT_USER into test_set_role_011_0'||i||';';
                            RESET SESSION AUTHORIZATION;
                            execute immediate 'drop table if exists test_set_role_012_0'||i||';SELECT SESSION_USER, CURRENT_USER into test_set_role_012_0'||i||';';
                        end loop;
                    end;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role11_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("ANONYMOUS BLOCK EXECUTE", msg)

        logger.info('------------------------此3张表查询SESSION_USER,CURRENT_USER为role11_002-----------------------------')
        sql_cmd = self.commonsh.execut_db_sql('''
                                            select * from test_set_role_011_00;
                                            select * from test_set_role_011_01;
                                            select * from test_set_role_011_02;
                                            ''')
        logger.info(sql_cmd)
        self.assertIn("role11_002", sql_cmd)
        self.assertNotIn("role11_001", sql_cmd)

        logger.info('------------------------此3张表查询SESSION_USER,CURRENT_USER为role11_001-----------------------------')
        sql_cmd = self.commonsh.execut_db_sql('''
        select * from test_set_role_012_00;
        select * from test_set_role_012_01;
        select * from test_set_role_012_02;
                                  ''')
        logger.info(sql_cmd)
        self.assertIn("role11_001", sql_cmd)
        self.assertNotIn("role11_002", sql_cmd)

    def tearDown(self):
        logger.info('---------------------------------清理环境。期望:删除用户成功-----------------------------------')
        sql_cmd = self.commonsh.execut_db_sql('''
                                            drop table if exists test_set_role_011_00,test_set_role_011_01,test_set_role_011_02,test_set_role_012_00,test_set_role_012_01,test_set_role_012_02 cascade;
                                            drop role if exists role11_001;
                                            revoke create on schema public from role11_002;
                                            drop group if exists role11_002;
                                            ''')
        logger.info(sql_cmd)
        logger.info('-------------------------Opengauss_Function_Set_Session_Authorization_Case0011执行结束---------------------------')

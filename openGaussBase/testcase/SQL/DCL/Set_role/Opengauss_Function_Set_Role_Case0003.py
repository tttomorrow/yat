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
Case Name   : sysadmin设置初始用户
Description :
    1.使用初始用户连gsql，创建用户，给用户赋权为sysadmin，期望:创建赋权成功
    2.使用role3_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role3_001
    3.使用role3_001连接gsql，执行set role 为初始用户:设置失败，查询CURRENT_USER为role3_001
    4.使用初始用户连gsql，清理环境。期望:删除用户成功
Expect      :
    1.使用初始用户连gsql，创建用户，给用户赋权为sysadmin，期望:创建赋权成功
    2.使用role3_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role3_001
    3.使用role3_001连接gsql，执行set role 为初始用户:设置失败，查询CURRENT_USER为role3_001
    4.使用初始用户连gsql，清理环境。期望:删除用户成功
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
        logger.info('------------------------Opengauss_Function_Set_Role_Case0003开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.username = self.userNode.ssh_user
        self.password = macro.GAUSSDB_INIT_USER_PASSWD

    def test_common_user_permission(self):
        logger.info('------------------------创建用户，给用户赋权为sysadmin，期望:创建赋权成功-----------------------------')
        sql_cmd = commonsh.execut_db_sql(f'''
                                        drop role if exists role3_001;
                                        create role role3_001 password '{macro.COMMON_PASSWD}';
                                        alter role role3_001 with login;
                                        grant all privileges to  role3_001;
                                        ''')
        logger.info(sql_cmd)
        self.assertIn(self.Constant.DROP_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.Constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)

        logger.info('-----------使用role3_001连接gsql，查看当前会话用户，当前用户。期望:SESSION_USER, CURRENT_USER均为role3_001-------------')
        sql_cmd = ('''
                    SELECT SESSION_USER, CURRENT_USER;
                    ''')
        excute_cmd = f'''
                        source {self.DB_ENV_PATH};
                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role3_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                        '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn("role3_001", msg)
        self.assertNotIn("role3_002", msg)

        logger.info('---------使用role3_001连接gsql，执行set role 为初始用户:设置失败，查询CURRENT_USER为role3_001----------')
        sql_cmd = (f'''SET ROLE \"{self.username}\" password '{self.password}';SELECT SESSION_USER, CURRENT_USER;''')
        excute_cmd = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U role3_001 -W {macro.COMMON_PASSWD} -c "{sql_cmd}"
                            '''
        logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg)
        self.assertIn("role3_001", msg)

    def tearDown(self):
        logger.info('---------------------------------清理环境。期望:删除用户成功-----------------------------------')
        sql_cmd = commonsh.execut_db_sql('''drop role if exists role3_001;''')
        logger.info(sql_cmd)
        logger.info('-------------------------Opengauss_Function_Set_Role_Case0003执行结束---------------------------')
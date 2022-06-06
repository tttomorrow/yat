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
Case Type   : keyword
Case Name   : opengauss关键字account(非保留)，锁定账户、解锁账户
Description :
    1.创建用户zhangsan
    2.锁定用户
    3.用锁定用户登录数据库
    4.解锁用户
    5.用解锁后的用户登录数据库
Expect      :
    1.创建用户zhangsan成功
    2.锁定用户成功
    3.用锁定用户登录数据库失败
    4.解锁用户成功
    5.用解锁后的用户登录数据库成功
History     :
"""

import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info("------------------- Opengauss_Function_Keyword_Account_Case0035 开始执行------------------------")
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_account(self):
        logger.info("------------------------创建用户zhangsan--------------------------")
        sql_cmd1 = commonsh.execut_db_sql(f'''CREATE USER zhangsan password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        self.assertIn('CREATE ROLE', sql_cmd1)
        logger.info("------------------------锁定用户--------------------------")
        sql_cmd2 = commonsh.execut_db_sql('''ALTER USER  zhangsan ACCOUNT LOCK;''')
        logger.info(sql_cmd2)
        self.assertIn('ALTER ROLE', sql_cmd2)
        logger.info("------------------------用锁定用户登录数据库--------------------------")
        excute_cmd3 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U  zhangsan -W '{macro.COMMON_PASSWD}' -c "SELECT coalesce(NULL,'hello');"
                            '''
        logger.info(excute_cmd3)
        msg1 = self.userNode.sh(excute_cmd3).result()
        logger.info(msg1)
        self.assertIn('The account has been locked', msg1)
        logger.info("------------------------解锁用户--------------------------")
        sql_cmd4 = commonsh.execut_db_sql(''' ALTER USER  zhangsan ACCOUNT UNLOCK;''')
        logger.info(sql_cmd4)
        self.assertIn('ALTER ROLE', sql_cmd4)
        logger.info("------------------------用解锁后的用户登录数据库--------------------------")
        excute_cmd5 = f'''
                                   source {self.DB_ENV_PATH};
                                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U  zhangsan -W '{macro.COMMON_PASSWD}' -c "SELECT coalesce(NULL,'hello');"
                                   '''
        logger.info(excute_cmd5)
        msg1 = self.userNode.sh(excute_cmd5).result()
        logger.info(msg1)
        self.assertIn('hello', msg1)

    def tearDown(self):
        logger.info("-----------------------清理创建的用户---------------------------")
        sql_cmd = commonsh.execut_db_sql(''' drop user zhangsan;''')
        logger.info(sql_cmd)
        self.assertIn('DROP ROLE', sql_cmd)

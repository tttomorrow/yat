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
Case Type   : security-user
Case Name   : 安全策略管理员用户可以进行DDL操作
Description :
    1.创建安全策略管理员用户
    CREEATE USER poladmin WITH POLADMIN PASSWORD 'QAZ2WSX@123'
    2.安全策略管理员用户登录，执行DDL语句
    CREATE TABLE table001(id INT);
    INSERT INTO table001 VALUES(3);
    DROP TABLE table001;
Expect      :
    1.CREATE ROLE
    2.CREATE TABLE
    INSERT 3
    DROP TABLE
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common


class Privategrant(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '------Opengauss_Function_Security_User_Case0014 start-----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_default_permission(self):
        self.logger.info('---------创建POLADMIN用户-------------')
        sql_cmd1 = f'CREATE USER poladmin WITH POLADMIN PASSWORD ' \
                   f'\'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.assertTrue(msg1.find('CREATE ROLE') > -1)
        self.logger.info('---------POLADMIN用户执行DDL语句------------')
        sql_cmd2 = 'CREATE TABLE table001(id INT);' \
                   'INSERT INTO table001 VALUES(3);' \
                   'DROP TABLE table001;'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U poladmin -W ' \
                      f'{macro.COMMON_PASSWD} -c "{sql_cmd2}"'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'CREATE TABLE', 'INSERT 0 1',
                                  'DROP TABLE')

    def tearDown(self):
        self.logger.info('---------清理环境-----------')
        sql_cmd1 = f'drop user poladmin;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertTrue(msg1.find('DROP ROLE') > -1)
        self.logger.info(
            '----Opengauss_Function_Security_User_Case0014 finish----')

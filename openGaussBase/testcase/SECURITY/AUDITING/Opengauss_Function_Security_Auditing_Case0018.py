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
Case Type   : security-auditing
Case Name   : 设置audit_user_locked=1
Description :
    步骤 1.查看audit_user_locked默认值
    步骤 2.管理员用户登录，锁定账号user003:alter user user003 account lock;
    步骤 3.解锁账户  alter user user003 account unlock
    步骤 4.登录数据库，查看审计日志SELECT * FROM pg_query_audit('$start_time','$end_time');时间设在最接近登录数据库的时间
Expect      :
    步骤 1.默认值1
    步骤 2.锁定成功
    步骤 3.解锁成功
    步骤 4.查询到锁定、解锁的信息
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0018 start----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        sql_cmd0 = 'show audit_user_locked;'
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'audit_user_locked', '1', '(1 row)',
                                  flag='1')
        sql_cmd1 = f'drop user if exists user003 cascade;' \
                   f'create user user003 with password ' \
                   f'\'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertTrue(msg1.find('CREATE ROLE') > -1)
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        sql_cmd2 = 'alter user user003 account lock;' \
                   'alter user user003 account unlock;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'select * from pg_query_audit(\'{start_time}\',' \
                   f'\'{end_time}\');'
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd3}"'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find('the user(user003) has been locked') > -1)
        self.assertTrue(msg3.find('the user(user003) has been unlocked') > -1)

    def tearDown(self):
        sql_cmd1 = '''drop user user003;'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0018 end----')

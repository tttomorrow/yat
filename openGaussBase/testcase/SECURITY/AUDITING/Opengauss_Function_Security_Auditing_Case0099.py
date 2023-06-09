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
Case Type   : security-auditing
Case Name   : 查看审计记录，start_time>end_time
Description :
    1.创建auditadmin属性的用户，CREATE USER audit_admin WITH AUDITADMIN
    password "$PASSWORD";
    2.登录数据库，查看审计记录， SELECT * FROM pg_query_audit('$start_time',
    'end_time');其中start time>endtime
    3.删除用户
Expect      :
    1.创建成功
    2.无法查询到审计记录
    3.删除成功
History     :
"""
import unittest
import datetime
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '-------Opengauss_Function_Security_Auditing_Case0099 star-----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.common = Common()
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_security(self):
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        time.sleep(5)
        sql_cmd1 = f'create user audit_admin with password ' \
                   f'\'{macro.COMMON_PASSWD}\';' \
                   f'create table table01(id int);' \
                   f'drop table table01;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        time.sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd3 = f'select  * from pg_query_audit(\'{end_time}\',\
                   \'{start_time}\');'
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd3}"'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find('(0 rows)'))

    def tearDown(self):
        sql_cmd1 = 'drop user audit_admin;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.logger.info(
            '-----Opengauss_Function_Security_Auditing_Case0099 end-----')

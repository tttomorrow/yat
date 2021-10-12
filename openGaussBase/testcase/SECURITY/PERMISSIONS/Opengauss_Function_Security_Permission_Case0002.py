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
Case Type   : Separation_permission
Case Name   : 非对象所有者不能查询对象
Description :
    1.初始用户执行：create user wf with password 'Qazwsx@123';
                grant create on database postgres to wf;
                create table security_table(id1 int,id2 int, id3 int)
    2.wf用户执行：select * from security_table;
Expect      :
    1.CREATE ROLE
    GRANT
    CREATE TABLE
    2.PERMISSION DENIED
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info(
            '-----Opengauss_Function_Security_Permission_Case0002 start-----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_default_permission(self):
        logger.info('---------create user || table----------')
        sql_cmd1 = f'create user wf with password ' \
                   f'\'{macro.COMMON_PASSWD}\';' \
                   f'grant create on database postgres to wf;' \
                   f'create table security_table(id1 int,id2 int, id3 int)'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg1)
        sql_cmd2 = 'select * from security_table;'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U  wf -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertIn(self.Constant.PERMISSION_DENIED, msg2)

    def tearDown(self):
        sql_cmd1 = 'drop table if exists security_table cascade;' \
                   'drop user if exists wf cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info(
            '----Opengauss_Function_Security_Permission_Case0002 finish----')

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
Case Type   : security-permission
Case Name   : 支持select权限赋予
Description :
    1.初始用户执行：create user wf with password '{macro.COMMON_PASSWD}';
                    create table security_table(id1 int,id2 int, id3 int);
                    grant select on security_table to wf;
    2.wf用户执行：select * from security_table;
Expect      :
    1.CREATE ROLE
       CREATE TABLE
       GRANT
    2.查询出表中内容id1,id2,id3的值
History     :
"""
import os
import sys
import unittest
from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info(
            '-----Opengauss_Function_Security_Permission_Case0005 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.common = Common()
        self.commonsh = CommonSH()
        self.Constant = Constant()

    def test_default_permission(self):
        logger.info('------------create user || table-----------------')
        sql_cmd1 = f'create user wf with password \'{macro.COMMON_PASSWD}\';' \
                   f'create table security_table(id1 int,id2 int,id3 int);' \
                   f'grant select on security_table to wf;'
        sql_cmd2 = 'select * from security_table;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd1}"'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U wf -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertTrue(msg1.find("GRANT") > -1)

        logger.info(excute_cmd1)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'id1 | id2 | id3', '(0 rows)',
                                  flag="1")

    def tearDown(self):
        sql_cmd1 = 'drop table if exists security_table cascade;' \
                   'drop user if exists wf cascade;'
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -c "{sql_cmd1}"'''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        logger.info(
            '----Opengauss_Function_Security_Permission_Case0005 finish-----')

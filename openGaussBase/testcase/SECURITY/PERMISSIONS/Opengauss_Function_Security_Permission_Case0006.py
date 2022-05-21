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
Case Type   : Separation_permission
Case Name   : 支持insert权限赋予
Description :
    1.初始用户执行：create user wf with password '$PASSWORD';
                create table security_table(id1 int,id2 int, id3 int);
                grant select on security_table to wf;
    2.wf用户执行：insert into security_table values(2,3,5);
Expect      :
    1.CREATE ROLE
    CREATE TABLE
    GRANT
    2.数据插入成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import *
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
common = Common()
commonsh = CommonSH()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----Opengauss_Function_Security_Permission_Case0006 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_default_permission(self):
        logger.info('--------create user || table-------')
        sql_cmd1 = f'''create user wf with password '{macro.COMMON_PASSWD}';
                    create table security_table(id1 int,id2 int, id3 int);
                    grant select on security_table to wf;
                    '''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg1)
        sql_cmd2 = 'select * from security_table;'
        SqlMdg = commonsh.execut_db_sql(sql_cmd2)
        common.equal_sql_mdg(SqlMdg, 'id1 | id2 | id3', '(0 rows)', flag="1")

    def tearDown(self):
        sql_cmd1 = 'drop table if exists security_table cascade;' \
                   'drop user if exists wf cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info(
            '----Opengauss_Function_Security_Permission_Case0006 finish----')

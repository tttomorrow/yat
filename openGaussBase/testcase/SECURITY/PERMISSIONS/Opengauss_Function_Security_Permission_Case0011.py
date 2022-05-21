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
Case Name   : 支持EXECUTE权限赋予
Description :
    1.初始用户执行：create user wf with password '$PASSWORD';
                DROP FUNCTION IF EXISTS func_add_sql() CASCADE;
                CREATE FUNCTION func_add_sql(integer, integer) RETURNS integer
                AS 'select $1 + $2' LANGUAGE SQL
                IMMUTABLE RETURNS NULL ON NULL INPUT;
                GRANT EXECUTE ON FUNCTION func_add_sql(integer, integer) TO wf;
    2.wf用户执行：call func_add_sql(3,5);
Expect      :
    1.CREATE ROLE
    DROIP
    CREATE FUNCTION
    GRANT
    2.调用成功，返回值8
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


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info(
            '----Opengauss_Function_Security_Permission_Case0011 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()

    def test_default_permission(self):
        logger.info('----------create function || table----------')
        sql_cmd1 = f'create user wf with password \'{macro.COMMON_PASSWD}\';' \
                   f'DROP FUNCTION IF EXISTS func_add_sql() CASCADE;' \
                   f'CREATE FUNCTION func_add_sql(integer, integer) RETURNS ' \
                   f'integer AS \'select \$1 + \$2\' LANGUAGE SQL IMMUTABLE ' \
                   f'RETURNS NULL ON NULL INPUT;' \
                   f'GRANT EXECUTE ON FUNCTION func_add_sql(integer, ' \
                   f'integer) TO wf;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, msg1)
        sql_cmd2 = 'call func_add_sql(3,5);'
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U  wf -W ' \
                      f'\'{macro.COMMON_PASSWD}\' -c "{sql_cmd2}"'
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        common.equal_sql_mdg(msg2, 'func_add_sql', '8', '(1 row)', flag="1")

    def tearDown(self):
        sql_cmd1 = 'DROP FUNCTION func_add_sql(integer, integer);' \
                   'drop user if exists wf cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info(
            '-----Opengauss_Function_Security_Permission_Case0011 finish----')

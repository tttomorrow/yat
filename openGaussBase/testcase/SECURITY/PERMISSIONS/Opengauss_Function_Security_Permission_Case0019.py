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
Case Name   : 取消用户revoke权限
Description :
    1.初始用户执行：create user wf with password '$PASSWORD';
                 create table security_table(id1 int,id2 int, id3 int);
                 revoke revoke on security_table from wf;
Expect      :
    1.不能取消revoke权限，返回无效语句相关的报错信息
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
            '----Opengauss_Function_Security_Permission_Case0019 start---')
        self.userNode = Node('PrimaryDbUser')
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.Constant = Constant()
        self.user = 'u_security_permission_0019'
        self.table = 'table_security_permission_0019'
    
    def test_default_permission(self):
        logger.info('-----------create user || table-----------')
        sql_cmd1 = f'drop user if exists {self.user};' \
            f'create user {self.user} password \'{macro.COMMON_PASSWD}\';' \
            f'drop table if exists {self.table};' \
            f'create table {self.table}(id1 int,id2 int, id3 int);' \
            f'revoke revoke on {self.table} from {self.user};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.UNRECOGNIZED_PRIVILEGE_MSG, msg1)
    
    def tearDown(self):
        sql_cmd1 = f'drop table {self.table};' \
                   f'drop user {self.user} cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info(
            '-----Opengauss_Function_Security_Permission_Case0019 finish----')

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
Case Type   : 用户-权限测试
Case Name   : 非序列所有者修改序列，合理报错
Description :
    1.创建序列
    2.创建普通用户
    3.普通用户执行ALTER SEQUENCE命令
    4.删除用户和序列
Expect      :
    1.创建成功
    2.用户创建成功
    3.合理报错
    4.删除成功
History     :
"""
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Sequence(unittest.TestCase):

    def setUp(self):
        logger.info(
            '--Opengauss_Function_DDL_Alter_Sequence_Case0001开始执行----')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.user_node = Node('dbuser')

    def test_user_permission(self):
        # 创建序列
        sql_cmd1 = commonsh.execut_db_sql('''
        drop sequence if exists t_serial;
        create sequence t_serial start 101;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_SEQUENCE_SUCCESS_MSG, sql_cmd1)
        # 创建普通用户
        sql_cmd2 = commonsh.execut_db_sql(
        f'''drop user if exists test_user1 cascade;
        create user test_user1 password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        # 普通用户执行ALTER SEQUENCE命令，合理报错
        sql_cmd3 = '''alter sequence t_serial maxvalue 10;'''
        excute_cmd1 = f'''
                 source {self.DB_ENV_PATH};
                 gsql -d {self.user_node.db_name} -p {self.user_node.db_port} \
-U test_user1 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}" '''
        msg1 = self.user_node.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('ERROR:  permission denied for relation t_serial', msg1)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''
        drop user test_user1 cascade;
        drop SEQUENCE t_serial;''')
        logger.info(sql_cmd4)
        logger.info(
            '----Opengauss_Function_DDL_Alter_Sequence_Case0001执行结束---')






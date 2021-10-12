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
Case Name   : 普通用户创建词典，合理报错
Description :
    1.创建普通用户
    2.普通用户创建词典
    3.删除用户
Expect      :
    1.用户创建成功
    2.合理报错
    3.删除成功
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
            '--Opengauss_Function_Dictionary_Case0002开始执行----')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.user_node = Node('dbuser')

    def test_user_permission(self):
        logger.info('--创建普通用户--')
        sql_cmd2 = commonsh.execut_db_sql(f'''
        drop user if exists test_user2 cascade;
        create user test_user2 password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        logger.info('普通用户创建词典，报错')
        sql_cmd3 = '''create text search dictionary pg_dict \
        (TEMPLATE = Simple);'''
        excute_cmd1 = f'''source {self.DB_ENV_PATH};\
        gsql -d {self.user_node.db_name} -p {self.user_node.db_port} \
        -U test_user2 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}" '''
        msg1 = self.user_node.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn(
            'must be system admin to CREATE TEXT SEARCH DICTIONARY', msg1)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''
        drop user if exists test_user2 cascade;
         ''')
        logger.info(sql_cmd4)
        logger.info(
            '----Opengauss_Function_Dictionary_Case0002执行结束---')

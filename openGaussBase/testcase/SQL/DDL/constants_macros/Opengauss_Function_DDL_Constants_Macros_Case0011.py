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
Case Type   : 常量与宏
Case Name   : SESSION_USER有效性测试
Description :
    1.查看SESSION_USER
    2.创建普通用户
    3.切换用户
    4.查看SESSION_USER
    5.删除用户
Expect      :
    1.显示当前gsql连接的用户
    2.创建普通用户成功
    3.切换用户成功
    4.显示pili
    5.删除用户成功
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class ConstantsMacros(unittest.TestCase):
    def setUp(self):
        logger.info(
            '------------------------Opengauss_Function_DDL_Constants_Macros_Case0011开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_session_user(self):
        sql_cmd1 = commonsh.execut_db_sql(f'''select SESSION_USER;
                                           drop user if exists pili;
                                          create user pili password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        self.res = sql_cmd1.splitlines()[-2].strip()
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = '''select SESSION_USER;'''
        excute_cmd1 = f'''
                           source {self.DB_ENV_PATH};
                           gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U pili -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                           '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('pili', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''drop user if exists pili;''')
        logger.info(sql_cmd3)
        logger.info(
            '------------------------Opengauss_Function_DDL_Constants_Macros_Case0011执行结束--------------------------')

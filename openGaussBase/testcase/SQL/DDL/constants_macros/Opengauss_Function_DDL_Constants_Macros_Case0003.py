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
Case Type   : 常量与宏
Case Name   : CURRENT_ROLE有效值测试
Description :
    1.查看当前用户
    2.创建新用户
    3.切换用户
    4.查看当前用户
    5.删除用户
Expect      :
    1.和gsql连接的用户一致
    2.创建新用户成功
    3.切换用户成功
    4.显示jolin
    5.用户删除成功
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
            '------------------------Opengauss_Function_DDL_Constants_Macros_Case0003开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_current_role(self):
        sql_cmd1 = commonsh.execut_db_sql(f'''select CURRENT_ROLE;
        drop user if exists jolin;
        create user jolin with sysadmin password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        self.res = sql_cmd1.splitlines()[-2].strip()
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = '''select CURRENT_ROLE;
                      select CURRENT_USER;'''
        excute_cmd1 = f'''
                          source {self.DB_ENV_PATH};
                          gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U jolin -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
                          '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('jolin', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''drop user if exists jolin;''')
        logger.info(sql_cmd3)
        logger.info(
            '------------------------Opengauss_Function_DDL_Constants_Macros_Case0003执行结束--------------------------')

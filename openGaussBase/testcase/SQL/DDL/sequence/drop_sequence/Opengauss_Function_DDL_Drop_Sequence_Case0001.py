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
Case Type   : 序列
Case Name   : 系统管理员删除序列
Description :
        1.创建序列
        2.创建系统管理员
        3.系统管理员删除序列
        4.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.删除成功
        4.清理环境完成
History     :
"""
import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Sequence(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Drop_Sequence_Case0001开始执行-----------------------------')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.userNode = Node('dbuser')
        self.Constant = Constant()

    def test_user_permission(self):
        # 创建序列
        sql_cmd1 = commonsh.execut_db_sql('''drop SEQUENCE if exists t_serial;
                                       CREATE SEQUENCE t_serial START 101;''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.CREATE_SEQUENCE_SUCCESS_MSG, sql_cmd1)
        # 创建系统管理员
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists test_sysadmin;
                                      create user test_sysadmin with sysadmin password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        # 系统管理员删除序列，成功
        sql_cmd3 = ('''drop SEQUENCE t_serial;''')
        excute_cmd1 = f'''
                         source {self.DB_ENV_PATH};
                         gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_sysadmin -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}"
                         '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.DROP_SEQUENCE_SUCCESS_MSG, msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除用户
        sql_cmd4 = commonsh.execut_db_sql('''drop user test_sysadmin cascade;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DDL_Drop_Sequence_Case0001执行结束--------------------------')






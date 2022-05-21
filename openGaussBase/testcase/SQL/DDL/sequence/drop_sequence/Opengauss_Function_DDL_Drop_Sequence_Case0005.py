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
Case Type   : 删除序列
Case Name   : 普通用户删除序列，合理报错
Description :
        1.创建序列
        2.创建普通用户
        3.普通用户删除序列
        4.删除用户和序列
Expect      :
        1.创建序列成功
        2.创建普通用户成功
        3.合理报错
        4.删除成功
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

class DropSequence(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Drop_Sequence_Case0005开始执行-----------------------------')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.userNode = Node('dbuser')
    def test_permisssion(self):
        # 创建序列
        sql_cmd1 = commonsh.execut_db_sql('''drop SEQUENCE if exists t_serial;
                                       CREATE SEQUENCE t_serial START 101;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_SEQUENCE_SUCCESS_MSG, sql_cmd1)
        # 创建普通用户
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists test_user;
                                      create user test_user password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        # 普通用户删除序列，合理报错
        sql_cmd3 = ('''drop SEQUENCE t_serial;''')
        excute_cmd1 = f'''
                                 source {self.DB_ENV_PATH};
                                 gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_user -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}"
                                '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  permission denied for relation t_serial', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除用户
        sql_cmd4 = commonsh.execut_db_sql('''drop user test_user cascade;''')
        logger.info(sql_cmd4)
        self.assertIn(constant.DROP_ROLE_SUCCESS_MSG, sql_cmd4)
        # 删除序列
        sql_cmd5 = commonsh.execut_db_sql('''drop SEQUENCE t_serial;''')
        logger.info(sql_cmd5)
        self.assertIn(constant.DROP_SEQUENCE_SUCCESS_MSG, sql_cmd5)
        logger.info('------------------------Opengauss_Function_DDL_Drop_Sequence_Case0005执行结束--------------------------')






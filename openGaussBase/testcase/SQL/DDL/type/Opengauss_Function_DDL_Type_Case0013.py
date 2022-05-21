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
Case Type   : type
Case Name   : 删除自定义数据类型，if exists选项测试，类型不存在，合理报错
Description :
    1.创建数据类型
    2.创建系统管理员
    3.系统管理员删除自定义数据类型,省略if exists选项
    4.系统管理员删除自定义数据类型，添加if exists选项
    5.系统管理员删除自定义数据类型，省略if exists选项，类型不存在
    6.删除用户
Expect      :
    1.创建数据类型成功
    2.创建系统管理员成功
    3.删除成功
    4.发出notice
    5.合理报错
    6.用户删除成功
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


class InsertPermission(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0013开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_insert_permission(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop type if exists t_type1 cascade;
                                       CREATE TYPE t_type1 AS (f1 int, f2 DECIMAL(10,4));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_TYPE_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists test_insert4 cascade;
       create user test_insert4 with sysadmin password  '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        sql_cmd4 = '''drop type t_type1 RESTRICT;'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_insert4 -W  '{macro.COMMON_PASSWD}' -c "{sql_cmd4}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.DROP_TYPE_SUCCESS_MSG, msg1)
        sql_cmd5 = '''drop type if exists t_type1 RESTRICT;'''
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_insert4 -W  '{macro.COMMON_PASSWD}' -c "{sql_cmd5}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('NOTICE:  type "t_type1" does not exist, skipping', msg1)
        sql_cmd6 = '''drop type t_type1;'''
        excute_cmd1 = f'''
                                   source {self.DB_ENV_PATH};
                                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_insert4 -W  '{macro.COMMON_PASSWD}' -c "{sql_cmd6}"
                                   '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  type "t_type1" does not exist', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd7 = commonsh.execut_db_sql('''drop user if exists test_insert4 cascade;''')
        logger.info(sql_cmd7)
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0013执行结束--------------------------')

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
Case Type   : 视图
Case Name   : 系统管理员使用alter view语句，修改成功
Description :
    1.建表并插入数据
    2.创建视图
    3.创建系统管理员用户
    4.普通用户使用alter view语句重命名视图名
    5.删除表
    6.删除用户
Expect      :
    1.建表并插入数据成功
    2.视图创建成功
    3.系统管理员用户创建成功
    4.合理报错
    5.表删除成功
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


class View(unittest.TestCase):
    def setUp(self):
        logger.info(
            '------------------------Opengauss_Function_DDL_View_Case0014开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_view_permission(self):

        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists table_view_014;
       create table table_view_014(id int,name varchar(20));
       insert into table_view_014 values(1,'hello'),(2,'world');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''drop view if exists temp_view_014 cascade;
       create view temp_view_014 as select * from table_view_014;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_VIEW_SUCCESS_MSG, sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql(f'''drop user if exists test_view014 cascade;
       create user test_view014 with sysadmin password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd3)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd3)
        sql_cmd4 = '''alter view temp_view_014 rename to temp_view_014_new;'''
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_view014 -W '{macro.COMMON_PASSWD}'  -c "{sql_cmd4}"
                            '''
        logger.info(sql_cmd4)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.ALTER_VIEW_SUCCESS_MSG, msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd3 = commonsh.execut_db_sql('''drop table table_view_014 cascade;
        drop user test_view014 cascade;''')
        logger.info(sql_cmd3)
        logger.info(
            '------------------------Opengauss_Function_DDL_View_Case0014执行结束--------------------------')

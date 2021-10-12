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
Case Type   : insert...returning--permission
Case Name   : 没有表的select权限的用户，使用insert..returning子句，合理报错
Description :
    1.建表
    2.创建用户
    3.回收用户表的select权限
    4.切换至test_insert2用户，给表插入数据,使用insert...returning子句
    5.删除表
    6.删除用户
Expect      :
    1.建表成功
    2.用户创建成功
    3.权限回收成功
    4.插入数据失败，合理报错
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


class InsertPermission(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Insert_Case0015开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_insert_permission(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists t_insert02;
       create table t_insert02(id int,name varchar(10));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists test_insert2 cascade;
       create user test_insert2 password  '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''revoke select on t_insert02 from test_insert2;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.REVOKE_SUCCESS_MSG, sql_cmd3)
        # sql_cmd4 = "insert into t_insert02 values (2, r'小明') returning *;"
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_insert2 -W '{macro.COMMON_PASSWD}' -c "insert into t_insert02 values (2, '小明') returning *;"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  permission denied for relation t_insert02', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd5 = commonsh.execut_db_sql('''drop table t_insert02;''')
        logger.info(sql_cmd5)
        sql_cmd6 = commonsh.execut_db_sql('''drop user test_insert2 cascade;''')
        logger.info(sql_cmd6)
        logger.info('------------------------Opengauss_Function_DML_Insert_Case0015执行结束--------------------------')



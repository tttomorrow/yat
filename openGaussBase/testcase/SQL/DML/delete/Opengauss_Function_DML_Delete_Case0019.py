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
'''case Type : delete--delete权限
case Name ：回收用户USING子句引用的表以及condition上读取的表的SELECT权限，执行delete操作，合理报错
description:
    步骤1：建表
    步骤2：插入数据
    步骤3：创建用户
    步骤4：回收用户表的select权限
    步骤5：test_delete用户删除表中重复的数据，使用using子句
    步骤6：删除表
    步骤7：删除用户
expect:
    步骤1：建表成功
    步骤2：数据插入成功
    步骤3：用户创建成功
    步骤4：回收用户表的select权限成功
    步骤5：est_delete用户删除表中重复的数据，合理报错
    步骤6：表删除成功
    步骤7：用户删除成功
'''
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


class DeletePermission(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Delete_Case0019开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_delete_permission(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists t_delete02;
       create table t_delete02(id int,name varchar(10));''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql('''insert into t_delete02 values (1,'小明');
       insert into t_delete02 values (2,'小明');
       insert into t_delete02 values (3,'小明');
       insert into t_delete02 values (4,'小李');
       insert into t_delete02 values (5,'小李');
       insert into t_delete02 values (6,'小李');
       insert into t_delete02 values (7,'小红');
       insert into t_delete02 values (8,'小红');''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql(f'''drop user if exists test_delete1 cascade;
       create user test_delete1 password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd3)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd3)
        sql_cmd4 = commonsh.execut_db_sql('''revoke select on t_delete02 from test_delete1;''')
        logger.info(sql_cmd4)
        self.assertIn(constant.REVOKE_SUCCESS_MSG, sql_cmd4)
        sql_cmd5 = '''delete from t_delete02 a using t_delete02 b where a.id<b.id and a.name=b.name;'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_delete1 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd5}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  permission denied for relation t_delete02', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd6 = commonsh.execut_db_sql('''drop table t_delete02;''')
        logger.info(sql_cmd6)
        sql_cmd7 = commonsh.execut_db_sql('''drop user test_delete1 cascade;''')
        logger.info(sql_cmd7)
        logger.info('------------------------Opengauss_Function_DML_Delete_Case0019执行结束--------------------------')

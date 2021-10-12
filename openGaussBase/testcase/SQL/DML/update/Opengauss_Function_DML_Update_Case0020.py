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
Case Type   : update--权限测试
Case Name   : 用户没有表的update权限，执行update语句，合理报错
Description :
    1.建表并插入数据
    2.创建用户
    3.回收用户test_update的表update权限
    4.test_update用户对表执行update操作
    5.删除表
    6.删除用户
Expect      :
    1.建表成功且数据插入成功
    2.用户创建成功
    3.权限回收成功
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


class Update(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Update_Case0020开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_update_permission(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists t_update02;
       create table t_update02(id int,name varchar(10));
       insert into t_update02 values (1,'小明');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1)
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists test_update cascade;
       create user test_update password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''revoke update on t_update02 from test_update;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.REVOKE_SUCCESS_MSG, sql_cmd3)
        sql_cmd4 = '''update t_update02 set id = id +1 where name = '小明';'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_update -W '{macro.COMMON_PASSWD}' -c "{sql_cmd4}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  permission denied for relation t_update02', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd5 = commonsh.execut_db_sql('''drop table t_update02;
        drop user if exists test_update cascade;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DML_Update_Case0020执行结束--------------------------')

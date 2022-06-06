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
Case Type   : 行访问控制策略
Case Name   : 创建行访问控制策略，行访问控制影响的SQL操作为update（列存表）
Description :
        1.创建行存表all_data
        2.创建用户
        3.插入数据
        4.授予用户表的select和update权限并打开行级安全检查
        5.创建行访问控制策略
        6.以t_user1登录数据库，测试
        7.修改表信息
        8.删除表信息
        9.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.插入成功
        4.赋予权限成功
        5.创建行访问控制策略成功
        6.查询表的所有信息
        7.usr1被允许更改她自己的usr,修改1条数据成功
        8.合理报错
        9.清理环境完成
History     :
"""
import sys
import unittest
from yat.test import macro
from yat.test import Node
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Policy(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0015开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_user_permission(self):
        # 创建列存表test_policy
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists test_policy cascade;
                                       create table test_policy(id int,usr varchar(20))with (ORIENTATION = COLUMN);''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 创建测试用户
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists t_user1 cascade;
                                    create user t_user1 password '{macro.COMMON_PASSWD}';
                                    drop user if exists t_user2 cascade;
                                    create user t_user2 password '{macro.COMMON_PASSWD}';
                                    drop user if exists t_user3 cascade;
                                    create user t_user3 password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG,  sql_cmd2)
        # 向表插入数据
        sql_cmd3 = commonsh.execut_db_sql('''insert into test_policy(id, usr) values(1, 't_user1');
                                      insert into test_policy(id, usr) values(2, 't_user2');
                                      insert into test_policy(id, usr) values(3, 't_user2');
                                      insert into test_policy(id, usr) values(4, 't_user2');
                                      insert into test_policy(id, usr) values(5, 't_user1');
                                      insert into test_policy(id, usr) values(5, 't_user3');''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd3)
        # 授予用户表的select和update权限并打开行级安全检查
        sql_cmd4 = commonsh.execut_db_sql('''grant select,update on test_policy to t_user1,t_user2,t_user3;
                                       ALTER TABLE test_policy ENABLE ROW LEVEL SECURITY;''')
        logger.info(sql_cmd4)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, sql_cmd4)
        self.assertIn(self.Constant.ALTER_TABLE_MSG, sql_cmd4)
        # 创建策略,指定行访问控制影响的数据库用户为public
        sql_cmd5 = commonsh.execut_db_sql('''drop POLICY if exists pol1 ON test_policy;
                                      CREATE POLICY pol1 ON test_policy FOR update TO PUBLIC USING (usr = current_user);''')
        logger.info(sql_cmd5)
        self.assertIn(self.Constant.CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG, sql_cmd5)
        # 以t_user1登录数据库，测试,查询表的所有信息
        # 修改表信息,usr1被允许更改她自己的usr,修改1条数据成功；修改其他用户信息，修改0条
        # 删除表信息，合理报错
        sql_cmd6 = ('''select * from test_policy;
                    update test_policy set usr = 't_user1 doe' where id = 1;
                    update test_policy set usr = 't_user2 doe' where id = 2;
                    delete from test_policy where usr = 't_user1';''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U t_user1 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd6}"
                            '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('t_user1', msg1)
        self.assertIn(self.Constant.UPDATE_SUCCESS_MSG, msg1)
        self.assertIn('ERROR:  permission denied for relation test_policy', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除行访问控制策略
        sql_cmd7 = commonsh.execut_db_sql('''drop POLICY if exists pol1 ON test_policy;''')
        logger.info(sql_cmd7)
        # 删除表
        sql_cmd8 = commonsh.execut_db_sql('''drop table test_policy;''')
        logger.info(sql_cmd8)
        # 删除用户
        sql_cmd9 = commonsh.execut_db_sql(f'''drop user if exists t_user1 cascade;
                                       drop user if exists t_user2 cascade;
                                       drop user if exists t_user3 cascade;''')
        logger.info(sql_cmd9)
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0015执行结束--------------------------')






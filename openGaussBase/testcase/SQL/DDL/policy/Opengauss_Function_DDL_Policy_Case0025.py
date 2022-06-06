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
Case Name   : 定义访问控制策略,行访问控制影响的SQL操作为delete（unlogged表）
Description :
        1.创建unlogged表
        2.创建用户
        3.插入数据
        4.授予用户表的select和delete权限并打开行级安全检查
        5.创建行访问控制策略
        6.以test_user_001登录数据库，测试
        7.以test_user_003登录数据库,修改表信息 usr = 'test_user_003'的id
        8.以test_user_003登录数据库，删除表信息，usr = 'test_user_003'
        9.以test_user_003登录数据库，删除表信息，usr = 'test_user_001' or usr = 'test_user_002'
        10.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.插入成功
        4.赋予权限成功
        5.创建行访问控制策略成功
        6.查询表所有信息
        7.合理报错
        8.删除1条
        9.输出0条
        10.清理环境完成
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
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0025开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_user_permission(self):
        # 创建unlogged表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists test_policy6 cascade;
                                   create unlogged table test_policy6(id int,usr name);''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 创建测试用户
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists test_user_001 cascade;
                                      create user test_user_001 password '{macro.COMMON_PASSWD}';
                                      drop user if exists test_user_002 cascade;
                                      create user test_user_002 password '{macro.COMMON_PASSWD}';
                                     drop user if exists test_user_003 cascade;
                                     create user test_user_003 password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG,  sql_cmd2)
        # 向表插入数据
        sql_cmd3 = commonsh.execut_db_sql('''insert into test_policy6(id, usr) values(1, 'test_user_001');
                                       insert into test_policy6(id, usr) values(2, 'test_user_002');
                                       insert into test_policy6(id, usr) values(3, 'test_user_002');
                                       insert into test_policy6(id, usr) values(4, 'test_user_002');
                                       insert into test_policy6(id, usr) values(5, 'test_user_001');
                                       insert into test_policy6(id, usr) values(5, 'test_user_003');''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd3)
        # 授予用户表的select和delete权限并打开行级安全检查
        sql_cmd4 = commonsh.execut_db_sql('''grant select,delete on test_policy6 to test_user_001,test_user_002,test_user_003;
                                       ALTER TABLE test_policy6 ENABLE ROW LEVEL SECURITY;''')
        logger.info(sql_cmd4)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, sql_cmd4)
        self.assertIn(self.Constant.ALTER_TABLE_MSG, sql_cmd4)
        # 创建策略,指定行访问控制影响的数据库用户为public
        sql_cmd5 = commonsh.execut_db_sql('''drop POLICY if exists t_pol1 ON test_policy6;
                                      CREATE POLICY t_pol1 ON test_policy6 FOR delete TO PUBLIC USING (usr = current_user);''')
        logger.info(sql_cmd5)
        self.assertIn(self.Constant.CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG, sql_cmd5)
        # 以test_user_001登录数据库，测试,查询表所有信息
        sql_cmd6 = ('''select * from test_policy6;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_user_001 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd6}"
                            '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('test_user_001', msg1)
        # 以test_user_003登录数据库,修改表信息 usr = 'test_user_003'的id，合理报错
        # 以test_user_003登录数据库，删除表信息，usr = 'test_user_003',删除1条
        # 以test_user_003登录数据库，删除表信息，usr = 'test_user_001' or usr = 'test_user_002'，删除0条
        sql_cmd7 = ('''update test_policy6 set id = id + 1 where usr = 'test_user_003';
                    delete from test_policy6 where usr = 'test_user_003';
                    delete from test_policy6 where usr = test_user_001' or usr = 'test_user_002';''')
        excute_cmd1 = f'''
                                   source {self.DB_ENV_PATH};
                                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_user_003 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd7}"
                                   '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('ERROR:  permission denied for relation test_policy6', msg1)
        self.assertIn(self.Constant.DELETE_SUCCESS_MSG, msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除行访问控制策略
        sql_cmd8 = commonsh.execut_db_sql('''drop POLICY if exists t_pol1 ON test_policy6;''')
        logger.info(sql_cmd8)
        # 删除表
        sql_cmd9 = commonsh.execut_db_sql('''drop table test_policy6;''')
        logger.info(sql_cmd9)
        # 删除用户
        sql_cmd10 = commonsh.execut_db_sql(f'''drop user if exists test_user_001 cascade;
                                      drop user if exists test_user_002 cascade;
                                      drop user if exists test_user_003 cascade;''')
        logger.info(sql_cmd10)
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0025执行结束--------------------------')






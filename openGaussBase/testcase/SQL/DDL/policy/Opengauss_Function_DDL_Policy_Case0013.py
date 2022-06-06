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
Case Name   : 同一张表创建两个行访问控制策略,执行查询命令
Description :
        1.创建行存表all_data
        2.创建用户
        3.插入数据
        4.授予用户表的select权限并打开行级安全检查
        5.创建行访问控制策略
        6.以test_usr1登录数据库，测试,查询表信息
        7.多个访问控制策略共同作用一张表
        8.再以test_usr1登录，执行查询
        9.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.插入成功
        4.赋予权限成功
        5.创建行访问控制策略成功
        6.只有usr字段值为test_usr1才对用户test_usr1可见
        7.创建成功
        8.查询结果是pol1和pol2两个策略进行OR的结果
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
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0013开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_user_permission(self):
        # 创建行存表test_policy
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists test_policy cascade;
                                    create table test_policy(id int,usr name);''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 创建测试用户
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists test_usr1 cascade;
                                    create user test_usr1 password '{macro.COMMON_PASSWD}';
                                    drop user if exists test_usr2 cascade;
                                    create user test_usr2 password '{macro.COMMON_PASSWD}';
                                    drop user if exists test_usr3 cascade;
                                    create user test_usr3 password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG,  sql_cmd2)
        # 向表插入数据
        sql_cmd3 = commonsh.execut_db_sql('''insert into test_policy(id, usr) values(1, 'test_usr1');
                                      insert into test_policy(id, usr) values(2, 'test_usr2');
                                      insert into test_policy(id, usr) values(3, 'test_usr2');
                                      insert into test_policy(id, usr) values(4, 'test_usr2');
                                      insert into test_policy(id, usr) values(5, 'test_usr1');
                                      insert into test_policy(id, usr) values(5, 'test_usr3');''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd3)
        # 授予用户表的select权限并打开行级安全检查
        sql_cmd4 = commonsh.execut_db_sql('''grant select,update on test_policy to test_usr1,test_usr2,test_usr3;
                                       ALTER TABLE test_policy ENABLE ROW LEVEL SECURITY;''')
        logger.info(sql_cmd4)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, sql_cmd4)
        self.assertIn(self.Constant.ALTER_TABLE_MSG, sql_cmd4)
        # 创建策略,指定行访问控制影响的数据库用户为public
        sql_cmd5 = commonsh.execut_db_sql('''drop POLICY if exists pol1 ON test_policy;
                                      CREATE POLICY pol1 ON test_policy FOR SELECT TO PUBLIC USING (usr = current_user);''')
        logger.info(sql_cmd5)
        self.assertIn(self.Constant.CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG, sql_cmd5)
        # 以test_usr1登录数据库，测试,查询表信息，只有usr字段值为test_usr1才对用户test_usr1可见,故SELECT类操作受行访问控制的影响，只能查看到满足条件(using_expression返回值为TRUE)的元组数据
        sql_cmd6 = ('''select * from test_policy;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_usr1 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd6}"
                            '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('test_usr1', msg1)
        # 多个访问控制策略共同作用一张表
        sql_cmd7 = commonsh.execut_db_sql('''drop POLICY if exists pol2 ON test_policy;
                                      CREATE POLICY pol2 ON test_policy FOR SELECT TO PUBLIC USING (id = 5);''')
        logger.info(sql_cmd7)
        self.assertIn(self.Constant.CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG, sql_cmd7)
        # 再以test_usr1登录，执行查询,可以看出其查询结果是pol1和pol2两个策略进行OR的结果
        sql_cmd8 = ('''select * from test_policy;''')
        excute_cmd1 = f'''
                                    source {self.DB_ENV_PATH};
                                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_usr1 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd8}"
                                    '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('5', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除行访问控制策略
        sql_cmd9 = commonsh.execut_db_sql('''drop POLICY if exists pol1 ON test_policy;
                                    drop POLICY if exists pol2 ON test_policy;''')
        logger.info(sql_cmd9)
        # 删除表
        sql_cmd10 = commonsh.execut_db_sql('''drop table test_policy;''')
        logger.info(sql_cmd10)
        # 删除用户
        sql_cmd11 = commonsh.execut_db_sql(f'''drop user if exists test_usr1 cascade;
                                       drop user if exists test_usr2 cascade;
                                       drop user if exists test_usr3 cascade;''')
        logger.info(sql_cmd11)
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0013执行结束--------------------------')






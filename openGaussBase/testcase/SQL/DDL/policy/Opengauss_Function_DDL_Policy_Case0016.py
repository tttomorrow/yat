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
Case Type   : 行访问控制策略
Case Name   : 创建行访问控制策略，行访问控制影响的SQL操作为delete（列存表）
Description :
        1.创建行存表all_data
        2.创建用户
        3.插入数据
        4.授予用户表的select和delete权限并打开行级安全检查
        5.创建行访问控制策略
        6.以u_usr1用户登录
        7.以u_usr2用户登录，u_usr2用户删除u_usr2信息
        8.以u_usr2用户登录，u_usr2用户删除u_usr1信息
        9.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.插入成功
        4.赋予权限成功
        5.创建行访问控制策略成功
        6.系统管理员可以看到所有的行和字段
        7.删除条目为1条
        8.删除条目为0条
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
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0016开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_user_permission(self):
        # 创建列存表t_passwd1
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists t_passwd1;
        CREATE TABLE t_passwd1 (user_name text,pwhash text,uid int,gid int NOT NULL,real_name text NOT NULL,home_phone text,extra_info text,home_dir text NOT NULL)with (ORIENTATION = COLUMN);''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 创建测试用户,其中u_usr1为系统管理员,u_usr2和u_usr3为普通用户
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists u_usr1 cascade;
                                      create user u_usr1 with sysadmin password '{macro.COMMON_PASSWD}';
                                      drop user if exists u_usr2 cascade;
                                      create user u_usr2 password '{macro.COMMON_PASSWD}';
                                      drop user if exists u_usr3 cascade;
                                      create user u_usr3 password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG,  sql_cmd2)
        # 向表插入数据
        sql_cmd3 = commonsh.execut_db_sql('''INSERT INTO t_passwd1 VALUES('u_usr1','xxx',0,0,'Admin','111-222-3333',null,'/root');
                                      INSERT INTO t_passwd1 VALUES('u_usr2','xxx',1,1,'Bob','123-456-7890',null,'/home/bob');
                                      INSERT INTO t_passwd1 VALUES('u_usr3','xxx',2,1,'Alice','098-765-4321',null,'/home/alice');''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd3)
        # 授予用户表的select和delete权限并打开行级安全检查
        sql_cmd4 = commonsh.execut_db_sql('''grant select,delete on t_passwd1 to u_usr1,u_usr2,u_usr3;
                                       ALTER TABLE t_passwd1 ENABLE ROW LEVEL SECURITY;''')
        logger.info(sql_cmd4)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, sql_cmd4)
        self.assertIn(self.Constant.ALTER_TABLE_MSG, sql_cmd4)
        # 创建策略,指定行访问控制影响的数据库用户为public
        sql_cmd5 = commonsh.execut_db_sql('''drop POLICY if exists pol2 ON t_passwd1;
                                      CREATE POLICY pol2 ON t_passwd1 FOR delete TO PUBLIC USING (user_name = current_user);''')
        logger.info(sql_cmd5)
        self.assertIn(self.Constant.CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG, sql_cmd5)
        # 以u_usr1用户登录，系统管理员可以看到所有的行和字段
        sql_cmd6 = ('''select * from t_passwd1;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U u_usr1 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd6}"
                            '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('u_usr2', msg1)
        # 以u_usr2用户登录，u_usr2用户修改user_name自身字段，合理报错
        # 以u_usr2用户登录，u_usr2用户删除u_usr2信息，删除条目为1条
        # 以u_usr2用户登录，u_usr2用户删除u_usr1信息，删除条目为0条
        sql_cmd7 = ('''update t_passwd1 set user_name = 'u_usr2' where uid = 1;
                   delete from t_passwd1 where user_name = 'u_usr2';
                   delete from t_passwd1 where user_name = 'u_usr1';''')
        excute_cmd1 = f'''
                                   source {self.DB_ENV_PATH};
                                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U u_usr2 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd7}"
                                   '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('ERROR:  permission denied for relation t_passwd1', msg1)
        self.assertIn(self.Constant.DELETE_SUCCESS_MSG, msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除行访问控制策略
        sql_cmd8 = commonsh.execut_db_sql('''drop POLICY if exists pol2 ON t_passwd1;''')
        logger.info(sql_cmd8)
        # 删除表
        sql_cmd9 = commonsh.execut_db_sql('''drop table if exists t_passwd1;''')
        logger.info(sql_cmd9)
        # 删除用户
        sql_cmd10 = commonsh.execut_db_sql(f'''drop user if exists u_usr1 cascade;
                                       drop user if exists u_usr2 cascade;
                                       drop user if exists u_usr3 cascade;''')
        logger.info(sql_cmd10)
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0016执行结束--------------------------')






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
Case Name   : 定义访问控制策略,行访问控制影响的SQL操作为delete（列存分区表）
Description :
        1.创建分区表
        2.创建用户
        3.插入数据
        4.授予用户表的select和delete权限并打开行级安全检查
        5.创建行访问控制策略
        6.以u_usr1用户登录
        7.以u_usr2用户登录，u_usr2用户修改c_usr自身字段
        8.以u_usr2用户登录，u_usr2用户删除u_usr2信息
        9.以u_usr2用户登录，u_usr2用户删除u_usr1信息
        10.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.插入成功
        4.赋予权限成功
        5.创建行访问控制策略成功
        6.系统管理员可以看到所有的行和字段
        7.合理报错
        8.删除条目为1条
        9.删除条目为0条
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
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0022开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_user_permission(self):
        # 创建分区表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists test_policy3;
       create table test_policy3(c_id int, c_usr varchar(20)	)WITH (ORIENTATION = COLUMN,COMPRESSION=MIDDLE)
       PARTITION BY RANGE (c_id)
       (
	    partition P_max values less than (maxvalue)
        );''')
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
        sql_cmd3 = commonsh.execut_db_sql('''insert into test_policy3 values(60,'u_usr1'),(150,'u_usr2'),(40,'u_usr3');''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd3)
        # 授予用户表的select和delete权限并打开行级安全检查
        sql_cmd4 = commonsh.execut_db_sql('''grant select,delete on test_policy3 to u_usr1,u_usr2,u_usr3;
                                       ALTER TABLE test_policy3 ENABLE ROW LEVEL SECURITY;''')
        logger.info(sql_cmd4)
        self.assertIn(self.Constant.GRANT_SUCCESS_MSG, sql_cmd4)
        self.assertIn(self.Constant.ALTER_TABLE_MSG, sql_cmd4)
        # 创建策略,指定行访问控制影响的数据库用户为public
        sql_cmd5 = commonsh.execut_db_sql('''drop POLICY if exists t_pol1 ON test_policy3;
                                      CREATE POLICY t_pol1 ON test_policy3 FOR delete TO PUBLIC USING (c_usr = current_user);''')
        logger.info(sql_cmd5)
        self.assertIn(self.Constant.CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG, sql_cmd5)
        # 以u_usr1用户登录，系统管理员可以看到所有的行和字段
        sql_cmd6 = ('''select * from test_policy3;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U u_usr1 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd6}"
                            '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('u_usr2', msg1)
        # 以u_usr2用户登录，u_usr2用户修改c_usr自身字段，合理报错
        # 以u_usr2用户登录，u_usr2用户删除u_usr2信息，删除条目为1条
        # 以u_usr2用户登录，u_usr2用户删除u_usr1信息，删除条目为0条
        sql_cmd7 = ('''update test_policy3 set c_usr = 'u_usr2new' where c_id = 150;
                    delete from test_policy3 where c_usr = 'u_usr2';
                    delete from test_policy2 where c_usr = 'u_usr1';''')
        excute_cmd1 = f'''
                                   source {self.DB_ENV_PATH};
                                   gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U u_usr2 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd7}"
                                   '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('ERROR:  permission denied for relation test_policy3', msg1)
        self.assertIn(self.Constant.DELETE_SUCCESS_MSG, msg1)
    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除行访问控制策略
        sql_cmd8 = commonsh.execut_db_sql('''drop POLICY if exists t_pol1 ON test_policy3;''')
        logger.info(sql_cmd8)
        # 删除表
        sql_cmd9 = commonsh.execut_db_sql('''drop table test_policy3;''')
        logger.info(sql_cmd9)
        # 删除用户
        sql_cmd10 = commonsh.execut_db_sql(f'''drop user if exists u_usr1 cascade;
                                      drop user if exists u_usr2 cascade;
                                      drop user if exists u_usr3 cascade;''')
        logger.info(sql_cmd10)
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0022执行结束--------------------------')






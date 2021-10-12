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
Case Name   : 行存表定义行访问控制策略，不打开行访问控制策略开关的情况下，行访问控制策略不生效
Description :
        1.创建行存表all_data
        2.创建用户
        3.插入数据
        4.将表all_data的读取权限赋予alice和bob用户并打开行访问控制策略开关
        5. 创建行访问控制策略
        6.切换至alice用户执行SELECT操作
        7.切换至bob用户执行SELECT操作
        8.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.插入成功
        4.赋予权限成功
        5. 创建行访问控制策略成功
        6.查询到表的所有信息
        7.查询到表的所有信息
        8.清理环境完成
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
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0007开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_user_permission(self):
        # 创建行存表all_data
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists all_data;
                                    CREATE TABLE all_data(id int, role varchar(100), data varchar(100)) with (ORIENTATION = ROW);''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 创建用户
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists alice cascade;
                                   CREATE user alice password '{macro.COMMON_PASSWD}';
                                   drop user if exists bob cascade;
                                   CREATE user bob password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG,  sql_cmd2)
        # 向表插入数据，包含不同用户数据信息
        sql_cmd3 = commonsh.execut_db_sql('''INSERT INTO all_data VALUES(1, 'alice', 'alice data');
                                       INSERT INTO all_data VALUES(2, 'bob', 'bob data');
                                       INSERT INTO all_data VALUES(3, 'peter', 'peter data');''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd3)
        # 将表all_data的读取权限赋予alice和bob用户
        sql_cmd4 = commonsh.execut_db_sql('''GRANT SELECT ON all_data TO alice, bob;''')
        logger.info(sql_cmd4)
        self.assertIn(constant.GRANT_SUCCESS_MSG, sql_cmd4)
        # 创建行访问控制策略，当前用户执行SELECT操作，有权限查询表的所有信息
        sql_cmd5 = commonsh.execut_db_sql('''drop POLICY if exists all_data_rls ON all_data cascade;
                                       CREATE ROW LEVEL SECURITY POLICY all_data_rls ON all_data USING(role = CURRENT_USER);
                                       SELECT * FROM all_data;''')
        logger.info(sql_cmd5)
        self.assertIn(self.Constant.CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG, sql_cmd5)
        self.assertIn('bob', sql_cmd5)
        # 切换至alice用户执行SELECT操作，行访问控制策略未生效，查询到表的所有信息
        sql_cmd6 = ('''SELECT * FROM all_data;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U alice -W '{macro.COMMON_PASSWD}' -c "{sql_cmd6}"
                            '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('peter', msg1)
        # 切换至bob用户执行SELECT操作，行访问控制策略未生效，查询到表的所有信息
        sql_cmd7 = ('''SELECT * FROM all_data;''')
        excute_cmd1 = f'''
                                    source {self.DB_ENV_PATH};
                                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U bob -W '{macro.COMMON_PASSWD}' -c "{sql_cmd7}"
                                    '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(excute_cmd1)
        logger.info(msg1)
        self.assertIn('alice', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除行访问控制策略
        sql_cmd8 = commonsh.execut_db_sql('''drop POLICY if exists all_data_rls ON all_data cascade;''')
        logger.info(sql_cmd8)
        # 删除表
        sql_cmd9 = commonsh.execut_db_sql('''drop table all_data;''')
        logger.info(sql_cmd9)
        # 删除用户
        sql_cmd10 = commonsh.execut_db_sql('''drop user alice cascade;
                                    drop user bob cascade;''')
        logger.info(sql_cmd10)
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0007执行结束--------------------------')






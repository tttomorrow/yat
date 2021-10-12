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
Case Name   : 系统管理员执行ALTER ROW LEVEL SECURITY POLICY操作
Description :
        1.创建行存表all_data
        2.打开行访问控制策略开关并创建行访问控制策略
        3.创建系统管理员test_sys
        4.系统管理员执行ALTER ROW LEVEL SECURITY POLICY
        5.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.创建成功
        4.修改成功
        5.清理环境完成
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


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0001开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_sysadmin_user_permission(self):
        # 创建行存表all_data
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists all_data;
                                   CREATE TABLE all_data(id int, role varchar(100), data varchar(100)) with (ORIENTATION = ROW);''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 打开行访问控制策略开关并创建行访问控制策略
        sql_cmd2 = commonsh.execut_db_sql('''ALTER TABLE all_data ENABLE ROW LEVEL SECURITY;
                                      drop POLICY if exists all_data_rls ON all_data cascade;
                                      CREATE ROW LEVEL SECURITY POLICY all_data_rls ON all_data USING(role = CURRENT_USER);''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.ALTER_TABLE_MSG, sql_cmd2)
        self.assertIn(self.Constant.CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG,  sql_cmd2)
        # 创建系统管理员test_sys
        sql_cmd3 = commonsh.execut_db_sql(f'''drop user if exists test_sys cascade;
                                    CREATE user test_sys with sysadmin password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd3)

        # 系统管理员执行ALTER ROW LEVEL SECURITY POLICY
        sql_cmd4 = ('''ALTER ROW LEVEL SECURITY POLICY all_data_rls ON all_data RENAME TO all_data_new_rls;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_sys -W '{macro.COMMON_PASSWD}' -c "{sql_cmd4}"
                            '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.ALTER_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG, msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除行访问控制策略
        sql_cmd5 = commonsh.execut_db_sql('''drop POLICY all_data_new_rls ON all_data cascade;''')
        logger.info(sql_cmd5)
        # 删除表
        sql_cmd6 = commonsh.execut_db_sql('''drop table if exists all_data;''')
        logger.info(sql_cmd6)
        # 删除用户
        sql_cmd7 = commonsh.execut_db_sql(f'''drop user if exists test_sys cascade;''')
        logger.info(sql_cmd7)
        logger.info('------------------------Opengauss_Function_DDL_Policy_Case0001执行结束--------------------------')






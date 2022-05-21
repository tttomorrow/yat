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
Case Name   : 普通用户删除行访问控制策略，合理报错
Description :
        1.创建行存表all_data
        2.创建测试用户
        3.打开行访问控制策略开关并创建行访问控制策略
        4.创建普通用户test_com
        5.删除行访问控制策略，添加ROW LEVEL SECURITY选项
        6.删除不存在的行访问控制策略，添加ROW LEVEL SECURITY选项以及if exists
        7.清理环境
Expect      :
        1.创建成功
        2.创建测试用户成功
        3.打开行访问控制策略开关并创建行访问控制策略成功
        4.创建普通用户test_com成功
        5.合理报错
        6.合理报错
        7.清理环境完成
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
        logger.info('------------------------Opengauss_BaseFunc_DDL_DROP_ROW_LEVEL_SECURITY_POLICY_0002开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_user_permission(self):
        # 创建行存表all_data
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists all_data;
                                   CREATE TABLE all_data(id int, role varchar(100), data varchar(100)) with (ORIENTATION = ROW);''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        # 创建测试用户
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists alice cascade;
                                      create user alice password '{macro.COMMON_PASSWD}';
                                      drop user if exists bob cascade;
                                    create user bob password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        # 打开行访问控制策略开关并创建行访问控制策略
        sql_cmd3 = commonsh.execut_db_sql('''ALTER TABLE all_data ENABLE ROW LEVEL SECURITY;
                                      drop POLICY if exists all_data_rls ON all_data cascade;
                                      CREATE ROW LEVEL SECURITY POLICY all_data_rls ON all_data to alice,bob USING(role = CURRENT_USER);''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.ALTER_TABLE_MSG, sql_cmd3)
        self.assertIn(self.Constant.CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG,  sql_cmd3)
        # 创建普通用户test_com
        sql_cmd4 = commonsh.execut_db_sql(f'''drop user if exists test_com cascade;
                                      CREATE user test_com password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd4)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd4)

        # 删除行访问控制策略，添加ROW LEVEL SECURITY选项,合理报错
        sql_cmd5 = ('''  drop ROW LEVEL SECURITY POLICY all_data_rls ON all_data;''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_com -W '{macro.COMMON_PASSWD}' -c "{sql_cmd5}"
                            '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  must be owner of relation all_data', msg1)
        # 删除不存在的行访问控制策略，添加ROW LEVEL SECURITY选项以及if exists,合理报错
        sql_cmd6 = (''' drop ROW LEVEL SECURITY POLICY if exists all_data_rls ON all_data;''')
        excute_cmd1 = f'''
                                    source {self.DB_ENV_PATH};
                                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_com -W '{macro.COMMON_PASSWD}' -c "{sql_cmd6}"
                                    '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  must be owner of relation all_data', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 所有者删除行访问控制策略，删除成功
        sql_cmd7 = commonsh.execut_db_sql('''drop ROW LEVEL SECURITY POLICY all_data_rls ON all_data RESTRICT;''')
        logger.info(sql_cmd7)
        # 删除表
        sql_cmd8 = commonsh.execut_db_sql('''drop table all_data;''')
        logger.info(sql_cmd8)
        # 删除用户
        sql_cmd9 = commonsh.execut_db_sql(f'''drop user if exists alice cascade;
                                       drop user if exists bob cascade;
                                       drop user if exists test_com cascade;''')
        logger.info(sql_cmd9)
        logger.info('------------------------Opengauss_BaseFunc_DDL_DROP_ROW_LEVEL_SECURITY_POLICY_0002执行结束--------------------------')






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
Case Type   : 系统操作
Case Name   : 普通用户执行vacuum操作，无权限，合理报错
Description :
        1.建表并插入数据
        2.创建用户
        3.普通用户pt执行vacuum操作
        4.清理环境
Expect      :
        1.创建成功
        2.创建用户成功
        3.发出一个WARNING
        4.清理环境完成
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

class SYS_Operation(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Set_Case0117开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_vacuum_user_permission(self):
        # 建表并插入数据
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists customer_info;
       CREATE TABLE customer_info(WR_RETURNED_DATE_SK INTEGER ,WR_RETURNED_TIME_name varchar(200));
       insert into customer_info values (generate_series(1,2000),'a');''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(self.Constant.INSERT_SUCCESS_MSG, sql_cmd1)
        # 创建用户
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists test_pt cascade;
                                       create user test_pt password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        # 普通用户pt执行vacuum操作，发出一个WARNING，WARNING:  skipping "customer_info" --- only table or database owner can vacuum it
        sql_cmd3 = '''vacuum full analyze customer_info;
        vacuum freeze analyze customer_info;
        vacuum full freeze customer_info;'''
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                    gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U test_pt -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}"
                    '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.VACUUM_SUCCESS_MSG, msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd4 = commonsh.execut_db_sql('''drop table customer_info;''')
        logger.info(sql_cmd4)
        # 删除用户
        sql_cmd5 = commonsh.execut_db_sql('''drop user test_pt cascade;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DML_Set_Case0117执行结束--------------------------')






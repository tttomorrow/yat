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
Case Type   :数据源
Case Name   : 修改Data Source的权限测试（sysadmin用户）
Description :
        1.创建系统管理员用户
        2.创建数据源对象
        3.系统管理员执行alter语句
        4.清理环境
Expect      :
        1.创建成功
        2.创建数据源对象成功
        3.修改成功
        4.清理环境完成
History     :
"""
import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class DataSource(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Alter_DataSource_Case0014开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('dbuser')
        self.Constant = Constant()

    def test_user_permission(self):
        # 创建系统管理员用户
        sql_cmd1 = commonsh.execut_db_sql(f'''drop user if exists sys_test cascade;
                                       create user sys_test with sysadmin password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)
        # 创建数据源
        sql_cmd2 = commonsh.execut_db_sql('''DROP DATA SOURCE if exists ds_test12;
                                      CREATE DATA SOURCE ds_test12;''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_DATA_SOURCE_SUCCESS_MSG, sql_cmd2)

        # 系统管理员执行alter语句
        sql_cmd3 = ('''ALTER DATA SOURCE ds_test12 TYPE 'MPPDB_TYPE';''')
        excute_cmd1 = f'''
                            source {self.DB_ENV_PATH};
                            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U sys_test -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}"
                            '''
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.ALTER_DATA_SOURCE_SUCCESS_MSG, msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除数据源对象
        sql_cmd4 = commonsh.execut_db_sql('''DROP DATA SOURCE ds_test12;''')
        logger.info(sql_cmd4)
        # 删除用户
        sql_cmd5 = commonsh.execut_db_sql('''drop user sys_test cascade;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DDL_Alter_DataSource_Case0014执行结束--------------------------')






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
Case Type   : 自定义数据类型
Case Name   : sysadmin用户删除自定义类型
Description :
        1.创建数据类型
        2.创建系统管理员
        3.系统管理员删除自定义数据类型,添加RESTRICT选项
Expect      :
        1.创建成功
        2.创建成功
        3.删除成功
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

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0012开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('dbuser')
        self.Constant = Constant()


    def test_user_permission(self):
        # 创建数据类型
        sql_cmd1 = commonsh.execut_db_sql('''drop type if exists t_type1 cascade;
                                       CREATE TYPE t_type1 AS (f1 int, f2 DECIMAL(10,4));''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.CREATE_TYPE_SUCCESS_MSG, sql_cmd1)
        # 创建系统管理员
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists ta_sysadmin cascade;
                                     CREATE user ta_sysadmin with sysadmin password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        # 系统管理员删除自定义数据类型,添加RESTRICT选项，删除成功
        sql_cmd3 = ('''drop type t_type1 RESTRICT;''')
        excute_cmd1 = f'''
                                        source {self.DB_ENV_PATH};
                                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U ta_sysadmin -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}"
                                       '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.DROP_TYPE_SUCCESS_MSG, msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql(f'''drop user if exists ta_sysadmin cascade;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0012执行结束--------------------------')






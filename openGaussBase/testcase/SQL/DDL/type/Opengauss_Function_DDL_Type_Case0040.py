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
Case Type   : 修改类型
Case Name   : 普通用户执行ALTER TYPE，合理报错
Description :
        1.创建数据类型
        2.创建用户
        3.t_user1用户执行ALTER TYPE
        4.删除类型和用户
Expect      :
        1.创建数据类型成功
        2.创建用户成功
        3.合理报错
        4.删除成功
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

class AlterType(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0040开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.sh_primy = CommonSH('dbuser')

    def test_common_user_permission(self):
        # 创建数据类型
        sql_cmd1 = commonsh.execut_db_sql('''drop type if exists bugstatus3 cascade;
                                       CREATE TYPE bugstatus3 AS ENUM ('create', 'modify', 'closed');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_TYPE_SUCCESS_MSG, sql_cmd1)
        # 创建用户
        sql_cmd2 = commonsh.execut_db_sql(f'''drop user if exists t1_user1 cascade;
                                       create user t1_user1 password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        # t_user1用户执行ALTER TYPE,合理报错
        sql_cmd3 = ('''ALTER TYPE bugstatus3 rename to new_bugstatus3;''')
        excute_cmd1 = f'''
                                        source {self.DB_ENV_PATH};
                                        gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U t1_user1 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}"
                                       '''
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn('ERROR:  permission denied for type bugstatus3', msg1)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除类型
        sql_cmd4 = commonsh.execut_db_sql('''drop type bugstatus3 cascade;''')
        logger.info(sql_cmd4)
        # 删除用户
        sql_cmd5 = commonsh.execut_db_sql('''drop user t1_user1 cascade;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0040执行结束--------------------------')






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
Case Type   : 系统操作
Case Name   : checkpoint权限测试,普通用户执行checkpoint，合理报错
Description :
        1.创建系统管理员
        2.调用checkpoint
        3.创建普通用户
        4.调用checkpoint
        5.清理环境
Expect      :
        1.创建系统管理员成功
        2.执行成功
        3.创建普通用户成功
        4.合理报错
        5.清理环境完成
History     :
"""
import os
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
        logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.user_01 = 'u_dml_set_0053_01'
        self.user_02 = 'u_dml_set_0053_02'

    def test_checkpoint(self):
        test = '-----step1:创建系统管理员 expect:成功-----'
        logger.info(test)
        sql_cmd1 = commonsh.execut_db_sql(
            f'''drop user if exists {self.user_01} cascade;
        create user {self.user_01} with sysadmin 
        password '{macro.COMMON_PASSWD}'; ''')
        logger.info(sql_cmd1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1,
                      '执行失败:' + test)

        test = '-----step2:调用checkpoint expect:成功-----'
        logger.info(test)
        sql_cmd2 = 'checkpoint;'
        excute_cmd1 = f"source {self.DB_ENV_PATH};" \
            f"gsql -d {self.userNode.db_name} " \
            f"-p {self.userNode.db_port} " \
            f"-U {self.user_01} -W '{macro.COMMON_PASSWD}' " \
            f"-c '{sql_cmd2}'"
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(self.Constant.CHECKPOINT_SUCCESS_MSG, msg1,
                      '执行失败:' + test)

        test = '-----step3:创建普通用户 expect:成功-----'
        logger.info(test)
        sql_cmd3 = commonsh.execut_db_sql(
            f'''drop user if exists {self.user_02} cascade;
        create user {self.user_02} password '{macro.COMMON_PASSWD}'; ''')
        logger.info(sql_cmd3)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd3,
                      '执行失败:' + test)

        test = '-----step4:调用checkpoint expect:合理报错-----'
        logger.info(test)
        sql_cmd4 = 'checkpoint;'
        excute_cmd1 = f"source {self.DB_ENV_PATH};" \
            f"gsql -d {self.userNode.db_name} " \
            f"-p {self.userNode.db_port} " \
            f"-U {self.user_02} -W '{macro.COMMON_PASSWD}' " \
            f"-c '{sql_cmd2}'"
        logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(
            'ERROR:  must be system admin or operator admin to do CHECKPOINT',
            msg1, '执行失败:' + test)

    def tearDown(self):
        logger.info('-----step5:清理环境-----')
        test = '-----删除用户 expect:成功-----'
        logger.info(test)
        sql_cmd5 = commonsh.execut_db_sql(
            f'''drop user if exists {self.user_01} cascade;
        drop user if exists {self.user_02} cascade;''')
        logger.info(sql_cmd5)

        self.assertEqual(2,
                         sql_cmd5.count(self.Constant.DROP_ROLE_SUCCESS_MSG),
                         '执行失败:' + test)
        logger.info(f'-----{os.path.basename(__file__)} end-----')

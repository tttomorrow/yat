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
Case Type   : 功能测试
Case Name   : 有管理员权限:修改internal类型
Description :
    1.管理员用户登录，show如下参数 期望:显示成功
    2.管理员用户登录，修改如下参数 期望:修改失败，报错无权限，参数未被修改
    错误提示:ERROR:  unsupport parameter
    ALTER SYSTEM SET only support POSTMASTER-level, SIGHUP-level and BACKEND-level guc variable,
    and it must be allowed to set in postgresql.conf.
    3.清理环境
    no need to clean
Expect      : 
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


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info(
            '------------------------Opengauss_Function_Alter_System_Set_Case0006开始执行-----------------------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_common_user_permission(self):
        logger.info(
            '-----------------------------------------管理员用户登录，show如下参数 期望:显示成功-----------------------------------------')
        sql_cmd = self.commonsh.execut_db_sql('''
                                            show server_version;
                                            show  server_version_num;
                                            ''')
        logger.info(sql_cmd)
        result1 = sql_cmd

        logger.info('------------------------管理员用户登录，修改如下参数 期望:修改失败，报错无权限，参数未被修改-----------------------------')
        sql_cmd = self.commonsh.execut_db_sql('''
                                            ALTER SYSTEM SET server_version to '10.0.0';
                                            ALTER SYSTEM SET  server_version_num to '90909';
                                            ''')
        logger.info(sql_cmd)
        self.assertIn("SET", sql_cmd)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], sql_cmd)
        self.assertIn("unsupport parameter", sql_cmd)

        logger.info('-----------------------------管理员用户登录，show如下参数 期望:显示成功,参数未被修改-------------------------------------')
        sql_cmd = self.commonsh.execut_db_sql('''
                                            show server_version;
                                            show  server_version_num;
                                            ''')
        logger.info(sql_cmd)
        result2 = sql_cmd
        self.assertEqual(result1, result2)

    def tearDown(self):
        logger.info(
            '------------------------------------------this is teardown-------------------------------------------')
        logger.info(
            '-------------------------------------------no need to clean------------------------------------------')
        logger.info(
            '------------------------Opengauss_Function_Alter_System_Set_Case0006执行结束--------------------------')

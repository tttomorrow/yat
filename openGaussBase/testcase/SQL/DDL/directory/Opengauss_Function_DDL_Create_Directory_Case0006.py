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
Case Type   : 用户-权限测试
Case Name   : 非初始用户（sysadmin用户）创建目录对象
             (修改参数enable_access_server_directory为on)
Description :
    1.修改参数enable_access_server_directory为on
    2.创建系统管理员
    3.系统管理员创建目录对象
    4.删除用户和用户
    5.恢复参数默认值
Expect      :
    1.修改成功
    2.创建系统管理员成功
    3.创建成功
    4.删除成功
    5.设置成功
History     :
"""
import time
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class DIRECTORY(unittest.TestCase):
    def setUp(self):
        logger.info(
            '---Opengauss_Function_DDL_Create_Directory_Case0006开始执行----')
        self.user_node = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH

    def test_common_user_permission(self):
        # 修改参数enable_access_server_directory为on
        sql_cmd1 = commonsh.execut_db_sql(
            '''ALTER SYSTEM SET enable_access_server_directory to on;''')
        logger.info(sql_cmd1)
        self.assertIn('ALTER SYSTEM SET', sql_cmd1)
        time.sleep(5)
        # 创建系统管理员
        sql_cmd2 = commonsh.execut_db_sql(f'''
        drop user if exists test_sys;
       create user test_sys with sysadmin password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        # 系统管理员创建目录对象，成功
        sql_cmd3 = ('''DROP DIRECTORY if exists test_dir;
                     create DIRECTORY test_dir as '/tmp/';''')
        excute_cmd1 = f'''
                    source {self.DB_ENV_PATH};
                gsql -d {self.user_node.db_name} -p {self.user_node.db_port} \
-U test_sys -W '{macro.COMMON_PASSWD}' -c "{sql_cmd3}"
                            '''
        msg1 = self.user_node.sh(excute_cmd1).result()
        logger.info(msg1)
        self.assertIn(constant.CREATE_DIRECTORY_SUCCESS_MSG, msg1)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''
        DROP DIRECTORY test_dir;
        drop user test_sys cascade;''')
        logger.info(sql_cmd4)
        # 恢复参数默认值
        sql_cmd6 = commonsh.execut_db_sql(
            '''ALTER SYSTEM SET enable_access_server_directory to off;''')
        logger.info(sql_cmd6)
        logger.info(
            '---Opengauss_Function_DDL_Create_Directory_Case0006执行结束----')

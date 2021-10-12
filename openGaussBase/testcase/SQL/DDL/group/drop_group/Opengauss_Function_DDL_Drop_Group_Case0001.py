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
'''
--  @date:2020/10/12
--  @testpoint:删除用户组测试
'''
import unittest

from yat.test import macro

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Drop_Group_Case0001开始执行-----------------------------')

    def test_group(self):
        # 创建用户组
        sql_cmd1 = commonsh.execut_db_sql(f'''drop group if exists test_group1a;
                                   create group test_group1a password '{macro.COMMON_PASSWD}';''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd1)

       # 删除用户组添加if exists,删除成功
        sql_cmd2 = commonsh.execut_db_sql('''drop group if exists test_group1a;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.DROP_ROLE_SUCCESS_MSG, sql_cmd2)

        # 删除不存在用户组，添加if exists，发出notice
        sql_cmd3 = commonsh.execut_db_sql('''select rolname from pg_authid where rolname = 'test_group9k';
                                      drop group if exists test_group9k;''')
        logger.info(sql_cmd3)
        self.assertIn('NOTICE:  role "test_group9k" does not exist', sql_cmd3)

        # 删除不存在用户组，省略if exists，合理报错
        sql_cmd4 = commonsh.execut_db_sql('''drop group test_group9k;''')
        logger.info(sql_cmd4)
        self.assertIn('ERROR:  role "test_group9k" does not exist', sql_cmd4)

    # 清理环境:no need to clean
    def tearDown(self):
        logger.info('----------this is teardown-------')
        logger.info('------------------------Opengauss_Function_DDL_Drop_Group_Case0001执行结束--------------------------')






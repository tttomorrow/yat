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
Case Type   :
Case Name   : 修改不存在的目录属主，合理报错
Description :
    1.查询是否存在test_dir2目录名
    2.创建系统管理员
    3.修改不存在的目录属主
    4.删除用户
Expect      :
    1.查询成功，不存在
    2.创建系统管理员成功
    3.修改不存在的目录属主，合理报错
    4.删除用户成功
History     :添加marco文件
"""
import unittest
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Alter_Directory_Case0003开始执行-----------------------------')

    def test_common_user_permission(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop DIRECTORY if exists test_dir2;
                                      select dirname,owner from PG_DIRECTORY where dirname = 'test_dir2';''')
        logger.info(sql_cmd1)
        self.assertIn('dirname', sql_cmd1)
        sql = f'''drop user if exists test_sys cascade;
                create user test_sys with sysadmin password '{macro.COMMON_PASSWD}';'''
        sql_cmd2 = commonsh.execut_db_sql(sql)
        logger.info(sql_cmd2)
        self.assertIn(constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd2)
        sql_cmd3 = commonsh.execut_db_sql('''ALTER DIRECTORY test_dir2 OWNER TO test_sys;''')
        logger.info(sql_cmd3)
        self.assertIn('ERROR:  directory "test_dir2" does not exist', sql_cmd3)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除用户
        sql_cmd7 = commonsh.execut_db_sql('''drop user test_sys cascade;''')
        logger.info(sql_cmd7)
        self.assertIn(constant.DROP_ROLE_SUCCESS_MSG, sql_cmd7)
        logger.info('------------------------Opengauss_Function_DDL_Alter_Directory_Case0003执行结束--------------------------')






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
'''
--  @testpoint:复合类型删除一个属性
'''
import sys
import unittest
sys.path.append(sys.path[0]+"/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH


logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()

class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0021开始执行-----------------------------')

    def test_common_user_permission(self):
        # 创建一种复合类型
        sql_cmd1 = commonsh.execut_db_sql('''drop type if exists test2_type cascade;
                                       create type test2_type as(a int,b text);''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_TYPE_SUCCESS_MSG, sql_cmd1)
        # 删除属性a，删除成功
        sql_cmd2 = commonsh.execut_db_sql('''ALTER TYPE test2_type DROP ATTRIBUTE a;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.ALTER_TYPE_SUCCESS_MSG, sql_cmd2)
        # 删除不存在的属性，添加if exists,发出notice
        sql_cmd3 = commonsh.execut_db_sql('''ALTER TYPE test2_type DROP ATTRIBUTE if exists a;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.ALTER_TYPE_SUCCESS_MSG, sql_cmd3)
        # 删除不存在的属性，省略if exists,合理报错
        sql_cmd4 = commonsh.execut_db_sql('''ALTER TYPE test2_type DROP ATTRIBUTE a;''')
        logger.info(sql_cmd4)
        self.assertIn('ERROR:  column "a" of relation "test2_type" does not exist', sql_cmd4)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除类型
        sql_cmd5 = commonsh.execut_db_sql('''drop type if exists test2_type cascade;''')
        logger.info(sql_cmd5)
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0021执行结束--------------------------')






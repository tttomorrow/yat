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
--  @testpoint:枚举类型增加一个新值，IF NOT EXISTS选项测试
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
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0033开始执行-----------------------------')

    def test_common_user_permission(self):
        # 创建枚举类型
        sql_cmd1 = commonsh.execut_db_sql('''drop type if exists bugstatus2 cascade;
                                       CREATE TYPE bugstatus2 AS ENUM ('create', 'modify', 'closed');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_TYPE_SUCCESS_MSG, sql_cmd1)
        # 为枚举类型增加一个新值，添加if not exists，添加成功
        sql_cmd2 = commonsh.execut_db_sql('''ALTER TYPE bugstatus2 ADD VALUE if not exists 'insert' BEFORE 'create';''')
        logger.info(sql_cmd2)
        self.assertIn(constant.ALTER_TYPE_SUCCESS_MSG, sql_cmd2)
        # 添加已经存在的标签值，抛出notice
        sql_cmd3 = commonsh.execut_db_sql('''ALTER TYPE bugstatus2 ADD VALUE if not exists 'closed' after 'create';''')
        logger.info(sql_cmd3)
        self.assertIn(constant.ALTER_TYPE_SUCCESS_MSG, sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除类型
        sql_cmd4 = commonsh.execut_db_sql('''drop type if exists bugstatus2 cascade;''')
        logger.info(sql_cmd4)
        logger.info('------------------------Opengauss_Function_DDL_Type_Case0033执行结束--------------------------')






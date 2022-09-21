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
Case Type   : dolphin
Case Name   : 恢复数据库
Description :
    1、查询当前数据库
    2、删除兼容b库并重新创建数据库
Expect      :
    1、成功
    2、成功
History     :
"""
 
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class CompatibilityTest02(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.common = Common()
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.constant = Constant()
        
    def test_dolphin(self):
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        text = '--step1:查询当前数据库;expect:成功--'
        self.log.info(text)
        sql_cmd = "select current_database();"
        self.log.info(sql_cmd)
        sql_res = self.sh_primary.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn(self.user_node.db_name, sql_res, '执行失败' + text)

    def tearDown(self):
        text = '----step2:删除兼容b库并重新创建数据库;expect:成功----'
        self.log.info(text)
        sql_cmd = f"drop database if exists {self.user_node.db_name};" \
                  f"create database {self.user_node.db_name};"
        self.log.info(sql_cmd)
        sql_res = self.sh_primary.execut_db_sql(sql_cmd, dbname='postgres')
        self.log.info(sql_res)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_res,
                      '执行失败' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

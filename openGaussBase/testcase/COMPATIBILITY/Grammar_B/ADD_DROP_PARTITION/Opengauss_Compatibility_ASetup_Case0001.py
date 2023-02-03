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
Case Type   : dolphin
Case Name   : 创建dolphin插件库
Description :
    1、创建b库
    2、b库下查询dolphin插件
Expect      :
    1、成功
    2、自动加载成功,无需手动创建
History     :
"""

import os
import unittest

from yat.test import Node
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class CompatibilityTest01(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.common = Common()
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.constant = Constant()

    def test_dolphin(self):
        self.log.info(f'----{os.path.basename(__file__)} start----')
        text = '----step1:创建和node.yml同名且兼容b库的数据库;expect:成功----'
        self.log.info(text)
        sql_cmd = f"drop database if exists {self.user_node.db_name};" \
                  f"create database {self.user_node.db_name} " \
                  f"dbcompatibility ='B';"
        self.log.info(sql_cmd)
        sql_res = self.sh_primary.execut_db_sql(sql_cmd, dbname='postgres')
        self.log.info(sql_res)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_res,
                      '执行失败' + text)

        text = '---step2:b库下查询dolphin插件;expect:自动加载成功,无需手动创建---'
        self.log.info(text)
        sql_cmd = "select extname from pg_extension where extname ='dolphin';"
        self.log.info(sql_cmd)
        sql_res = self.sh_primary.execut_db_sql(sql_cmd,
                                                dbname=self.user_node.db_name)
        self.log.info(sql_res)
        self.assertEqual('dolphin', sql_res.splitlines()[-2].strip(),
                         '执行失败' + text)

    def tearDown(self):
        self.log.info('--无须清理环境，待sql用例执行完后清理--')
        self.log.info(f'----{os.path.basename(__file__)} end-----')



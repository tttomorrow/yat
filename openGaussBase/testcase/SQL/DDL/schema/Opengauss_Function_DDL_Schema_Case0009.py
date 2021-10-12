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
Case Type   : 基础功能
Case Name   : 修改模式用户
Description :
    1.开启事务创建模式
    2.开启事务修改模式
    3.删除schema
Expect      :
    1.创建成功
    2.修改成功
    3.删除成功
History     :
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Ddlschema(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Schema_Case0009.py start--')
        self.db_primary_db_user = Node(node='PrimaryDbUser')
        self.constant = Constant()
        self.schema_name = 'schema_case009'

    def test_schema(self):
        self.log.info('----------------1.开启事务创建模式-----------------')
        sql = f"start transaction;create schema {self.schema_name};end;\dn"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)
        self.assertIn(self.schema_name, result)

        self.log.info('-------------2.开启事务修改模式---------------------')
        sql = f"start transaction;" \
            f"alter schema {self.schema_name} " \
            f"rename to {self.schema_name}_new;end;\dn"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_SCHEMA_SUCCESS_MSG, result)
        self.assertIn(f"{self.schema_name}_new", result)

        self.log.info('-------------3.开启事务删除模式---------------------')
        sql = f"start transaction;" \
            f"drop schema if exists {self.schema_name}_new;end;\dn"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.DROP_SCHEMA_SUCCESS_MSG, result)
        self.assertNotIn(f"{self.schema_name}", result)

    def tearDown(self):
        self.log.info('------------环境清理-----------')
        self.log.info('---------删除模式------')
        sql = f"drop schema if exists {self.schema_name} cascade;" \
            f"drop schema if exists {self.schema_name}_new cascade;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('--Opengauss_Function_DDL_Schema_Case0009.py finish-')

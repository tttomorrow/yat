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
Case Type   : 基础功能
Case Name   : 修改模式用户
Description :
    1.创建模式
    2.创建函数
    3.使用函数创建模式
    4.使用函数修改模式
    5.使用函数删除模式
Expect      :
    1.创建模式成功
    2.创建函数成功
    3.创建模式成功
    4.修改成功
    5.删除成功
History     :
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Ddlschema(unittest.TestCase):
    commonshpri = CommonSH('PrimaryDbUser')

    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_DDL_Schema_Case0008.py start--')
        self.constant = Constant()
        self.schema_name = 'schema_case008'

    def test_schema(self):
        self.log.info('----------------1.创建模式-----------------')
        sql = f"create schema {self.schema_name};"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_SCHEMA_SUCCESS_MSG, result)

        self.log.info('-------------2.创建函数---------------------')
        sql = f"CREATE OR REPLACE FUNCTION " \
            f"{self.schema_name}.create_schema() " \
            f"RETURNS integer AS \$\$        " \
            f"BEGIN" \
            f"                create schema {self.schema_name}_new;" \
            f"                RETURN 222; " \
            f"END;" \
            f"\$\$ LANGUAGE plpgsql;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, result)
        sql = f"CREATE OR REPLACE FUNCTION {self.schema_name}.alter_schema()" \
            f" RETURNS integer AS \$\$        " \
            f"BEGIN" \
            f"    alter schema {self.schema_name}_new rename " \
            f"to {self.schema_name}_new1;" \
            f"    RETURN 221; " \
            f"END;" \
            f"\$\$ LANGUAGE plpgsql;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, result)
        sql = f"CREATE OR REPLACE FUNCTION {self.schema_name}.drop_schema()" \
            f" RETURNS integer AS \$\$        " \
            f"BEGIN" \
            f"                drop schema {self.schema_name}_new1;" \
            f"                RETURN 220; " \
            f"END;" \
            f"\$\$ LANGUAGE plpgsql;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, result)

        self.log.info('----------3.使用函数创建模式----------')
        sql = f"select {self.schema_name}.create_schema();\dn"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('222', result)
        self.assertIn(f"{self.schema_name}_new", result)

        self.log.info('----------4.使用函数修改模式----------')
        sql = f"select {self.schema_name}.alter_schema();\dn"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('221', result)
        self.assertIn(f"{self.schema_name}_new1", result)

        self.log.info('----------5.使用函数删除模式----------')
        sql = f"select {self.schema_name}.drop_schema();\dn"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn('220', result)
        self.assertNotIn(f"{self.schema_name}_new", result)

    def tearDown(self):
        self.log.info('------------环境清理-----------')
        self.log.info('---------删除模式------')
        sql = f"drop schema if exists {self.schema_name} cascade;" \
            f"drop schema if exists {self.schema_name}_new cascade;" \
            f"drop schema if exists {self.schema_name}_new1 cascade;"
        result = self.commonshpri.execut_db_sql(sql)
        self.log.info(result)
        self.log.info('--Opengauss_Function_DDL_Schema_Case0008.py finish-')

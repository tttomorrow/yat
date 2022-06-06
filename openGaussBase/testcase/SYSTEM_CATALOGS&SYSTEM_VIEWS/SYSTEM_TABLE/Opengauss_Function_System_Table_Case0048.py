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
Case Type   : 系统表
Case Name   : 测试系统表PG_PROC字段与数据类型
Description :
    1.查看系统表PG_PROC的表结构
    2.该表字段与对应字段数据类型是否正确
Expect      :
    1.查看系统表PG_PROC的表结构成功
    2.该表字段与字段数据类型对应正确
History     :
    modified：2021/10/12 by 5318639 优化用例适配新代码
    modified：2022/1/10 by 5318639 优化用例适配新代码
"""

import sys
import unittest

from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH


class SystemTable(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '------Opengauss_Function_System_Table_Case0048start------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['proname', 'pronamespace', 'proowner', 'prolang',
                       'procost', 'prorows', 'provariadic',
                       'protransform', 'proisagg', 'proiswindow', 'prosecdef',
                       'proleakproof', 'proisstrict',
                       'proretset', 'provolatile', 'pronargs',
                       'pronargdefaults', 'prorettype', 'proargtypes',
                       'proallargtypes', 'proargmodes', 'proargnames',
                       'proargdefaults', 'prosrc', 'probin',
                       'proconfig', 'proacl', 'prodefaultargpos',
                       'fencedmode', 'proshippable', 'propackage',
                       'prokind', 'proargsrc', 'propackageid', 'proisprivate',
                       'proargtypesext', 'prodefaultargposext', 'allargtypes',
                       'allargtypesext'],
            'Type': ['name', 'oid', 'oid', 'oid', 'real', 'real', 'oid',
                     'regproc', 'boolean', 'boolean', 'boolean',
                     'boolean', 'boolean', 'boolean', '"char"', 'smallint',
                     'smallint', 'oid', 'oidvector', 'oid[]',
                     '"char"[]', 'text[]', 'pg_node_tree', 'text', 'text',
                     'text[]', 'aclitem[]', 'int2vector',
                     'boolean', 'boolean', 'boolean', '"char"', 'text', 'oid',
                     'boolean', 'oidvector_extend', 'int2vector_extend',
                     'oidvector', 'oidvector_extend']}

    def test_systable(self):
        text = '----------step1:查看表结构;expect:查看成功-------------'
        self.log.info(text)
        msg = self.comsh.execut_db_sql('\d PG_PROC')
        self.log.info(msg)
        result_dict = self.com.format_sql_result(msg)
        self.log.info(result_dict)
        text = '-----step2:查看表字段与对应字段数据类型是否正确;expect:对应正确------'
        self.log.info(text)
        del result_dict['Modifiers']
        self.assertDictEqual(self.expect_result_dict, result_dict,
                             '执行失败' + text)

    def tearDown(self):
        self.log.info(
            '-----Opengauss_Function_System_Table_Case0048finish-----')

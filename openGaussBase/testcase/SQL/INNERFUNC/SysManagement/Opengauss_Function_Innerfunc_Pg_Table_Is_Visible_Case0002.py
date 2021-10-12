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
Case Type   : 功能测试
Case Name   : 使用pg_table_is_visible函数查询表在搜索路径中所有可见表
Description :
    1. 在搜索路径中查找所有可见表
Expect      :
    1. 包含系统表及系统视图以及用户表
History     : 
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.commonsh = CommonSH('dbuser')
        self.log.info('''---
            Opengauss_Function_Innerfunc_Pg_Table_Is_Visible_Case0002开始---''')

    def test_scheme(self):
        self.log.info('''--------查询所有可见表--------''')
        cmd = '''select relname from pg_class 
            where pg_table_is_visible(oid) = 't';'''
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        res = msg.splitlines()
        # 系统表及系统视图可见
        sys_table = [table for table in res if table.startswith(' pg_')]
        sys_view = [view for view in res if view.startswith(' gs_')]
        self.assertTrue(len(sys_table) > 128)
        self.assertTrue(len(sys_view) > 30)

    def tearDown(self):
        self.log.info('''---
            Opengauss_Function_Innerfunc_Pg_Table_Is_Visible_Case0002结束---''')

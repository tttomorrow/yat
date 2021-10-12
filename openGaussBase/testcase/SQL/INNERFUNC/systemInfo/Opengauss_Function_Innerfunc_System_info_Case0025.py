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
Case Type   : 系统信息函数-模式可见性查询函数 
Case Name   : 使用函数pg_tablespace_databases()，查看获取在指定的表空间中有对象的数据库OID集合
Description :
    1.查看表空间的oid
    2.使用函数pg_tablespace_databases()，查看获取在指定的表空间中有对象的数据库OID集合
Expect      :
    1.查看表空间的oid成功
    2.使用函数pg_tablespace_databases()，查看获取在指定的表空间中有对象的数据库OID集合成功
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0025开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.查看表空间的oid')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select oid,spcname from pg_tablespace;')
        LOG.info(sql_cmd)
        self.assertIn('1663 | pg_default', sql_cmd)

        LOG.info(
            f'-步骤2.使用函数pg_tablespace_databases()，查看获取在指定的表空间中有对象的数据库OID集合')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select  pg_tablespace_databases(1663) limit 4;')
        LOG.info(sql_cmd)
        self.assertIn(f'4 rows', sql_cmd)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0025结束-')

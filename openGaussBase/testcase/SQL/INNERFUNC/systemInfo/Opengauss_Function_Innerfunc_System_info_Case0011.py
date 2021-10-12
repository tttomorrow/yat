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
Case Type   : 系统信息函数
Case Name   : pg_function_is_visible(function_oid)查看该函数是否在搜索路径中可见
Description :
    1.创建函数
    2.查看函数OID
    3.pg_function_is_visible(function_oid)查看该函数是否在搜索路径中可见
Expect      :
    1.创建函数成功
    2.查看函数OID成功
    3.查看该函数是否在搜索路径中可见成功，结果可见
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0011开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.创建函数')
        sql_cmd = self.commonsh.execut_db_sql(
            f'''create or replace procedure pro_test() is
                V1 BLOB;
                begin
                  IF V1 is NULL then
                  raise info 'V1 is NULL';
                  else
                  raise info 'V1 is not NULL';
                  end if;
                end;
            ''')
        LOG.info(sql_cmd)
        self.assertIn('CREATE PROCEDURE', sql_cmd)

        LOG.info('--步骤2.查看函数OID--')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select oid from PG_PROC where proname=\'pro_test\';')
        LOG.info(sql_cmd)
        oid = sql_cmd.split('\n')[2].strip()
        LOG.info(oid)

        LOG.info('--步骤3.pg_function_is_visible(function_oid)查看该函数是否在搜索路径中可见--')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_function_is_visible(\'{oid}\');')
        LOG.info(sql_cmd)
        self.assertIn('t', sql_cmd)

    def tearDown(self):
        LOG.info('-------清理环境-------')
        sql_cmd = self.commonsh.execut_db_sql(f'drop procedure pro_test;')
        LOG.info(sql_cmd)
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0011结束-')

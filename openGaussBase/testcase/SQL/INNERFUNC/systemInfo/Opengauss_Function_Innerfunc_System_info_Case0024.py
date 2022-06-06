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
Case Type   : 系统信息函数-模式可见性查询函数 
Case Name   :  使用函数pg_get_indexdef(index_oid) ，获取索引的CREATE INDEX命令
Description :
    1.查看索引的oid
    2.使用函数pg_get_indexdef(index_oid) ，获取索引的CREATE INDEX命令
Expect      :
    1.查看索引的oid成功
    2.使用函数pg_get_indexdef(index_oid) ，获取索引的CREATE INDEX命令成功
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0024开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.查看索引的oid')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select indexrelid from PG_INDEX limit 1;')
        LOG.info(sql_cmd)
        self.assertIn('2831', sql_cmd)

        LOG.info(f'-步骤2.使用函数pg_get_indexdef(index_oid) ，获取索引的CREATE INDEX命令')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_get_indexdef(2831);')
        LOG.info(sql_cmd)
        self.assertIn(f'CREATE UNIQUE INDEX pg_toast_2604_index '
                      f'ON pg_toast.pg_toast_2604 USING btree '
                      f'(chunk_id, chunk_seq) TABLESPACE pg_default',
                      sql_cmd)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0024结束-')

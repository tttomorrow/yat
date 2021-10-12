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
Case Name   : 使用函数pg_opfamily_is_visible(),查看该操作符族是否在搜索路径中可见
Description :
    1.查看操作符族的oid
    2.使用函数pg_opfamily_is_visible(),查看该操作符族是否在搜索路径中可见
Expect      :
    1.查看操作符族的oid成功
    2.使用函数pg_opfamily_is_visible(),查看该操作符族是否在搜索路径中可见成功
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0022开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.查看操作符族的oid')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select oid,opfname from  pg_opfamily limit 1;')
        LOG.info(sql_cmd)
        self.assertIn('421 | abstime_ops', sql_cmd)
        oid = int(sql_cmd.split('\n')[2].split('|')[0])
        LOG.info(oid)
        if oid >= 0:
            LOG.info('查看操作符族的oid成功')
        else:
            raise Exception('查看异常，请检查')

        LOG.info(f'-步骤2.使用函数pg_opfamily_is_visible(),查看该操作符族是否在搜索路径中可见')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select  pg_opfamily_is_visible({oid});')
        LOG.info(sql_cmd)
        self.assertIn('t', sql_cmd)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0022结束-')

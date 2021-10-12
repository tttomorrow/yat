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
Case Name   : 使用函数pg_tablespace_location() ，获取表空间所在的文件系统的路径
Description :
    1.创建表空间
    2.查看表空间oid
    3.使用函数pg_tablespace_location() ，获取表空间所在的文件系统的路径
    4.删除表空间
Expect      :
    1.创建表空间成功
    2.查看表空间oid成功
    3.使用函数pg_tablespace_location() ，获取表空间所在的文件系统的路径成功
    4.删除表空间成功
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0026开始-')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.创建表空间')
        sql_cmd = self.commonsh.execut_db_sql(
            f'create tablespace test_tbps relative '
            f'location \'test_1/test_2\';')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, sql_cmd)

        LOG.info(
            f'-步骤2.查看表空间oid')
        sql_cmd = self.commonsh.execut_db_sql(f'select oid,spcname '
                                              f'from pg_tablespace where'
                                              f' spcname=\'test_tbps\';')
        LOG.info(sql_cmd)
        oid = int(sql_cmd.split('\n')[2].split('|')[0])
        LOG.info(oid)
        if oid >= 0:
            LOG.info('查看排序规则的oid成功')
        else:
            raise Exception('查看异常，请检查')

        LOG.info(f'-步骤3.使用函数pg_tablespace_location() ，获取表空间所在的文件系统的路径')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_tablespace_location({oid});')
        LOG.info(sql_cmd)
        self.assertIn('test_1/test_2', sql_cmd)

    def tearDown(self):
        LOG.info(f'-步骤4.删除表空间')
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop tablespace test_tbps;')
        LOG.info(sql_cmd)
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0026结束-')

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
Case Type   : 系统管理函数-备份控制函数
Case Name   : 函数pg_xlogfile_name_offset() ,将事务日志的位置字符串转换为文件名并返回在文件中的字节偏移量
Description :
    1.获取当前日志写入位置
    2.将事务日志的位置字符串转换为文件名并返回在文件中的字节偏移量
Expect      :
    1.获取当前日志写入位置成功
    2.将事务日志的位置字符串转换为文件名并返回在文件中的字节偏移量成功
History     : 
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0015开始-')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info(f'--步骤1.获取当前日志写入位置--')
        sql_cmd = self.commonsh.execut_db_sql(f'select '
                                              f'pg_current_xlog_location();')
        LOG.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)
        text = sql_cmd.split('\n')[2].split()[0]
        LOG.info(text)
        self.assertIn('/', sql_cmd)
        LOG.info(f'--步骤2.将事务日志的位置字符串转换为文件名并返回在文件中的字节偏移量--')
        sql_cmd = self.commonsh.execut_db_sql(f'select '
                                              f'pg_xlogfile_name_'
                                              f'offset(\'{text}\');')
        LOG.info(sql_cmd)
        str1 = sql_cmd.split('\n')[2]
        LOG.info(str1)
        str2 = str1.split(',')
        LOG.info(len(str2))
        self.assertEqual(len(str2), 2)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0015结束-')

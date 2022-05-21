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
Case Type   : 统计信息函数
Case Name   : pg_stat_get_backend_start(integer)描述：给定服务器进程启动的时间，
            如果当前用户不是系统管理员或被查询的后端的用户，则返回NULL。
Description :
    1.给定服务器进程启动的时间，以系统用户执行
    2.重启数据库，再次执行函数，以系统用户执行
    3.给定服务器进程启动的时间，以非系统用户执行，结果为null
    4.清理环境
Expect      :
    1.给定服务器进程启动的时间，以系统用户执行
    2.重启数据库，再次执行函数，以系统用户执行
    3.给定服务器进程启动的时间，以非系统用户执行，结果为null
    4.清理环境
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_statistics_function_Case0075开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        self.log.info('-----步骤1.给定服务器进程启动的时间，以系统用户执行--')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_stat_get_backend_start(1);')
        self.log.info(sql_cmd)
        str1 = sql_cmd.split('\n')[-2]
        self.log.info(f'str1 = {str1}')
        list1 = str1.split(',')
        self.log.info(f'list1 = {list1}')
        str2 = list1[0]
        self.log.info(f'str2 = {str2}')
        str3 = str2.split('.')[0]
        self.log.info(f'str3 = {str3}')

        self.log.info('--步骤2.重启数据库，再次执行函数，以系统用户执行--')
        gsql_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t restart;'
        self.log.info(gsql_cmd)
        msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(msg)
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_stat_get_backend_start(1);')
        self.log.info(sql_cmd)
        str1_b = sql_cmd.split('\n')[-2]
        self.log.info(f'str1_b = {str1_b}')
        list2 = str1_b.split(',')
        self.log.info(f'list2 = {list2}')
        str2_b = list2[0]
        self.log.info(f'str2_b = {str2_b}')
        str3_b = str2_b.split('.')[0]
        self.log.info(f'str3_b = {str3_b}')
        self.assertTrue(f'{str3} < {str3_b}')

        self.log.info('-----步骤3.给定服务器进程启动的时间，以非系统用户执行，结果为null-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'Create user test identified by \'{macro.COMMON_PASSWD}\';')
        self.log.info(sql_cmd)
        sql_msg = f'source {macro.DB_ENV_PATH};' \
            f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
            f' -U  test ' \
            f'-W {macro.COMMON_PASSWD}' \
            f' -c "select pg_stat_get_backend_start(1);" '
        self.log.info(sql_msg)
        msg = self.dbuser.sh(sql_msg).result()
        self.log.info(msg)
        str4 = msg.split('\n')[-2]
        num = len(str4)
        self.log.info(num)
        self.assertEqual(1, num)

    def tearDown(self):
        self.log.info('-----步骤4.清理环境-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop user test;')
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_statistics_function_Case0075结束')

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
Case Type   : 系统管理函数
Case Name   : pg_postmaster_start_time() 返回服务器的启动时间
Description :
    1.重启数据库，并查看当前时间
    2.pg_postmaster_start_time() 返回服务器的启动时间
Expect      :
    1.重启数据库，并查看当前时间成功
    2.返回服务器启动时间成功
History     :
"""
import unittest
import time
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0009开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.重启数据库-')
        restrt = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t restart'
        LOG.info(restrt)
        check_msg = self.dbuser_node.sh(restrt).result()
        LOG.info(check_msg)
        time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        LOG.info(f'time1 = {time1}')

        LOG.info(f'-步骤2.pg_postmaster_start_time()函数查看数据库启动时间-')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_postmaster_start_time();')
        LOG.info(sql_cmd)
        time2 = sql_cmd.split('\n')[2].strip()
        LOG.info(time2)
        list1 = time2.split(',')
        LOG.info(f'list1 = {list1}')
        time3 = list1[0]
        LOG.info(f'time3 = {time3}')
        time4 = time3.split('.')[0]
        LOG.info(f'time4 = {time4}')
        self.assertTrue(f'{time1} > {time4}')

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0009结束-')

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
Case Name   : DBE_PERF.get_global_record_reset_time()描述：汇聚openGauss统计信息重置时间，
            查询该函数必须具有sysadmin权限。
Description :
    1.重启数据库，并查看当前时间
    2.get_global_record_reset_time()函数查看数据库启动时间
    3.查看当前时间及日期
    4.创建数据库,删除数据库，并查看删除数据库时间
Expect      :
    1.重启数据库，并查看当前时间成功
    2.get_global_record_reset_time()函数查看数据库启动时间成功
    3.查看当前时间及日期成功
    4.创建数据库,删除数据库，并查看删除数据库时间成功
History     :
"""

import unittest
import time
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Functions(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Innerfunc_System_Info_Case0095开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')
        self.constant = Constant()
        self.db_name = "db_system_Info_0095"

    def test_func_sys_info(self):
        text = "--step1:重启数据库并查看当前时间;expect:重启数据库并查看当前时间成功--"
        self.log.info(text)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.log.info(f'time1 = {time1}')

        text = "--step2:使用函数函数查看数据库启动时间;expect:查看成功--"
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'select dbe_perf.get_global_record_reset_time();')
        self.log.info(sql_cmd)
        time2 = sql_cmd.split('\n')[2].strip()
        self.log.info(f'time2 = {time2}')
        list1 = time2.split(',')
        self.log.info(f'list1 = {list1}')
        time3 = list1[1]
        self.log.info(f'time3 = {time3}')
        time4 = time3.split('.')[0]
        self.log.info(f'time4 = {time4}')
        self.assertTrue(time1 > time4, '执行失败:' + text)

        text = "--step3:查看当前日期及时间;expect:查看成功"
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'select sysdate;')
        self.log.info(sql_cmd)
        self.assertIn("sysdate", sql_cmd, '执行失败:' + text)
        time5 = sql_cmd.split('\n')[-2].strip()
        self.log.info(f'time5 = {time5}')

        text = "--step4:创建数据库,删除数据库，并查看删除数据库时间;expect:查看成功"
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'create database {self.db_name};'
            f'select pg_sleep(3);'
            f'drop database {self.db_name};'
            f'select dbe_perf.get_global_record_reset_time();')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        time6 = sql_cmd.split('\n')[-2].strip()
        self.log.info(f'time6 = {time6}')
        list1 = time6.split(',')
        self.log.info(f'list1 = {list1}')
        time7 = list1[1]
        self.log.info(f'time7 = {time7}')
        time8 = time7.split('.')[0]
        self.log.info(f'time8 = {time8}')
        time9 = time8[1:]
        self.log.info(f'time9 = {time9}')
        self.assertTrue(time5 < time9, '执行失败:' + text)

    def tearDown(self):
        self.log.info('-------无需清理环境-------')
        self.log.info('-Opengauss_Function_Innerfunc_System_Info_Case0095结束-')

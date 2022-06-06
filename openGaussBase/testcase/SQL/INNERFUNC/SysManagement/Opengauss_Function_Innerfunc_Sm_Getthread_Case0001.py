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
Case Type   : 功能测试
Case Name   : 使用pg_stat_get_thread()提供当前节点下所有线程的状态信息
Description :
    1. gsql连接数据库，查询gsql线程
    2. 函数错误调用
Expect      :
    1. 返回节点名称及线程信息
    2. 合理报错
History     : 
"""
import unittest
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.user = Node('dbuser')
        self.commonsh = CommonSH('dbuser')
        self.log.info('Opengauss_Function_Innerfunc_Sm_Getthread_Case0001开始')

    def test_get_thread(self):
        self.log.info('------------校验PG_OS_THREADS字段------------')
        title = ['node_name', 'pid', 'lwpid', 'thread_name', 'creation_time']
        func = 'select * from  pg_stat_get_thread();'
        msg0 = self.commonsh.execut_db_sql(func)
        self.log.info(msg0)
        head = list(map(lambda s: s.strip(), msg0.splitlines()[0].split('|')))
        self.log.info(f'函数返回结果的字段是：{head}')
        self.assertTrue(head == title)
        gsql1 = [line for line in msg0.splitlines() if 'gsql' in line][0]
        self.log.info(f'第一次gsql连接的线程信息是：{gsql1}')

        now = self.user.sh('date "+%Y-%m-%d %H:%M:%S"').result()
        cmd = 'select * from  pg_stat_get_thread();'
        msg = self.commonsh.execut_db_sql(cmd)
        self.log.info(msg)
        gsql2 = [line for line in msg.splitlines() if 'gsql' in line][0]
        self.log.info(f'第二次gsql连接的线程信息是：{gsql2}')

        self.assertTrue(gsql1 != gsql2)
        self.log.info('------------校验PG_OS_THREADS各字段类型------------')
        gsql = list(map(lambda s: s.strip(), gsql2.split('|')))
        self.assertTrue(0 < int(gsql[1]) < 9223372036854775807)  # bigint
        self.assertTrue(0 < int(gsql[2]) < 2147483647)  # integer
        gsql2_time = gsql[-1].strip()
        cmd2 = f"select '{now}'::timestamp - '{gsql2_time}'::timestamp;"
        msg2 = self.commonsh.execut_db_sql(cmd2)
        self.log.info(msg2)
        diff = msg2.splitlines()[-2].strip().strip('-')
        self.assertTrue(diff[:5] == '00:00')

    def tearDown(self):
        self.log.info('Opengauss_Function_Innerfunc_Sm_Getthread_Case0001结束')
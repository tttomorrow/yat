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
Case Name   : pg_cancel_backend向由pid标识的后端进程发送一个查询取消（SIGINT）信号
Description :
    1.查看一个活动的后端进程的PID
    2.由pid标识的后端进程发送一个查询取消（SIGINT）信号
Expect      :
     1.查看一个活动的后端进程的PID成功
    2.由pid标识的后端进程发送一个查询取消（SIGINT）信号成功
History     :
"""
import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from yat.test import macro

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0002开始执行-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info('---------步骤1.查看一个活动的后端进程的PID---------')
        sql_cmd = self.commonsh.execut_db_sql(f'select pid '
                                              f'from pg_stat_activity;')
        LOG.info(sql_cmd)
        self.assertIn('pid', sql_cmd)
        list1 = sql_cmd.split('\n')
        LOG.info(list1)
        pid = list1[-2]
        LOG.info(pid)
        LOG.info('---------步骤2.取消一个后端的当前查询---------')
        sql_cmd = f'select pg_cancel_backend({pid});'
        excute_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.dbuser_node.db_name} ' \
            f'-p {self.dbuser_node.db_port} -c "{sql_cmd}"'
        LOG.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn('t', sql_cmd)

    def tearDown(self):
        LOG.info('-----------------无需清理环境----------------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0002结束-')

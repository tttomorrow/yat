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
Case Type   : 系统管理函数-恢复控制函数（备机执行）
Case Name   : pg_last_xlog_receive_location() 描述：获取最后接收事务日志的位置并通过流复制将其同步到磁盘
Description :
    1.备机执行函数pg_last_xlog_receive_location()
    2.主机执行函数pg_last_xlog_receive_location()
Expect      :
    1.备机执行函数pg_last_xlog_receive_location(),获取成功
    2.主机执行函数pg_last_xlog_receive_location()，获取失败
History     : 
"""

import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(), '单机环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0019开始-')
        self.commonsh = CommonSH('Standby1DbUser')
        self.commonsh1 = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info(f'---步骤1.备机执行函数pg_last_xlog_receive_location(),获取成功---')
        sql_cmd1 = self.commonsh.execut_db_sql(f'select '
                                               f'pg_last_xlog_'
                                               f'receive_location();')
        LOG.info(sql_cmd1)
        list1 = sql_cmd1.split('\n')[2].split()
        LOG.info(list1)
        self.assertEqual(len(list1), 1)

        LOG.info(f'---步骤2.主机执行函数pg_last_xlog_receive_location()，获取失败---')
        sql_cmd2 = self.commonsh1.execut_db_sql(f'select '
                                                f'pg_last_xlog_'
                                                f'receive_location();')
        LOG.info(sql_cmd2)
        list2 = sql_cmd2.split('\n')[2]
        list3 = list2.split()
        LOG.info(list3)
        self.assertEqual(len(list3), 0)

    def tearDown(self):
        LOG.info('-----无需清理环境------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0019结束-')

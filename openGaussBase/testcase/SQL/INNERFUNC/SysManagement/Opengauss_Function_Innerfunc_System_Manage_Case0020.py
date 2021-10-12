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
Case Name   : 函数pg_last_xact_replay_timestamp()，获取最后一个事务在恢复时重放的时间戳
Description :
    1..主机准备数据，创建事务并rollback，获取最后一个事务在恢复时重放的时间戳
    2.备机执行函数pg_last_xact_replay_timestamp()，执行成功
Expect      :
    1.步骤1.主机准备数据，创建事务并rollback，获取最后一个事务在恢复时重放的时间戳，返回结果为空
    2.主机执行函数pg_last_xact_replay_timestamp()，返回事务在恢复时重放的时间戳成功
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
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0020开始-')
        self.commonsh = CommonSH('Standby1DbUser')
        self.commonsh1 = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info(f'---步骤1.主机准备数据，创建事务并rollback，获取最后一个事务在恢复时重放的时间戳---')
        sql_cmd1 = self.commonsh1.execut_db_sql(f'create table '
                                                f'test_func(id int);'
                                                f'insert into '
                                                f'test_func values(1);'
                                                f'start transaction;'
                                                f'insert into '
                                                f'test_func values(2);'
                                                f'select * from test_func;'
                                                f'rollback;'
                                                f'select pg_last_'
                                                f'xact_replay_timestamp();')
        LOG.info(sql_cmd1)
        list1 = sql_cmd1.split('\n')[13].split()
        LOG.info(list1)
        self.assertEqual(len(list1), 0)

        LOG.info(f'---步骤2.备机执行函数pg_last_xact_replay_timestamp()，执行成功---')
        sql_cmd2 = self.commonsh.execut_db_sql(f'select now();'
                                               f'select pg_last_'
                                               f'xact_replay_timestamp();')
        LOG.info(sql_cmd2)
        list2 = sql_cmd2.split('\n')[2]
        list3 = list2.split()[0]
        LOG.info(list3)
        list4 = sql_cmd2.split('\n')[7]
        list5 = list4.split()[0]
        LOG.info(list5)
        self.assertEqual(list3, list5)

    def tearDown(self):
        LOG.info('-----清理环境------')
        sql_cmd2 = self.commonsh1.execut_db_sql(f'drop table test_func;')
        LOG.info(sql_cmd2)
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0020结束-')

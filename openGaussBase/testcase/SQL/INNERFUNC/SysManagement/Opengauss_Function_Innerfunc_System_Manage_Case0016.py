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
Case Type   : 系统管理函数-其他函数
Case Name   : 函数pg_stat_get_data_senders()，提供当前活跃的数据复制发送线程的详细信息
Description :
    1.查线程池状态是否开启
    2.开启线程池状态
    3.重启数据库
    4.查看当前活跃的数据复制发送线程的详细信息
    5.关闭线程池状态
    6.重启数据库
Expect      :
    1.查线程池状态是否开启成功
    2.开启线程池状态成功
    3.重启数据库成功
    4.查看当前活跃的数据复制发送线程的详细信息成功
    5.关闭线程池状态成功
    6.重启数据库成功
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0016开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info(f'-----步骤1.查线程池状态是否开启-----')
        sql_cmd = self.commonsh.execut_db_sql(f'show enable_thread_pool;')
        LOG.info(sql_cmd)
        self.assertIn('off', sql_cmd)

        LOG.info(f'-----步骤2.开启线程池状态-----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc set -D {macro.DB_INSTANCE_PATH}  -c "enable_thread_pool=on"
        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('Success to perform gs_guc!', msg)

        LOG.info('-----步骤3.重启数据库------')
        stopmsg = self.commonsh.stop_db_cluster()
        LOG.info(stopmsg)
        startmsg = self.commonsh.start_db_cluster()
        LOG.info(startmsg)

        LOG.info(f'--步骤4.查看当前活跃的数据复制发送线程的详细信息--')
        sql_cmd = self.commonsh.execut_db_sql(f' select '
                                              f'threadpool_status();')
        LOG.info(sql_cmd)
        list1 = sql_cmd.split('\n')[2]
        list2 = list1.split(',')
        LOG.info(list2)
        LOG.info(len(list2))
        self.assertEqual(len(list2), 8)

        LOG.info(f'-----步骤5.关闭线程池状态-----')
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc set -D {macro.DB_INSTANCE_PATH}  -c "enable_thread_pool=off"
        '''
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('Success to perform gs_guc!', msg)

    def tearDown(self):
        LOG.info('-----步骤6.重启数据库------')
        stopmsg = self.commonsh.stop_db_cluster()
        LOG.info(stopmsg)
        startmsg = self.commonsh.start_db_cluster()
        LOG.info(startmsg)
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0016结束-')

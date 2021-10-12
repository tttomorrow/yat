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
Case Type   : 统计信息函数
Case Name   : DBE_PERF.global_threadpool_status()描述：显示在所有节点上的线程池
    中工作线程及会话的状态信息。函数返回信息具体字段GLOBAL_THREADPOOL_STATUS字段。
Description :
    1.查线程池状态是否开启
    2.开启线程池状态
    3.重启数据库
    4.显示在所有节点上的线程池中工作线程及会话的状态信息，以系统用户执行
    5.汇聚所有节点数据文件IO的统计信息，以非系统用户执行
    6.恢复环境
Expect      :
    1.查线程池状态是否开启成功
    2.开启线程池状态成功
    3.重启数据库成功
    4.显示在所有节点上的线程池中工作线程及会话的状态信息，以系统用户执行成功
    5.汇聚所有节点数据文件IO的统计信息，以非系统用户执行，合理失败
    6.恢复环境成功
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
        self.log.info('Opengauss_Function_statistics_function_Case0018开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        self.log.info(f'-----步骤1.查线程池状态是否开启-----')
        sql_cmd = self.commonsh.execut_db_sql(f'show enable_thread_pool;')
        self.log.info(sql_cmd)
        self.assertIn('off', sql_cmd)

        self.log.info(f'-----步骤2.开启线程池状态-----')
        gsql_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc set -D {macro.DB_INSTANCE_PATH}  -c "enable_thread_pool=on"
        '''
        self.log.info(gsql_cmd)
        msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(msg)
        self.assertIn('Success to perform gs_guc!', msg)

        self.log.info('-----步骤3.重启数据库------')
        stopmsg = self.commonsh.stop_db_cluster()
        self.log.info(stopmsg)
        startmsg = self.commonsh.start_db_cluster()
        self.log.info(startmsg)

        self.log.info('-----步骤4.显示在所有节点上的线程池中工作线程及会话的状态信息，以系统用户执行-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select DBE_PERF.get_global_rel_iostat();')
        self.log.info(sql_cmd)
        str_info = sql_cmd.split('\n')[-2]
        self.log.info(f'str_info = {str_info}')
        num = len(str_info.split(','))
        self.log.info(f'num = {num}')
        if num == 5:
            self.log.info('汇聚所有节点数据文件IO的统计信息成功')
        else:
            raise Exception('函数执行异常，请检查')

        self.log.info("-----步骤5.汇聚所有节点数据文件IO的统计信息，以非系统用户执行-----")
        gsql_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -p {self.dbuser.db_port} -d ' \
            f'{self.dbuser.db_name} -U ' \
            f'{self.dbuser.db_user} -W {self.dbuser.db_password}' \
            f' -c "select DBE_PERF.get_global_rel_iostat();" '
        self.log.info(gsql_cmd)
        msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(msg)
        self.assertIn('ERROR:  permission denied for schema dbe_perf', msg)

    def tearDown(self):
        self.log.info('-----步骤6.------')
        gsql_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc set -D {macro.DB_INSTANCE_PATH}  -c "enable_thread_pool=off";
        gs_om -t restart;
        '''
        self.log.info(gsql_cmd)
        msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(msg)
        self.log.info('Opengauss_Function_statistics_function_Case0018结束')

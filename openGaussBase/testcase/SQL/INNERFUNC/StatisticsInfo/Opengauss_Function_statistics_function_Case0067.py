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
Case Name   : DBE_PERF.get_global_session_stat()描述：获取openGauss节点上的
            会话状态信息，查询该函数必须具有sysadmin权限。
Description :
    1.获取openGauss节点上的会话状态信息，以系统管理员执行
    2.当未开启线程池（enable_thread_pool = off）时，统计查询结果
    3.当开启线程池（enable_thread_pool = on）时，统计查询结果
    4.获取openGauss节点上的会话状态信息，以非系统管理员执行
    5.恢复环境
Expect      :
    1.获取openGauss节点上的会话状态信息，以系统管理员执行
    2.当未开启线程池（enable_thread_pool = off）时，统计查询结果，查询成功
    3.当开启线程池（enable_thread_pool = on）时，统计查询结果，
    所有的线程和会话的内存使用情况查询成功
    4.获取openGauss节点上的会话状态信息，以非系统管理员执行，合理报错
    5.恢复环境成功
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
        self.log.info('Opengauss_Function_statistics_function_Case0067开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        self.log.info('-----步骤1.获取openGauss节点上的会话状态信息，以系统管理员执行-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select DBE_PERF.get_global_session_stat () limit 3;')
        self.log.info(sql_cmd)
        number = len(sql_cmd.splitlines())
        self.log.info(number)
        if number >= 3:
            str_info1 = sql_cmd.split('\n')[-2]
            self.log.info(str_info1)
            num = len(str_info1.split(','))
            self.log.info(f'num = {num}')
            if num == 6:
                self.log.info('获取openGauss节点上的会话状态信息成功')
            else:
                raise Exception('函数执行异常，请检查')

            self.log.info('-步骤2.当未开启线程池（enable_thread_pool = off）时，统计查询结果-')
            sql_cmd = self.commonsh.execut_db_sql(
                f'select count(*) from DBE_PERF.get_global_session_stat();')
            self.log.info(sql_cmd)
            str_info1 = sql_cmd.split('\n')[-2]
            self.log.info(str_info1)

            self.log.info('-步骤3.当开启线程池（enable_thread_pool = on）时，统计查询结果-')
            set_cmd = f'source {macro.DB_ENV_PATH};' \
                f'gs_guc set  -N all -D {macro.DB_INSTANCE_PATH} ' \
                f'-c "enable_thread_pool=on";' \
                f'gs_om -t restart;'
            self.log.info(set_cmd)
            restart_cmd = self.dbuser.sh(set_cmd).result()
            self.log.info(restart_cmd)
            self.assertIn('Successfully started.', restart_cmd)

            sql_cmd = self.commonsh.execut_db_sql(
                f'select count(*) from DBE_PERF.get_global_session_stat();')
            self.log.info(sql_cmd)
            str_info3 = sql_cmd.split('\n')[-2]
            self.log.info(str_info3)
            self.assertTrue(str_info1 < str_info3)

            self.log.info("---步骤4.获取openGauss节点上的会话状态信息，以非系统管理员执行---")
            sql_msg = f'source {macro.DB_ENV_PATH};' \
                f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
                f' -U  {self.dbuser.db_user} ' \
                f'-W {self.dbuser.db_password}' \
                f' -c "select DBE_PERF.get_global_session_stat();" '
            self.log.info(sql_msg)
            msg = self.dbuser.sh(sql_msg).result()
            self.log.info(msg)
            self.assertIn('ERROR:  permission denied for schema dbe_perf', msg)
        else:
            raise Exception('函数执行异常，请检查')
        
    def tearDown(self):
        self.log.info('---步骤5.恢复环境---')
        restart_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc set  -N all -D {macro.DB_INSTANCE_PATH} ' \
            f'-c "enable_thread_pool=off";' \
            f'gs_om -t restart;' \
            f'gs_om -t status --detail; '
        self.log.info(restart_cmd)
        check_msg = self.dbuser.sh(restart_cmd).result()
        self.log.info(check_msg)
        self.log.info('Opengauss_Function_statistics_function_Case0067结束')

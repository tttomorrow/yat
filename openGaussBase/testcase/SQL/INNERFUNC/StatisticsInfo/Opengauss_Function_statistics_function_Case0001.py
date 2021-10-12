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
Case Name   : DBE_PERF.get_global_session_memory(),汇聚各节点的Session级别的内存使用情况，
            包含执行作业在数据节点上Postgres线程和Stream线程分配的所有内存，
            单位为MB，查询该函数必须具有sysadmin权限
Description :
    1.查看enable_memory_limit值,判断环境是否支持函数执行
    2.汇聚各节点的Session级别的内存使用情况,以系统用户执行
    3.汇聚各节点的Session级别的内存使用情况,以非系统用户执行
    4.恢复环境
Expect      :
    1.查看enable_memory_limit值,判断环境是否支持函数执行成功
    2.汇聚各节点的Session级别的内存使用情况,以系统用户执行成功
    3.汇聚各节点的Session级别的内存使用情况,以非系统用户执行，合理报错
    4.恢复环境成功
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
        self.log.info('Opengauss_Function_statistics_function_Case0001开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.log.info('--步骤1.查看enable_memory_limit值,判断环境是否支持函数执行--')
        excute_cmd = f''' source {macro.DB_ENV_PATH};gs_guc set -D \
        {macro.DB_INSTANCE_PATH} -c "enable_memory_limit=on"; 
        gs_om -t restart;
        '''
        self.log.info(excute_cmd)
        msg = self.dbuser.sh(excute_cmd).result()
        self.log.info(msg)
        sql_cmd = self.commonsh.execut_db_sql(
            f'show enable_memory_limit;')
        self.log.info(sql_cmd)
        if 'off' in sql_cmd:
            return '环境内存不支持此用例执行，故跳过'
        else:
            self.log.info('--步骤2.汇聚各节点的Session级别的内存使用情况,以系统用户执行--')
            sql_cmd = self.commonsh.execut_db_sql(
                f'show disable_memory_protect;')
            self.log.info(sql_cmd)
            check_cmd = f'''source {macro.DB_ENV_PATH};
                gs_guc reload -N all -I all -c "disable_memory_protect=on"
                 '''
            self.log.info(check_cmd)
            msg = self.dbuser.sh(check_cmd).result()
            self.log.info(msg)
            sql_cmd = self.commonsh.execut_db_sql(f'select DBE_PERF.'
                                                  f'get_global_session'
                                                  f'_memory();')
            self.log.info(sql_cmd)
            number = len(sql_cmd.splitlines())
            self.log.info(number)
            if number >= 3:
                list1 = sql_cmd.split('\n')[-2]
                self.log.info(list1)
                list2 = len(list1.split(','))
                self.log.info(list2)
                if list2 == 5:
                    self.log.info('汇聚各节点的Session级别的内存使用情况成功')
                else:
                    raise Exception('函数执行异常，请检查')
            else:
                check_cmd = f'''source {macro.DB_ENV_PATH};
                    gs_guc reload -N all -I all -c "disable_memory_protect=on"
                     '''
                self.log.info(check_cmd)
                msg = self.dbuser.sh(check_cmd).result()
                self.log.info(msg)

            self.log.info("--步骤3.汇聚各节点的Session级别的内存使用情况，以非系统用户执行--")
            check_cmd = f'''source {macro.DB_ENV_PATH};
                gsql -p {self.dbuser.db_port} \
                -d {self.dbuser.db_name} \
                -U {self.dbuser.db_user} -W {self.dbuser.db_password} -c "
                select DBE_PERF.get_global_session_memory();
                " '''
            self.log.info(check_cmd)
            msg = self.dbuser.sh(check_cmd).result()
            self.log.info(msg)
            self.assertIn('ERROR:  permission denied for '
                          'schema dbe_perf', msg)

    def tearDown(self):
        self.log.info("-----步骤4.恢复环境-------")
        check_cmd = f'''source {macro.DB_ENV_PATH};
        gs_guc reload -N all -I all -c "disable_memory_protect=off";
        '''
        self.log.info(check_cmd)
        msg = self.dbuser.sh(check_cmd).result()
        self.log.info(msg)
        self.log.info('Opengauss_Function_statistics_function_Case0001结束')

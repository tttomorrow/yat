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
Case Name   : DBE_PERF.get_global_memory_node_detail()描述：汇聚所有节点某个
    数据库节点内存使用情况，查询该函数必须具有sysadmin权限。
Description :
    1.查看enable_memory_limit值,判断环境是否支持函数执行
    2.汇聚所有节点某个数据库节点内存使用情况，以系统用户执行
    3.汇聚所有节点某个数据库节点内存使用情况，以非系统用户执行
Expect      :
    1.查看enable_memory_limit值,判断环境是否支持函数执行
    2.汇聚所有节点某个数据库节点内存使用情况，以系统用户执行成功
    3.汇聚所有节点某个数据库节点内存使用情况，以非系统用户执行，合理报错
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
        self.log.info('Opengauss_Function_statistics_function_Case0036开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        self.log.info('---步骤1.查看enable_memory_limit值,判断环境是否支持函数执行---')
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
            self.log.info('---步骤2.汇聚所有节点某个数据库节点内存使用情况，以系统用户执行---')
            sql_cmd = self.commonsh.execut_db_sql(
                f'set disable_memory_protect = on;'
                f'select DBE_PERF.get_global_memory_node_detail() limit 3;')
            self.log.info(sql_cmd)
            str_info = sql_cmd.split('\n')[-2]
            self.log.info(str_info)
            num = len(str_info.split(','))
            self.log.info(f'num = {num}')
            if num == 3:
                self.log.info('汇聚所有节点某个数据库节点内存使用情况成功')
            else:
                raise Exception('函数执行异常，请检查')

            self.log.info("---步骤3.汇聚所有节点某个数据库节点内存使用情况，以非系统用户执行---")
            gsql_cmd = f'source {macro.DB_ENV_PATH};' \
                f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
                f' -U  {self.dbuser.db_user} ' \
                f'-W {self.dbuser.db_password}' \
                f' -c "set set disable_memory_protect = on;' \
                f'select DBE_PERF.get_global_memory_node_detail();" '
            self.log.info(gsql_cmd)
            msg = self.dbuser.sh(gsql_cmd).result()
            self.log.info(msg)
            self.assertIn('ERROR:  permission denied for schema dbe_perf', msg)

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0036结束')

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
Case Name   : gs_total_nodegroup_memory_detail描述：返回当前数据库逻辑集群
    使用内存的信息，单位为MB得到一个逻辑集群。
Description :
    1.查看enable_memory_limit值,判断环境是否支持函数执行
    2.返回当前数据库逻辑集群使用内存的信息
Expect      :
    1.查看enable_memory_limit值,判断环境是否支持函数执行
    2.返回当前数据库逻辑集群使用内存的信息成功
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
        self.log.info('Opengauss_Function_statistics_function_Case0042开始')
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
            self.log.info('-----步骤2.返回当前数据库逻辑集群使用内存的信息-----')
            sql_cmd = self.commonsh.execut_db_sql(
                f'set disable_memory_protect = on;'
                f'select gs_total_nodegroup_memory_detail();')
            self.log.info(sql_cmd)
            str_info = sql_cmd.split('\n')[-2]
            self.log.info(str_info)
            num = len(str_info.split(','))
            self.log.info(f'num = {num}')
            if num == 3:
                self.log.info('汇聚各节点的命名空间中所有系统表索引的IO状态信息成功')
            else:
                raise Exception('函数执行异常，请检查')

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0042结束')

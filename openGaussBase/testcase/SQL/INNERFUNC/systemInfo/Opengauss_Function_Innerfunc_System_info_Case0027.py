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
Case Type   : 系统信息函数-模式可见性查询函数 
Case Name   : 使用函数pg_sequence_parameters(sequence_oid)，
              获取指定sequence的参数，包含起始值，最小值和最大值，递增值等
Description :
    1.查看序列的oid
    2.使用函数pg_sequence_parameters(sequence_oid)，
      获取指定sequence的参数，包含起始值，最小值和最大值，递增值等
Expect      :
    1.查看序列的oid成功
    2.使用函数pg_sequence_parameters(sequence_oid)，
      获取指定sequence的参数，包含起始值，最小值和最大值，递增值等成功
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0027开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    Primary_SH = CommonSH('PrimaryDbUser')

    @unittest.skipIf(1 == Primary_SH.get_node_num(), '单机环境不执行')
    def test_func_sys_info(self):
        LOG.info(f'-步骤1.查看序列的oid')
        sql_cmd1 = self.commonsh.execut_db_sql(
            f'select relid,relname,schemaname from pg_statio_user_sequences;')
        LOG.info(sql_cmd1)
        oid = int(sql_cmd1.split('\n')[2].split('|')[0])
        LOG.info(oid)
        if oid >= 0:
            LOG.info('查看排序规则的oid成功')
        else:
            raise Exception('查看异常，请检查')

        LOG.info(f'-步骤2.使用函数pg_sequence_parameters()，获取指定sequence的参数，'
                 f'包含起始值，最小值和最大值，递增值等')
        sql_cmd2 = self.commonsh.execut_db_sql(
            f'select pg_sequence_parameters({oid});')
        LOG.info(sql_cmd2)
        list1 = sql_cmd2.split('\n')[2]
        LOG.info(list)
        list2 = list1.split(',')
        self.assertEqual(len(list2), 5)

    def tearDown(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0027结束-')

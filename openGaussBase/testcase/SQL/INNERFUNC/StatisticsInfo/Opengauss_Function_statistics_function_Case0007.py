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
Case Name   : DBE_PERF.get_summary_workload_sql_count()描述：提供openGauss中
            不同负载SELECT，UPDATE，INSERT，DELETE，DDL， DML，DCL计数信息，
            查询该函数必须具有sysadmin权限
Description :
    1.查看openGauss中不同负载SELECT，UPDATE，INSERT，DELETE，DDL， DML，DCL计数信息，主节点执行
    2.以非系统用户执行
    3.查看openGauss中不同负载SELECT，UPDATE，INSERT，DELETE，DDL， DML，DCL计数信息，备节点执行
Expect      :
    1.查看openGauss中不同负载SELECT，UPDATE，INSERT，DELETE，DDL， DML，DCL计数信息，主节点执行，成功
    2.以非系统用户执行，合理报错
    3.查看openGauss中不同负载SELECT，UPDATE，INSERT，DELETE，DDL，
    DML，DCL计数信息，备节点执行，成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(
    '6002' not in Primary_SH.get_db_cluster_status('detail'),
    '单机环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_statistics_function_Case0007开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()
        self.commonsh1 = CommonSH('Standby1DbUser')

    def test_server_tools1(self):
        self.log.info('-----步骤1.查看openGauss中不同负载SELECT，'
                      'UPDATE，INSERT，DELETE，DDL，DML，DCL计数信息，主节点执行-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select DBE_PERF.get_summary_workload_sql_count();')
        self.log.info(sql_cmd)
        number = len(sql_cmd.splitlines())
        self.log.info(number)
        if number >= 3:
            list1 = sql_cmd.split('\n')[-2]
            self.log.info(list1)
            list2 = len(list1.split(','))
            self.log.info(list2)
            if list2 == 9:
                self.log.info('显示openGauss中不同负载技术信息成功')
            else:
                raise Exception('函数执行异常，请检查')
        else:
            raise Exception('执行结果异常，请检查')

        self.log.info("-----步骤2.以非系统用户执行-------")
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -p {self.dbuser.db_port} -d ' \
            f'{self.dbuser.db_name} -U ' \
            f'{self.dbuser.db_user} -W {self.dbuser.db_password}' \
            f' -c "select DBE_PERF.get_summary_workload_sql_count();" '
        self.log.info(check_cmd)
        msg = self.dbuser.sh(check_cmd).result()
        self.log.info(msg)
        self.assertIn('ERROR:  permission denied for schema dbe_perf', msg)

        self.log.info('-----步骤3.查看openGauss中不同负载SELECT，'
                      'UPDATE，INSERT，DELETE，DDL，DML，DCL计数信息，备节点执行-----')
        sql_cmd = self.commonsh1.execut_db_sql(
            f'select DBE_PERF.get_summary_workload_sql_count();')
        self.log.info(sql_cmd)
        list1 = sql_cmd.split('\n')[-2]
        list2 = len(list1.split(','))
        self.log.info(list2)
        if list2 == 9:
            self.log.info('显示openGauss中不同负载技术信息成功')
        else:
            raise Exception('函数执行异常，请检查')

    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0007结束')

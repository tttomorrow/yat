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
Case Type   : 系统管理函数
Case Name   : 其他函数
Description :
    1.函数pg_stat_get_sql_count提供当前节点中所有用户执行的
    SELECT/UPDATE/INSERT/DELETE/MERGE INTO语句的计数结果
Expect      :
    1.查询成功
History     :
"""
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0005开始-')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info(f'-步骤1.查看当前节点中所有用户执行的'
                 f'SELECT/UPDATE/INSERT/DELETE/MERGE INTO语句的计数结果-')
        sql_cmd = self.commonsh.execut_db_sql(f'select user_name,'
                                              f'select_count from '
                                              f'pg_stat_get_sql_count();')
        LOG.info(sql_cmd)
        num = int(sql_cmd.split('\n')[2].split('|')[-1].strip())
        LOG.info(num)
        if num >= 0:
            LOG.info('次数统计成功')
        else:
            raise Exception('查看异常，请检查')

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Manage_Case0005结束-')

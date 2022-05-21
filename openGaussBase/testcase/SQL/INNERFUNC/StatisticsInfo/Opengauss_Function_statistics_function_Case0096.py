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
Case Name   : DBE_PERF.get_statement_responsetime_percentile()，描述：
            获取openGaussSQL响应时间P80，P95分布信息，查询该函数必须具有sysadmin权限。
Description :
    1.获取openGaussSQL响应时间P80，P95分布信息，以系统用户执行
    2.创建普通用户，获取openGaussSQL响应时间P80，P95分布信息，以非系统用户执行
    3.清理环境
Expect      :
    1.获取openGaussSQL响应时间P80，P95分布信息，以系统用户执行成功
    2.创建用户成功，获取openGaussSQL响应时间P80，P95分布信息，以非系统用户执行，合理报错
    3.清理环境成功
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_statistics_function_Case0096开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()
        self.constant = Constant()
        self.user = "u_statistics_function_0096"

    def test_built_in_func(self):
        text = "--step1:获取openGaussSQL响应时间P80，P95分布信息，以系统用户执行;expect:执行成功--"
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'select DBE_PERF.get_statement_responsetime_percentile ();')
        self.log.info(sql_cmd)
        str1 = sql_cmd.split('\n')[-2]
        self.log.info(str1)
        str2 = len(str1.split(','))
        self.log.info(str2)
        self.assertEqual(str2, 2, '执行失败:' + text)

        text = "--step2:创建普通用户，获取openGaussSQL响应时间P80，P95分布信息，" \
               "以非系统用户执行;expect:用户创建成功，非系统用户执行合理报错--"
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'create user {self.user} '
            f'identified by \'{self.dbuser.db_password}\';')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        gsql_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
            f' -U  {self.user} ' \
            f'-W {self.dbuser.db_password}' \
            f' -c "select DBE_PERF.get_statement_responsetime_percentile();" '
        self.log.info(gsql_cmd)
        msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(msg)
        self.assertIn('ERROR:  permission denied for schema dbe_perf',
                      msg, '执行失败:' + text)

    def tearDown(self):
        text = "--step3:清理环境;expect:清理环境成功--"
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop user {self.user} cascade;')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        self.log.info('Opengauss_Function_statistics_function_Case0096结束')

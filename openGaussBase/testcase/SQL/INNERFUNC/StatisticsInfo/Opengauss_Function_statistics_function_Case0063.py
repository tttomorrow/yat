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
Case Name   : DBE_PERF.get_local_toast_relation()描述：提供本地toast表的name和
            其关联表的对应关系，查询该函数必须具有sysadmin权限
Description :
    1.提供本地toast表的name和其关联表的对应关系，以系统管理员执行
    2.提供本地toast表的name和其关联表的对应关系，以非系统管理员执行
Expect      :
    1.提供本地toast表的name和其关联表的对应关系，以系统管理员执行成功
    2.提供本地toast表的name和其关联表的对应关系，以非系统管理员执行，合理报错
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
        self.log.info('Opengauss_Function_statistics_function_Case0063开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        self.log.info('-----步骤1.提供本地toast表的name和其关联表的对应关系，以系统管理员执行-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select DBE_PERF.get_local_toast_relation ();')
        self.log.info(sql_cmd)
        number = len(sql_cmd.splitlines())
        self.log.info(number)
        if number >= 3:
            self.assertIn('pg_statistic', sql_cmd)
            str_info = sql_cmd.split('\n')[-2]
            self.log.info(str_info)
            num = len(str_info.split(','))
            self.log.info(f'num = {num}')
            if num == 3:
                self.log.info('提供本地toast表的name和其关联表的对应关系成功')
            else:
                raise Exception('函数执行异常，请检查')

            self.log.info("-----步骤2.提供本地toast表的name和其关联表的对应关系，以非系统管理员执行-----")
            gsql_cmd = f'source {macro.DB_ENV_PATH};' \
                f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
                f' -U  {self.dbuser.db_user} ' \
                f'-W {self.dbuser.db_password}' \
                f' -c "select DBE_PERF.get_local_toast_relation();" '
            self.log.info(gsql_cmd)
            msg = self.dbuser.sh(gsql_cmd).result()
            self.log.info(msg)
            self.assertIn('ERROR:  permission denied for schema dbe_perf', msg)
        else:
            raise Exception('函数执行异常，请检查')
        
    def tearDown(self):
        self.log.info('Opengauss_Function_statistics_function_Case0063结束')

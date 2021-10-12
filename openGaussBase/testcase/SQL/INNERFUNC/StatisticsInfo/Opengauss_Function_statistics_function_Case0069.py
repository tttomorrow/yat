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
Case Name   : get_instr_user_login()描述：获取当前节点的用户登入登出次数信息，查询该函数必须具有sysadmin权限。
Description :
    1.获取当前节点的用户登入登出次数信息，以系统管理员执行
    2.获取当前节点的用户登入登出次数信息，以非系统管理员执行
    3.清理环境
Expect      :
    1.获取当前节点的用户登入登出次数信息，以系统管理员执行成功
    2.获取当前节点的用户登入登出次数信息，以非系统管理员执行，合理报错
    3.清理环境成功
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
        self.log.info('Opengauss_Function_statistics_function_Case0069开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()

    def test_built_in_func(self):
        self.log.info('-----步骤1.获取当前节点的用户登入登出次数信息，以系统管理员执行-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select get_instr_user_login();')
        self.log.info(sql_cmd)
        number = len(sql_cmd.splitlines())
        self.log.info(number)
        if number >= 3:
            str_info = sql_cmd.split('\n')[2]
            self.log.info(str_info)
            num = len(str_info.split(','))
            self.log.info(f'num = {num}')
            if num == 5:
                self.log.info('获取当前节点的用户登入登出次数信息成功')
            else:
                raise Exception('函数执行异常，请检查')

            self.log.info("-----步骤2.获取当前节点的用户登入登出次数信息，以非系统管理员执行-----")
            sql_cmd = self.commonsh.execut_db_sql(
                f'Create user test identified by \'{macro.COMMON_PASSWD}\';')
            self.log.info(sql_cmd)
            sql_msg = f'source {macro.DB_ENV_PATH};' \
                f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
                f' -U  test ' \
                f'-W {macro.COMMON_PASSWD}' \
                f' -c "select get_instr_user_login();" '
            self.log.info(sql_msg)
            msg = self.dbuser.sh(sql_msg).result()
            self.log.info(msg)
            self.assertIn('ERROR:  only system/monitor admin can get '
                          'user statistics info', msg)
        else:
            raise Exception('函数执行异常，请检查')

    def tearDown(self):
        self.log.info('-----步骤3.清理环境-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop user test;')
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_statistics_function_Case0069结束')

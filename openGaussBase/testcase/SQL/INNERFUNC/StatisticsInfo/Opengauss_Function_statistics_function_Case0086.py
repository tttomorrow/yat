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
Case Name   : gs_wlm_get_user_info(int),获取所有用户的相关信息，入参为int类型，
            可以为任意int值或NULL。该函数只有sysadmin权限的用户可以执行
Description :
    1.获取所有用户的相关信息，以系统用户执行
    2.获取所有用户的相关信息，以非系统用户执行
    3.清理环境
Expect      :
    1.获取所有用户的相关信息，以系统用户执行成功
    2.获取所有用户的相关信息，以非系统用户执行，合理报错
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
        self.log.info('Opengauss_Function_statistics_function_Case0086开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_built_in_func(self):
        self.log.info('-----步骤1.获取所有用户的相关信息，以系统用户执行--')
        sql_cmd = self.commonsh.execut_db_sql(
            f'select gs_wlm_get_user_info(1);')
        self.log.info(sql_cmd)
        str1 = sql_cmd.split('\n')[-2]
        self.log.info(f'str1 = {str1}')
        num = len(str1.split(','))
        self.log.info(f'list1 = {num}')
        if num == 8:
            self.log.info('获取所有用户的相关信息成功')
        else:
            raise Exception('函数执行异常，请检查')

        self.log.info("-----步骤2.获取所有用户的相关信息，以非系统用户执行-----")
        sql_cmd = self.commonsh.execut_db_sql(
            f'Create user test identified by \'{macro.COMMON_PASSWD}\';')
        self.log.info(sql_cmd)
        sql_msg = f'source {macro.DB_ENV_PATH};' \
            f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
            f' -U  test ' \
            f'-W {macro.COMMON_PASSWD}' \
            f' -c "select gs_wlm_get_user_info(1);" '
        self.log.info(sql_msg)
        msg = self.dbuser.sh(sql_msg).result()
        self.log.info(msg)
        self.assertIn(f'ERROR:  permission denied for '
                      f'function pg_stat_get_wlm_user_info', msg)

    def tearDown(self):
        self.log.info('-----步骤3.清理环境-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop user test cascade;')
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_statistics_function_Case0086结束')

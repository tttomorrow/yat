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
Case Name   : gs_wlm_readjust_user_space_through_username(text name)
            描述：修正指定用户的存储空间使用情况
Description :
    1.修正指定用户的存储空间使用情况,以管理员用户执行
    2.修正指定用户的存储空间使用情况,以非管理员用户执行
    3.清理环境
Expect      :
    1.修正指定用户的存储空间使用情况,以管理员用户执行成功
    2.修正指定用户的存储空间使用情况,以非管理员用户执行，只能修正自己的使用情况
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
        self.log.info('Opengauss_Function_statistics_function_Case0091开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_built_in_func(self):
        self.log.info('-----步骤1.修正指定用户的存储空间使用情况,以管理员用户执行--')
        self.log.info(vars(self.dbuser))
        sql_cmd = self.commonsh.execut_db_sql(
            f'select gs_wlm_readjust_user_space_'
            f'through_username(\'{self.dbuser.db_user}\');'
            f'select gs_wlm_readjust_user_space_'
            f'through_username(\'{self.dbuser.ssh_user}\');')
        self.log.info(sql_cmd)
        self.assertIn('Exec Success', sql_cmd)

        self.log.info('--步骤2.修正指定用户的存储空间使用情况,以非管理员用户执行--')
        sql_cmd = self.commonsh.execut_db_sql(
            f'Create user test identified by \'{macro.COMMON_PASSWD}\';')
        self.assertIn('CREATE ROLE', sql_cmd)
        self.log.info(sql_cmd)
        sql_msg = f'source {macro.DB_ENV_PATH};' \
            f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
            f' -U  test ' \
            f'-W {macro.COMMON_PASSWD}' \
            f' -c "select gs_wlm_readjust_user_space_' \
            f'through_username(\'{self.dbuser.db_user}\');' \
            f'select gs_wlm_readjust_user_space_through_username(\'test\');" '
        self.log.info(sql_msg)
        msg = self.dbuser.sh(sql_msg).result()
        self.log.info(msg)
        self.assertIn(f'ERROR:  Normal user could not '
                      f'readjust other user space', msg)
        self.assertIn('Exec Success', msg)

    def tearDown(self):
        self.log.info('-----步骤3.清理环境-----')
        sql_cmd = self.commonsh.execut_db_sql(
            f'drop user test cascade;')
        self.log.info(sql_cmd)
        self.assertIn('DROP ROLE', sql_cmd)
        self.log.info('Opengauss_Function_statistics_function_Case0091结束')

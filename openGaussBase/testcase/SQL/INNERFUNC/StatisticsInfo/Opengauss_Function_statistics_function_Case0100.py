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
Case Name   : pg_stat_get_wlm_session_info(int flag)描述：
            获取当前内存中记录的TopSQL查询语句级别相关统计信息
Description :
    1.获取当前内存中记录的TopSQL查询语句级别相关统计信息，以系统用户执行
    2.创建监控管理员
    2.获取当前内存中记录的TopSQL查询语句级别相关统计信息，以监控管理员执行
    3.获取当前内存中记录的TopSQL查询语句级别相关统计信息，以普通用户执行
    4.恢复环境
Expect      :
    1.获取当前内存中记录的TopSQL查询语句级别相关统计信息，以系统用户执行成功
    2.获取当前内存中记录的TopSQL查询语句级别相关统计信息，以监控管理员执行失败
    3.获取当前内存中记录的TopSQL查询语句级别相关统计信息，以普通用户执行失败
    4.恢复环境成功
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
        self.log.info('Opengauss_Function_statistics_function_Case0100开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()
        self.constant = Constant()
        self.user_1 = "u_statistics_function_0100_01"
        self.user_2 = "u_statistics_function_0100_02"

    def test_built_in_func(self):
        text = '--step1:获取所有用户的资源使用统计信息，以系统用户执行;expect:执行成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'select pg_stat_get_wlm_session_info (1);')
        self.log.info(sql_cmd)
        self.assertIn('0 rows', sql_cmd, '执行失败:' + text)

        text = '--step2:创建监控管理员;expect:创建成功'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'create user {self.user_1} with monadmin password '
            f' \'{self.dbuser.db_password}\';')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = '--step3:获取所有用户的资源使用统计信息，以监控管理员执行;expect:合理报错--'
        self.log.info(text)
        gsql_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
            f' -U {self.user_1}' \
            f' -W {self.dbuser.db_password}' \
            f' -c "select pg_stat_get_wlm_session_info(1);" '
        self.log.info(gsql_cmd)
        msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(msg)
        self.assertIn('0 rows', msg, '执行失败:' + text)

        text = '--step4:创建普通用户;expect:创建成功'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'create user {self.user_2} identified '
            f'by \'{self.dbuser.db_password}\';')
        self.log.info(sql_cmd)

        text = '--step5:获取所有用户的资源使用统计信息，以普通用户执行;expect:合理报错--'
        self.log.info(text)
        gsql_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
            f' -U {self.user_2}' \
            f' -W {self.dbuser.db_password}' \
            f' -c "select pg_stat_get_wlm_session_info(1);" '
        self.log.info(gsql_cmd)
        msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(msg)
        self.assertIn('ERROR:  permission denied for '
                      'function pg_stat_get_wlm_session_info', msg)

    def tearDown(self):
        text = '--step6:清理环境;expect:清理环境成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'drop user {self.user_1} '
                                              f'cascade;'
                                              f'drop user {self.user_2} '
                                              f'cascade;')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        self.log.info('Opengauss_Function_statistics_function_Case0100结束')

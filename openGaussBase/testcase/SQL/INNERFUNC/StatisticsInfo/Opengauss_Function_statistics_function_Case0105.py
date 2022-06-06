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
Case Name   : get_instr_unique_sql()描述：获取当前节点的执行语句（归一化SQL）信息，
            查询该函数必须具有sysadmin权限。
Description :
    1.获取当前节点的执行语句（归一化SQL）信息，以系统用户执行
    2.创建普通用户
    2.获取当前节点的执行语句（归一化SQL）信息，以非系统用户执行
    4.恢复环境
Expect      :
    1.获取当前节点的执行语句（归一化SQL）信息，以系统用户执行成功
    2.创建普通用户
    3.获取当前节点的执行语句（归一化SQL）信息，以非系统用户执行，合理报错
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
        self.log.info('Opengauss_Function_statistics_function_Case0105开始')
        self.dbuser = Node('dbuser')
        self.commonsh = CommonSH()
        self.constant = Constant()
        self.user = "u_statistics_function_0105"

    def test_built_in_func(self):
        text = '--step1.获取当前节点的执行语句（归一化SQL）信息，以系统用户执行;expect:执行成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'select get_instr_unique_sql() limit 3;')
        self.log.info(sql_cmd)
        str_info = sql_cmd.split('\n')[-2]
        self.log.info(str_info)
        num = len(str_info.split(','))
        self.log.info(f'num = {num}')
        if num > 0:
            self.log.info('获取当前节点的执行语句（归一化SQL）信息成功')
        else:
            raise Exception(f'函数执行异常，请检查{text}')

        text = '--step2.创建普通用户;expect:创建用户成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(
            f'create user {self.user} identified '
            f'by  \'{self.dbuser.db_password}\';')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = '--step3.获取当前节点的执行语句（归一化SQL）信息，以非系统用户执行;expect:合理报错--'
        self.log.info(text)
        gsql_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -p {self.dbuser.db_port} -d {self.dbuser.db_name}' \
            f' -U {self.user} ' \
            f' -W {self.dbuser.db_password}' \
            f' -c "select get_instr_unique_sql() limit 3;" '
        self.log.info(gsql_cmd)
        msg = self.dbuser.sh(gsql_cmd).result()
        self.log.info(msg)
        self.assertIn('ERROR:  only system/monitor'
                      ' admin can query unique sql view', msg)

    def tearDown(self):
        text = '--step4.恢复环境;expect:执行成功--'
        self.log.info(text)
        sql_cmd = self.commonsh.execut_db_sql(f'drop user {self.user} '
                                              f'cascade;')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        self.log.info('Opengauss_Function_statistics_function_Case0105结束')

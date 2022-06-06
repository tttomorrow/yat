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
Case Type   : 系统信息函数-会话信息函数
Case Name   : 使用函数pg_get_ruledef(rule_oid) ，获取规则的CREATE RULE命令
Description : 使用函数pg_get_ruledef(rule_oid) ，获取规则的CREATE RULE命令
Expect      : 使用函数pg_get_ruledef(rule_oid) ，获取规则的CREATE RULE命令
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0015开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        LOG.info(f'-步骤1.查看数据库中规则名')
        sql_cmd1 = self.commonsh.execut_db_sql(
            f'select rulename,tablename,definition from pg_rules;')
        LOG.info(sql_cmd1)
        self.assertIn('pg_settings_u', sql_cmd1)
        self.assertIn('pg_settings_n', sql_cmd1)

        LOG.info(f'-步骤2.根据规则名查看oid')
        sql_cmd2 = self.commonsh.execut_db_sql(
            f'select oid,rulename from pg_rewrite '
            f'where rulename = \'pg_settings_u\';')
        LOG.info(sql_cmd2)
        oid = int(sql_cmd2.split('\n')[2].split('|')[0])
        LOG.info(oid)
        if oid >= 0:
            LOG.info('查看临时模式的OID成功')
        else:
            raise Exception('查看异常，请检查')

        LOG.info(f'-步骤3.使用函数pg_get_ruledef(rule_oid)，获取规则的CREATE RULE命令')
        sql_cmd3 = self.commonsh.execut_db_sql(
            f'select * from pg_get_ruledef({oid});')
        LOG.info(sql_cmd3)
        rule_command = sql_cmd3.split('\n')[2]
        LOG.info(rule_command)
        self.assertIn(f'{rule_command}', sql_cmd1)

    def tearDown(self):
        LOG.info('-------无需清理环境-------')
        LOG.info('-Opengauss_Function_Innerfunc_System_Info_Case0015结束-')

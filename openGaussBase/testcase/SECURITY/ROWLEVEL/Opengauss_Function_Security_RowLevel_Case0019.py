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
Case Type   : security_masking
Case Name   : 创建行访问控制策略指定不存在的用户
Description :
    1.创建表
    2.打开行级访问开关，创建行级访问策略，指定不存在的用户
Expect      :
    1.创建成功
    2.创建成功
    3.创建成功
History     :
"""
import unittest
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '---Opengauss_Function_Security_RowLevel_Case0019 start---')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.user01 = 'u01_security_rowlevel_0019'
        self.table = 'table_security_rowlevel_0019'
        self.rowlevel = 'rls_ecurity_rowlevel_0019'
    
    def test_masking(self):
        text = '--------step1：创建表，并给用户赋予访问权限;expect：成功--------'
        self.logger.info(text)
        sql_cmd1 = f'create table {self.table}(id int, role varchar(100), ' \
            f'data varchar(100));'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertIn('CREATE TABLE', msg1, '执行失败:' + text)
        text = '----step2：创建行级访问策略,指定不存在的用户；expect：失败----'
        self.logger.info(text)
        sql_cmd2 = f'create row level security policy {self.rowlevel} on ' \
            f'{self.table} to {self.user01} using(role = current_user);'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.assertIn(f'role "{self.user01}" does not exist', msg2,
                      '执行失败:' + text)
    
    def tearDown(self):
        text = '-------清理环境------'
        self.logger.info(text)
        sql_cmd1 = f'drop table {self.table} cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.logger.info(
            '---Opengauss_Function_Security_RowLevel_Case0019 finish---')

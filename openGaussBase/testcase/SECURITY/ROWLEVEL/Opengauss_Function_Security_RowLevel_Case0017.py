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
Case Name   : 同一张表最多创建100个行访问控制策略
Description :
    1.创建表
    2.创建行级访问策略101个
Expect      :
    1.创建成功
    2.第100个创建成功，第101个创建失败
History     :
"""
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        text = '---Opengauss_Function_Security_RowLevel_Case0017 start---'
        self.logger.info(text)
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.table = 'table_security_rowlevel_0017'
        self.rowlevel = 'rls_ecurity_rowlevel_0017'
    
    def test_masking(self):
        text = '------step1：创建表 expect:成功------'
        self.logger.info(text)
        sql_cmd1 = f'drop table if exists {self.table};' \
            f'create table {self.table}(id int, role varchar(100), ' \
            f'data varchar(100));'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertIn('CREATE TABLE', msg1, '执行成功' + text)
        text = '---step2：创建行级访问策略101个 expect:失败---'
        self.logger.info(text)
        content_list = []
        i = 1
        while i < 102:
            rowlevel = self.rowlevel + '_' + str(i)
            sql_cmd2 = f'CREATE ROW LEVEL SECURITY POLICY {rowlevel} ON ' \
                f'{self.table} USING(role = CURRENT_USER);'
            msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
            self.logger.info(msg2)
            content_list.append(msg2.strip())
            i += 1
        self.logger.info(content_list)
        self.assertIn('should less than or equal to 100', content_list[-1],
                      '执行失败:' + text)
    
    def tearDown(self):
        self.logger.info('-------清理资源------')
        sql_cmd1 = f'drop table {self.table};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.logger.info(
            '---Opengauss_Function_Security_RowLevel_Case0017 finish---')

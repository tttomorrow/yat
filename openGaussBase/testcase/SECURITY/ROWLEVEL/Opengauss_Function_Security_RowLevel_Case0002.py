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
Case Type   : security_rowlevel
Case Name   : 表创建行访问控制策略，关闭行访问控制开关，策略不生效
Description :
    1.创建用户
    2.创建表，并给用户赋予访问权限
    3.关闭开行级访问开关，创建行级访问策略
    4.不同的用户分别登陆数据库访问表
Expect      :
    1.创建成功
    2.创建成功，赋权成功
    3.创建成功
    4.每个用户可以查看到所有的数据
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '---Opengauss_Function_Security_RowLevel_Case0002 start---')
        self.userNode = Node(node='PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.user01 = 'u01_security_rowlevel_0002'
        self.user02 = 'u02_security_rowlevel_0002'
        self.user03 = 'u03_security_rowlevel_0002'
        self.table = 'table_security_rowlevel_0002'
        self.rowlevel = 'rls_ecurity_rowlevel_0002'
    
    def test_masking(self):
        text = '--------step1：创建用户；expect：成功--------'
        self.logger.info(text)
        sql_cmd1 = f'create user {self.user01} password ' \
            f'\'{macro.COMMON_PASSWD}\';create user {self.user02} password' \
            f' \'{macro.COMMON_PASSWD}\';create user {self.user03} ' \
            f'password \'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertTrue(msg1.count('CREATE ROLE') == 3, '执行失败:' + text)
        text = '--------step2：创建表，并给用户赋予访问权限--------'
        self.logger.info(text)
        sql_cmd2 = f'create table {self.table}(id int, role varchar(100), ' \
            f'data varchar(100));insert into {self.table} values(1, ' \
            f'\'{self.user01}\', \'alice data\');insert into {self.table} ' \
            f'values(2, \'{self.user02}\', \'bob data\');insert into ' \
            f'{self.table} values(3, \'{self.user03}\', \'peter data\');' \
            f'grant select on {self.table} to {self.user01}, {self.user02}, ' \
            f'{self.user03};'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.assertIn('GRANT', msg2, '执行失败:' + text)
        text = '----step3：关闭开行级访问开关，创建行级访问策略；expect：成功----'
        self.logger.info(text)
        sql_cmd3 = f'create row level security policy {self.rowlevel} on ' \
            f'{self.table} using(role = current_user);'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertIn('CREATE ROW LEVEL SECURITY', msg3, '执行失败:' + text)
        text = '----step4：不同得用户分别登陆数据库访问表；expect：成功----'
        self.logger.info(text)
        sql_cmd4 = f'select data from {self.table};'
        exe_cmd4 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.user01} -W \'' \
            f'{macro.COMMON_PASSWD}\' -c "{sql_cmd4}"'
        self.logger.info(exe_cmd4)
        msg4 = self.userNode.sh(exe_cmd4).result()
        self.logger.info(msg4)
        self.common.equal_sql_mdg(msg4, 'data', 'alice data', 'bob data',
                                  'peter data', '(3 rows)', flag='1')
        exe_cmd5 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.user02} -W \'' \
            f'{macro.COMMON_PASSWD}\' -c "{sql_cmd4}"'
        self.logger.info(exe_cmd5)
        msg5 = self.userNode.sh(exe_cmd5).result()
        self.logger.info(msg5)
        self.common.equal_sql_mdg(msg5, 'data', 'alice data', 'bob data',
                                  'peter data', '(3 rows)', flag='1')
    
    def tearDown(self):
        text = '-------清理环境------'
        self.logger.info(text)
        sql_cmd1 = f'drop row level security policy {self.rowlevel} on ' \
            f'{self.table};' \
            f'drop table {self.table} cascade;' \
            f'drop user {self.user01} cascade;' \
            f'drop user {self.user02} cascade;' \
            f'drop user {self.user03} cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.logger.info(
            '---Opengauss_Function_Security_RowLevel_Case0002 finish---')

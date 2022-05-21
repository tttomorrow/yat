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
Case Type   : 事务控制
Case Name   : 执行匿名块后不加‘/’，使用commit进行提交是否成功
Description :
    1.创建测试表
    DROP TABLE IF EXISTS TESTZL;
    CREATE TABLE TESTZL (
        SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
    2.执行匿名块后不加‘/’,使用commit进行提交
    DECLARE
    BEGIN
      INSERT INTO TESTZL VALUES (001,'SK1','TT',3332);
    END;
    COMMIT;
    3.清理环境
    DROP TABLE IF EXISTS TESTZL;
Expect      :
    1.创建成功
    2.匿名块无法提交
    3.清理环境成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


class TransactionFile(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_DML_Transaction_Case0031开始执行----')
        self.pri_node = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.t_name = 't_dml_transaction_case0031'

    def test_transaction_file(self):
        step_txt = '----step1：新建测试表 expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f'DROP TABLE IF EXISTS {self.t_name};' \
            f'CREATE TABLE {self.t_name} (' \
            f'SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);'
        create_msg = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_msg,
                      '执行失败:' + step_txt)

        step_txt = "----step2：执行匿名块后不加‘/’,使用commit进行提交" \
                   " expect:匿名块无法提交----"
        self.log.info(step_txt)
        sql_cmd = f'''DECLARE
                      BEGIN
                       INSERT INTO {self.t_name} VALUES (001,'SK1','TT',3332);
                      END;
                      COMMIT;
                     '''
        connect_cmd = f'gsql -d {self.pri_node.db_name} ' \
            f'-p {self.pri_node.db_port}'
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                   expect <<EOF
                   set timeout 10
                   spawn {connect_cmd}
                   expect {self.pri_node.db_name + "=#"}
                   send "{sql_cmd}\\n"
                   expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        exec_msg = self.pri_node.sh(execute_cmd).result()
        self.log.info(exec_msg)
        exp_msg = exec_msg.splitlines()[-1].strip()
        self.assertNotIn(self.pri_node.db_name + "=#", exp_msg,
                         '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----step3：清理环境----')
        text_1 = '----删除表 expect:成功----'
        self.log.info(text_1)
        drop_sql = f'DROP TABLE IF EXISTS {self.t_name};'
        drop_msg = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_msg)
        self.log.info(
            '----Opengauss_Function_DML_Transaction_Case0031执行完成----')

        self.log.info('----断言tearDown执行成功----')
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text_1)

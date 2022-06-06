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
Case Name   : 执行匿名块后加‘/’进行提交，查看备机数据是否同步
Description :
    1.创建测试表
    DROP TABLE IF EXISTS TESTZL;
    CREATE TABLE TESTZL (
        SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);
    2.执行匿名块后加‘/’进行提交
    DECLARE
    BEGIN
      INSERT INTO TESTZL VALUES (001,'SK1','TT',3332);
    END;
    /
    3.查看备机事务数据是否同步
    SELECT * FROM TESTZL;
    4.清理环境
    DROP TABLE IF EXISTS TESTZL;
Expect      :
    1.创建成功
    2.提交成功
    3.同步
    4.清理环境成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(), '单机环境不执行')
class TransactionFile(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_DML_Transaction_Case0032开始执行----')
        self.PrimaryNode = Node('PrimaryDbUser')
        self.Standby_SH = CommonSH('Standby1DbUser')
        self.constant = Constant()
        self.t_name = 't_dml_transaction_case0032'

    def test_transaction_file(self):
        step_txt = '----step1：新建测试表 expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f'DROP TABLE IF EXISTS {self.t_name};' \
            f'CREATE TABLE {self.t_name} (' \
            f'SK INTEGER,ID CHAR(16),NAME VARCHAR(20),SQ_FT INTEGER);'
        create_msg = Primary_SH.execut_db_sql(create_sql)
        self.log.info(create_msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_msg,
                      '执行失败:' + step_txt)

        step_txt = '----step2：执行匿名块后加‘/’进行提交 expect:提交成功----'
        self.log.info(step_txt)
        sql_cmd = f'''DECLARE
                      BEGIN
                       INSERT INTO {self.t_name} VALUES (001,'SK1','TT',3332);
                      END;
                      /
                     '''
        connect_cmd = f'gsql -d {self.PrimaryNode.db_name} ' \
            f'-p {self.PrimaryNode.db_port}'
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                   expect <<EOF
                   set timeout 10
                   spawn {connect_cmd}
                   expect {self.PrimaryNode.db_name + "=#"}
                   send "{sql_cmd}\\n"
                   expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        execute_msg = self.PrimaryNode.sh(execute_cmd).result()
        self.log.info(execute_msg)
        self.assertIn(self.constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG,
                      execute_msg, '执行失败:' + step_txt)

        step_txt = '----step3：查看备机事务数据是否同步 expect:同步----'
        self.log.info(step_txt)
        select_sql = f'SELECT * FROM {self.t_name};'
        msg_primary = Primary_SH.execut_db_sql(select_sql)
        self.log.info(msg_primary)
        msg_standby = self.Standby_SH.execut_db_sql(select_sql)
        self.log.info(msg_standby)
        self.assertEqual(msg_primary, msg_standby, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----step4：清理环境----')
        text_1 = '----删除表 expect:成功----'
        self.log.info(text_1)
        drop_sql = f'DROP TABLE IF EXISTS {self.t_name};'
        drop_msg = Primary_SH.execut_db_sql(drop_sql)
        self.log.info(drop_msg)
        self.log.info(
            '----Opengauss_Function_DML_Transaction_Case0032执行完成----')

        self.log.info('----断言tearDown执行成功----')
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, drop_msg,
                      '执行失败:' + text_1)

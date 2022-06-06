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
Case Type   : GUC_ErrorLog
Case Name   : 修改参数log_statement的值为mod
Description :
    1.修改参数log_statement的值为mod
    2.连接数据库执行不同类型SQL语句
    3.查看pg_log日志文件中是否记录步骤2中语句
Expect      :
    1.修改参数log_statement的值为mod，修改成功
    2.连接数据库执行不同类型SQL语句成功
    3.查看pg_log日志文件中记录步骤2中所有DDL语句、数据修改语句
History     :
    modified：2022-3-29 by 5328113;修改pg_log目录，避免其他日志影响
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class ErrorLog(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:start----')
        self.pri_dbuser = Node('PrimaryDbUser')
        self.pri_root = Node('PrimaryRoot')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.tb_name = 'tb_Guc_ErrorLog_Case0113'
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    'pg_errorlog_case0113')

    def test_main(self):
        step_txt = '----查看参数log_directory默认值----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show log_directory;')
        self.log.info(f"log_directory is {result}")
        self.dir_init = result.strip().splitlines()[-2].strip()

        step_txt = '----step0:修改参数log_directory; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"log_directory='{self.dir_new}'",
                                        single=True)
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----查看参数log_statement的默认值----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show log_statement;')
        self.log.info(f"log_statement is {result}")
        self.para1 = result.strip().splitlines()[-2].strip()

        step_txt = '----step1:修改参数log_statement的值为mod expect:设置成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'log_statement=mod')
        self.assertTrue(msg, '执行失败:' + step_txt)

        self.log.info('----重启数据库，避免其他用例关键日志信息影响断言----')
        self.pri_sh.restart_db_cluster()

        step_txt = '----step2: 创建测试表并插入数据，expect: 创建成功----'
        self.log.info(step_txt)
        sql = f"create table {self.tb_name}(id int,name char(1));" \
            f"insert into {self.tb_name} values(4,'a');" \
            f"prepare insert_sql(int,varchar(10)) as " \
            f"insert into {self.tb_name} values(\$1,\$2);" \
            f"execute insert_sql(2,'b');" \
            f"deallocate prepare insert_sql;" \
            f"prepare select_sql(int,varchar(10)) as " \
            f"select * from {self.tb_name} where id = \$1 and name = \$2;" \
            f"execute select_sql(2,'b');" \
            f"deallocate prepare select_sql;" \
            f"select * from {self.tb_name};" \
            f"truncate {self.tb_name};" \
            f"explain analyze select * from {self.tb_name};" \
            f"drop table {self.tb_name};"
        create_result = self.pri_sh.execut_db_sql(sql)
        self.log.info(create_result)

        step_txt = '----step3: 查看pg_log日志文件中是否记录步骤2中语句' \
                   'expect: 记录步骤2中所有DDL语句、数据修改语句---'
        self.log.info(step_txt)
        self.log.info('----查看pg_log----')
        shell_cmd = f'''ls -t {self.dir_new} | head -1'''
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name} | grep 'statement:'"
        self.log.info(shell_cmd)
        result = self.pri_root.sh(shell_cmd).result()
        self.log.info(result)
        self.log.info('----包含DDL语句、数据修改语句打印信息----')
        sql = f"create table {self.tb_name}(id int,name char(1));" \
            f"insert into {self.tb_name} values(4,'a');" \
            f"prepare insert_sql(int,varchar(10)) as " \
            f"insert into {self.tb_name} values($1,$2);" \
            f"execute insert_sql(2,'b');" \
            f"truncate {self.tb_name};" \
            f"drop table {self.tb_name};"
        all_sql = sql.strip().split(';')
        for item_sql in all_sql:
            if item_sql:
                self.log.info(item_sql)
                self.assertIn(item_sql, result, '执行失败:' + step_txt)
        self.log.info('----不包含除ddl、数据修改语句外其他打印信息----')
        sql = f"deallocate prepare insert_sql;" \
            f"prepare select_sql(int,varchar(10)) as " \
            f"select * from {self.tb_name} where id = $1 and name = $2;" \
            f"execute select_sql(2,'b');" \
            f"deallocate prepare select_sql;" \
            f"select * from {self.tb_name};" \
            f"explain analyze select * from {self.tb_name};"
        all_sql = sql.strip().split(';')
        for item_sql in all_sql:
            if item_sql:
                self.log.info(item_sql)
                self.assertNotIn(item_sql, result, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清除表数据 expect: 成功----'
        self.log.info(step1_txt)
        drop_sql = f'drop table if exists {self.tb_name};'
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        step2_txt = '----还原参数 expect: 成功----'
        self.log.info(step2_txt)
        msg1 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'log_statement={self.para1}')
        step3_txt = '----还原参数log_directory; expect:修改成功----'
        self.log.info(step3_txt)
        msg2 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"log_directory='{self.dir_init}'",
                                         single=True)

        step_txt = '----断言teardown执行成功----'
        self.log.info(step_txt)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_result,
                      '执行失败:' + step1_txt)
        self.assertTrue(msg1, '执行失败:' + step2_txt)
        self.assertTrue(msg2, '执行失败:' + step3_txt)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

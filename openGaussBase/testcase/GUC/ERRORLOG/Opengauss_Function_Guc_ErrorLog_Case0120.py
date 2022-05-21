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
Case Name   : 设置数据库级别的参数：logging_module为on(ALL)，不同数据库操作是否产生模块日志
Description :
    1.创建新库
    2.修改新库参数logging_module值为on(ALL)
    3.非新库查看logging_module参数，并进行事务操作（以XACT模块进行验证）
    4.查看pg日志
    5.新库查看logging_module参数，并进行事务操作（以XACT模块进行验证）
    6.查看pg日志
Expect      :
    1.创建新库成功
    2.修改新库参数logging_module值为on(ALL)成功
    3.非新库查看logging_module参数为初始值，进行事务操作成功
    4.查看pg日志，非新库事务未产生XACT模块日志
    5.新库查看logging_module参数为修改值，进行事务操作成功
    6.查看pg日志，新库事务产生XACT模块日志
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
        self.db_name = 'db_guc_errorlog_case0120'
        self.old_db_name = self.pri_dbuser.db_name
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    'pg_errorlog_case0120')

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

        step_txt = '----step1:创建新库 expect：成功----'
        self.log.info(step_txt)
        create_db = f'create database {self.db_name};'
        create_result = self.pri_sh.execut_db_sql(create_db)
        self.log.info(create_result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, create_result,
                      '执行失败:' + step_txt)

        self.log.info('----重启数据库，避免其他用例关键日志信息影响断言----')
        self.pri_sh.restart_db_cluster()

        step_txt = '----查看参数logging_module的默认值----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show logging_module;')
        self.log.info(f"logging_module is {result}")
        self.para1 = result.strip().splitlines()[-2].strip()

        step_txt = '----step2:修改新库参数logging_module值为on(ALL) expect: 成功'
        self.log.info(step_txt)
        sql = f"alter database {self.db_name} set " \
            f"logging_module to 'on(all)';"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)

        step_txt = '----step3:非新库查看logging_module参数，并进行事务操作' \
                   'expect：参数为初始值，进行事务操作成功----'
        self.log.info(step_txt)
        sql = f"show logging_module;" \
            f"start transaction;" \
            f"commit;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.para1, result, '执行失败:' + step_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)

        self.log.info('----step4:查看pg日志 expect：非新库事务未产生XACT模块日志----')
        shell_cmd = f'ls -t {self.dir_new} | head -1'
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name}|grep {self.old_db_name}" \
            f"|grep XACT|grep gsql"
        self.log.info(shell_cmd)
        shell_result = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result)
        self.assertEqual('', shell_result, '执行失败:' + step_txt)

        step_txt = '----step5: 新库查看logging_module参数，进行事务操作' \
                   'expect：参数为修改值，进行事务操作成功----'
        self.log.info(step_txt)
        sql = f"show logging_module;" \
            f"start transaction;" \
            f"commit;"
        result = self.pri_sh.execut_db_sql(sql, dbname=f'{self.db_name}')
        self.log.info(result)
        self.assertNotIn(self.para1, result, '执行失败:' + step_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)

        self.log.info('----step6:查看pg日志 expect：新库事务产生XACT模块日志----')
        shell_cmd = f'ls -t {self.dir_new} | head -1'
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name}|grep {self.db_name}|grep XACT|grep gsql"
        self.log.info(shell_cmd)
        shell_result = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result)
        self.assertNotEqual('', shell_result, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----删除数据库 expect: 成功----'
        self.log.info(step1_txt)
        drop_sql = f"drop database {self.db_name};"
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)
        step2_txt = '----还原参数log_directory; expect:修改成功----'
        self.log.info(step2_txt)
        msg2 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"log_directory='{self.dir_init}'",
                                         single=True)

        step_txt = '----断言teardown执行成功----'
        self.log.info(step_txt)
        self.assertIn(self.constant.DROP_DATABASE_SUCCESS, drop_result,
                      step1_txt)
        self.assertTrue(msg2, '执行失败:' + step2_txt)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

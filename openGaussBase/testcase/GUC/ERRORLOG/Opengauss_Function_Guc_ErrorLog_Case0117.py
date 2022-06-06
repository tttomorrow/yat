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
Case Name   : 设置数据库级别的参数：logging_module为on(ALL)，在下次会话中生效
Description :
    1.创建新库
    2.连接新库，执行修改参数logging_module值为on(ALL)
    3.步骤2会话，查看参数值
    4.步骤2会话进行事务操作（以XACT模块进行验证）
    5.查看pg日志
    6.重新连接新库进行参数查看
    7.步骤6会话进行事务操作
    8.查看pg日志
Expect      :
    1.创建新库成功
    2.连接新库，执行修改参数logging_module值为on(ALL)，设置成功
    3.步骤2会话，查看参数值，未生效
    4.步骤2会话进行事务操作（以XACT模块进行验证）操作成功
    5.查看pg日志，数据库会话内未产生XACT日志信息
    6.重新连接新库进行参数查看，参数值已修改
    7.步骤6会话进行事务操作，操作成功
    8.查看pg日志，数据库会话内产生XACT日志信息
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
        self.db_name = 'db_guc_errorlog_case0117'
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    'pg_errorlog_case0117')

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
        result = self.pri_sh.execut_db_sql('show logging_module;',
                                           dbname=f'{self.db_name}')
        self.log.info(f"logging_module is {result}")
        self.para1 = result.strip().splitlines()[-2].strip()

        step_txt = '----连接新库，执行修改参数logging_module值为on(ALL)，进行会话内事务操作'
        self.log.info(step_txt)
        sql = f"alter database {self.db_name} set " \
            f"logging_module to 'on(all)';" \
            f"show logging_module;" \
            f"start transaction;" \
            f"commit;"
        result = self.pri_sh.execut_db_sql(sql, dbname=f'{self.db_name}')
        self.log.info(result)

        step_txt = '----step2:连接新库，执行修改参数logging_module值为on(ALL)expect：成功----'
        self.log.info(step_txt)
        self.assertIn(self.constant.ALTER_DATABASE_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)

        step_txt = '----step3:步骤2会话，查看参数值 expect：未生效----'
        self.log.info(step_txt)
        self.assertIn(self.para1, result, '执行失败:' + step_txt)

        step_txt = '----step4:步骤2会话进行事务操作（以XACT模块进行验证） expect：操作成功----'
        self.log.info(step_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)

        self.log.info('----step5:查看pg日志 expect：数据库会话内未产生XACT日志信息----')
        shell_cmd = f'ls -t {self.dir_new} | head -1'
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name}|grep {self.db_name}|grep XACT|grep gsql"
        self.log.info(shell_cmd)
        shell_result = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result)
        self.assertEqual('', shell_result, '执行失败:' + step_txt)

        step_txt = '----重新连接新库，进行会话内事务操作----'
        self.log.info(step_txt)
        sql = f"show logging_module;" \
            f"start transaction;" \
            f"commit;"
        result = self.pri_sh.execut_db_sql(sql, dbname=f'{self.db_name}')
        self.log.info(result)

        step_txt = '----step6:重新连接新库进行参数查看 expect：参数值已修改----'
        self.log.info(step_txt)
        self.assertNotIn(self.para1, result, '执行失败:' + step_txt)

        step_txt = '----step7:步骤6会话进行事务操作 expect：操作成功----'
        self.log.info(step_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)

        self.log.info('----step8:查看pg日志 expect：数据库会话内产生XACT日志信息----')
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

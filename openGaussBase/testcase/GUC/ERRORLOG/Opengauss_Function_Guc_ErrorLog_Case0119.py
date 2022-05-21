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
Case Name   : 设置会话级别的参数：logging_module为on(ALL)，修改本次会话中的取值,退出会话后，设置将失效
Description :
    1.打开会话，执行修改参数logging_module值为on(ALL)
    2.步骤1会话，查看参数值
    3.步骤1会话进行事务操作（以XACT模块进行验证）
    4.查看pg日志
    5.重新打开会话
    6.步骤5会话进行事务操作
    7.查看pg日志
Expect      :
    1.打开会话，执行修改参数logging_module值为on(ALL)，设置成功
    2.步骤1会话，查看参数值，生效
    3.步骤1会话进行事务操作（以XACT模块进行验证）操作成功
    4.查看pg日志，数据库会话内产生XACT日志信息
    5.重新打开会话，查看参数值，未生效
    6.步骤5会话进行事务操作，操作成功
    7.查看pg日志，数据库会话内未产生XACT日志信息
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
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    'pg_errorlog_case0119')

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

        self.log.info('----重启数据库，避免其他用例关键日志信息影响断言----')
        self.pri_sh.restart_db_cluster()

        step_txt = '----查看参数logging_module的默认值----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show logging_module;')
        self.log.info(f"logging_module is {result}")
        self.para1 = result.strip().splitlines()[-2].strip()

        step_txt = '----打开会话，执行修改参数logging_module值为on(ALL)，进行会话内事务操作'
        self.log.info(step_txt)
        sql = f"set logging_module to 'on(all)';" \
            f"show logging_module;" \
            f"start transaction;" \
            f"commit;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)

        step_txt = '----step1:修改参数logging_module值为on(ALL)expect：成功----'
        self.log.info(step_txt)
        self.assertIn(self.constant.SET_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)

        step_txt = '----step2:步骤2会话，查看参数值 expect：生效----'
        self.log.info(step_txt)
        self.assertNotIn(self.para1, result, '执行失败:' + step_txt)

        step_txt = '----step3:步骤2会话进行事务操作（以XACT模块进行验证） expect：操作成功----'
        self.log.info(step_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)

        self.log.info('----step4:查看pg日志 expect：数据库会话内未产生XACT日志信息----')
        shell_cmd = f'ls -t {self.dir_new} | head -1'
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name}|grep XACT|grep gsql"
        self.log.info(shell_cmd)
        shell_result1 = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result1)
        self.assertNotEqual('', shell_result1, '执行失败:' + step_txt)

        step_txt = '----重新打开会话，进行会话内事务操作----'
        self.log.info(step_txt)
        sql = f"show logging_module;" \
            f"start transaction;" \
            f"commit;"
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)

        step_txt = '----step5:重新打开会话进行参数查看 expect：参数值已恢复----'
        self.log.info(step_txt)
        self.assertIn(self.para1, result, '执行失败:' + step_txt)

        step_txt = '----step6:步骤6会话进行事务操作 expect：操作成功----'
        self.log.info(step_txt)
        self.assertIn(self.constant.START_TRANSACTION_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)

        self.log.info('----step7:查看pg日志 expect：较步骤4不产生多余XACT日志信息----')
        shell_cmd = f'ls -t {self.dir_new} | head -1'
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name}|grep XACT|grep gsql"
        self.log.info(shell_cmd)
        shell_result2 = self.pri_dbuser.sh(shell_cmd).result()
        self.log.info(shell_result2)
        self.assertEqual(shell_result1, shell_result2, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----还原参数log_directory; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"log_directory='{self.dir_init}'",
                                        single=True)
        step_txt = '----断言teardown执行成功----'
        self.log.info(step_txt)
        self.assertTrue(msg, '执行失败:' + step_txt)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

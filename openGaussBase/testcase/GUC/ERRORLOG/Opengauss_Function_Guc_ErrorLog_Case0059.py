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
Case Name   : 修改参数log_min_messages的值为error
Description :
    1.修改log_min_messages参数为error
    2.执行产生warning级别日志的SQL语句；“commit”；
    3.执行产生error级别日志的SQL语句；“create table test;”’
Expect      :
    1.修改log_min_messages参数为error，修改成功
    2.执行产生warning级别日志的SQL语句；“commit”；查看pg日志，不打印warning级别日志
    3.执行产生error级别日志的SQL语句；“create table test;”’；查看pg日志，打印ERROR级别日志信息
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
        self.tb_name = 'tb_Guc_ErrorLog_Case0059'
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    'pg_errorlog_case0059')

    def test_main(self):
        step_txt = '----查看log_min_messages初始配置值----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show log_min_messages;')
        self.log.info(f"log_min_messages is {result}")
        self.para1 = result.strip().splitlines()[-2]
        result = self.pri_sh.execut_db_sql('show log_directory;')
        self.log.info(f"log_directory is {result}")
        self.dir_init = result.strip().splitlines()[-2].strip()
        result = self.pri_sh.execut_db_sql('show log_min_error_statement;')
        self.log.info(f"log_min_error_statement is {result}")

        step_txt = '----step0:修改参数log_directory; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"log_directory='{self.dir_new}'",
                                        single=True)
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step1:修改log_min_messages参数为error; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'log_min_messages=error')
        self.assertTrue(msg, '执行失败:' + step_txt)

        self.log.info('----重启数据库，避免其他用例关键日志信息影响断言----')
        self.pri_sh.restart_db_cluster()

        step_txt = '----step2:执行产生warning级别日志的SQL语句；' \
                   '查看pg日志; expect:不打印warning级别日志----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('commit;')
        self.log.info(result)
        self.assertTrue('WARNING' in result, '执行失败:' + step_txt)
        self.log.info('----查看pg_log----')
        shell_cmd = f'''ls -t {self.dir_new} | head -1'''
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        msg_flag = 'WARNING:  there is no transaction in progress'
        shell_cmd = f"cat {file_name} | grep '{msg_flag}' -5"
        self.log.info(shell_cmd)
        result = self.pri_root.sh(shell_cmd).result()
        self.log.info(result)
        self.assertEqual('', result, '执行失败:' + step_txt)

        step_txt = '----step3:执行产生error级别日志的SQL语句；' \
                   '查看pg日志; expect:打印ERROR级别日志----'
        self.log.info(step_txt)
        sql = f'create table {self.tb_name};'
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertTrue('ERROR' in result)
        self.log.info('----查看pg_log----')
        shell_cmd = f'''ls -t {self.dir_new} | head -1'''
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name} | grep '{sql}' -B 1"
        self.log.info(shell_cmd)
        result = self.pri_root.sh(shell_cmd).result()
        self.log.info(result)
        self.assertIn('ERROR', result, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt1 = '----还原参数log_directory; expect:修改成功----'
        self.log.info(step_txt1)
        msg1 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"log_directory='{self.dir_init}'",
                                         single=True)

        step_txt2 = '----恢复参数log_min_messages值为初始值; expect:修改成功----'
        self.log.info(step_txt2)
        msg2 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'log_min_messages={self.para1}')

        step_txt = '----断言teardown执行成功----'
        self.log.info(step_txt)
        self.assertTrue(msg1, '执行失败:' + step_txt1)
        self.assertTrue(msg2, '执行失败:' + step_txt2)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

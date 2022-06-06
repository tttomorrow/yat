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
Case Name   : 设置参数debug_pretty_print的默认值为off
Description :
    1.设置debug_pretty_print参数为off
    2.设置debug_print_parse、debug_print_rewritten和debug_print_plan的值均为on
    3.进行简单的SQL操作，查看pg日志
Expect      :
    1.设置debug_pretty_print参数为off，设置成功
    2.设置成功
    3.进行简单的SQL操作，查看pg日志，打印的执行计划、解析树、重写结果信息未缩进展示
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
        self.tb_name = 'tb_Guc_ErrorLog_Case0095'
        self.suc_flag1 = 'LOG:  plan'
        self.suc_flag2 = 'LOG:  rewritten parse tree'
        self.suc_flag3 = 'LOG:  parse tree'
        self.suc_flag4 = 'DETAIL:     {QUERY \n'
        self.suc_flag5 = 'DETAIL:  (\n'
        self.suc_flag6 = 'DETAIL:     {PLANNEDSTMT \n'
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    'pg_errorlog_case0095')

    def test_main(self):
        step_txt = '----查询debug_pretty_print参数默认值----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show debug_print_plan;')
        self.log.info(f"debug_print_plan is {result}")
        self.para1 = result.strip().splitlines()[-2].strip()
        result = self.pri_sh.execut_db_sql('show debug_print_parse;')
        self.log.info(f"debug_print_parse is {result}")
        self.para2 = result.strip().splitlines()[-2].strip()
        result = self.pri_sh.execut_db_sql('show debug_print_rewritten;')
        self.log.info(f"debug_print_rewritten is {result}")
        self.para3 = result.strip().splitlines()[-2].strip()
        result = self.pri_sh.execut_db_sql('show debug_pretty_print;')
        self.log.info(f"debug_pretty_print is {result}")
        self.para4 = result.strip().splitlines()[-2].strip()
        self.assertEqual('on', self.para4, '执行失败:' + step_txt)
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

        step_txt = '----step1:设置debug_pretty_print参数为off expect:设置成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'debug_pretty_print=off')
        self.assertTrue(msg, '执行失败:' + step_txt)

        self.log.info('----重启数据库，避免其他用例关键日志信息影响断言----')
        self.pri_sh.restart_db_cluster()

        step_txt = '----step2:设置debug_print_parse、debug_print_rewritten和' \
                   'debug_print_plan的值均为on expect:设置成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'debug_print_plan=on')
        self.assertTrue(msg, '执行失败:' + step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'debug_print_parse=on')
        self.assertTrue(msg, '执行失败:' + step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'debug_print_rewritten=on')
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step3:进行简单的SQL操作，查看pg日志 ' \
                   'expect:打印的执行计划、解析树、重写结果信息未缩进展示----'
        self.log.info(step_txt)
        sql = f'create table {self.tb_name} (id int);' \
            f'insert into {self.tb_name} values(1);'
        result = self.pri_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result,
                      '执行失败:' + step_txt)
        self.log.info('----查看pg_log----')
        shell_cmd = f'''ls -t {self.dir_new} | head -1'''
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name} | grep -E " \
            f"'{self.suc_flag1}|{self.suc_flag2}|{self.suc_flag3}' -A 10"
        self.log.info(shell_cmd)
        result = self.pri_root.sh(shell_cmd).result()
        self.log.info(result)
        self.assertNotEqual('', result, '执行失败:' + step_txt)
        self.assertNotIn(self.suc_flag4, result, '执行失败:' + step_txt)
        self.assertNotIn(self.suc_flag5, result, '执行失败:' + step_txt)
        self.assertNotIn(self.suc_flag6, result, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----恢复参数debug_print_plan expect: 成功----'
        self.log.info(step1_txt)
        msg1 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'debug_print_plan={self.para1}')
        msg2 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'debug_print_parse={self.para2}')
        msg3 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'debug_print_rewritten='
                                         f'{self.para3}')
        msg4 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'debug_pretty_print={self.para4}')

        step2_txt = '----清理表数据 expect: 成功----'
        self.log.info(step2_txt)
        drop_sql = f"drop table if exists {self.tb_name};"
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)

        step3_txt = '----还原参数log_directory; expect:修改成功----'
        self.log.info(step3_txt)
        msg5 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"log_directory='{self.dir_init}'",
                                         single=True)

        step_txt = '----断言teardown执行成功----'
        self.log.info(step_txt)
        self.assertTrue(msg1, '执行失败:' + step1_txt)
        self.assertTrue(msg2, '执行失败:' + step1_txt)
        self.assertTrue(msg3, '执行失败:' + step1_txt)
        self.assertTrue(msg4, '执行失败:' + step1_txt)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_result,
                      '执行失败:' + step2_txt)
        self.assertTrue(msg5, '执行失败:' + step3_txt)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

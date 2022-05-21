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
Case Name   : 查看参数debug_print_rewritten的默认值为off
Description :
    1.查看参数debug_print_rewritten的默认值
    2.进行简单的SQL操作，查看pg日志
Expect      :
    1.查看参数debug_print_rewritten的默认值,结果为off
    2.进行简单的SQL操作，查看pg日志，未打印重写结果关键信息“LOG:  rewritten parse tree”
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
        self.tb_name = 'tb_Guc_ErrorLog_Case0085'
        self.suc_flag = 'LOG:  rewritten parse tree'
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    'pg_errorlog_case0085')

    def test_main(self):
        step_txt = '----查看参数log_directory；expect：查询成功----'
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

        step_txt = '----step1:查看参数debug_print_rewritten的默认值expect：结果为off----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show debug_print_rewritten;')
        self.log.info(f"debug_print_rewritten is {result}")
        self.para1 = result.strip().splitlines()[-2].strip()
        self.assertEqual('off', self.para1, '执行失败:' + step_txt)

        step_txt = '----step2:进行简单的SQL操作，查看pg日志 expect:未打印重写结果关键信息----'
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
        shell_cmd = f"cat {file_name} | grep '{self.suc_flag}' -A 10"
        self.log.info(shell_cmd)
        result = self.pri_root.sh(shell_cmd).result()
        self.log.info(result)
        self.assertEqual('', result, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt1 = '----清理表数据; expect:清理成功----'
        self.log.info(step_txt1)
        drop_sql = f"drop table if exists {self.tb_name};"
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)

        step_txt2 = '----还原参数log_directory; expect:修改成功----'
        self.log.info(step_txt2)
        msg2 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"log_directory='{self.dir_init}'",
                                         single=True)

        step_txt = '----断言teardown执行成功----'
        self.log.info(step_txt)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_result,
                      "执行失败" + step_txt1)
        self.assertTrue(msg2, '执行失败:' + step_txt2)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

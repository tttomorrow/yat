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
Case Name   : 设置参数log_checkpoints的值为on，自动检查点日志验证
Description :
    1.修改参数log_checkpoints为on
    2.设置enable_incremental_checkpoint、incremental_checkpoint_timeout
    3.等待incremental_checkpoint_timeout时间，查看pg日志
Expect      :
    1.查看参数log_checkpoints的默认值，为off
    2.设置enable_incremental_checkpoint、incremental_checkpoint_timeout
    3.等待incremental_checkpoint_timeout时间，查看pg日志，打印检查点和重启点的统计
History     :
    modified：2022-3-29 by 5328113;修改pg_log目录，避免其他日志影响
"""
import os
import re
import time
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
        self.suc_flag1 = 'CreateCheckPoint PrintCkpXctlControlFile'
        self.match_msg1 = 'checkpoint starting: time'
        self.match_msg2 = 'checkpoint complete: wrote .* buffers (.*%); ' \
                          '.* transaction log file(s) added, .* removed, ' \
                          '.* recycled; write=.* s, sync=.* s, total=.* s; ' \
                          'sync files=.*, longest=.* s, average=.* s'
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    'pg_errorlog_case0098')

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

        step_txt = '----step1:查询log_checkpoints参数默认值 expect:默认值为off----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql(
            'show enable_incremental_checkpoint;')
        self.log.info(f"enable_incremental_checkpoint is {result}")
        self.para2 = result.strip().splitlines()[-2].strip()
        result = self.pri_sh.execut_db_sql(
            'show incremental_checkpoint_timeout;')
        self.log.info(f"incremental_checkpoint_timeout is {result}")
        self.para3 = result.strip().splitlines()[-2].strip()
        result = self.pri_sh.execut_db_sql('show log_checkpoints;')
        self.log.info(f"log_checkpoints is {result}")
        self.para1 = result.strip().splitlines()[-2].strip()

        step_txt = '----step2:修改参数log_checkpoints为on expect:设置成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'log_checkpoints=on')
        self.assertTrue(msg, '执行失败:' + step_txt)

        self.log.info('----重启数据库，避免其他用例关键日志信息影响断言----')
        self.pri_sh.restart_db_cluster()

        step_txt = '----step2:设置enable_incremental_checkpoint、' \
                   'incremental_checkpoint_timeout expect:设置成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'enable_incremental_checkpoint=on')
        self.assertTrue(msg, '执行失败:' + step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'incremental_checkpoint_timeout=30s')
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step3:等待incremental_checkpoint_timeout时间，查看pg日志 ' \
                   'expect:打印检查点和重启点的统计----'
        self.log.info(step_txt)
        time.sleep(30)
        self.log.info('----查看pg_log----')
        shell_cmd = f'''ls -t {self.dir_new} | head -1'''
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name} | grep '{self.suc_flag1}' -C 20"
        self.log.info(shell_cmd)
        result = self.pri_root.sh(shell_cmd).result()
        self.log.info(result)
        self.assertNotEqual('', result, '执行失败:' + step_txt)
        self.assertIn(self.match_msg1, result, "执行失败" + step_txt)
        match_result = len(re.findall(self.match_msg2, result))
        self.assertGreater(1, match_result, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----恢复参数 ;expect :恢复成功----'
        self.log.info(step1_txt)
        msg1 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'enable_incremental_checkpoint='
                                         f'{self.para2}')
        msg2 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'incremental_checkpoint_timeout='
                                         f'{self.para3}')
        msg3 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'log_checkpoints={self.para1}')

        step2_txt = '----还原参数log_directory; expect:修改成功----'
        self.log.info(step2_txt)
        msg4 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"log_directory='{self.dir_init}'",
                                         single=True)

        step_txt = '----断言teardown执行成功----'
        self.log.info(step_txt)
        self.assertTrue(msg1, '执行失败:' + step1_txt)
        self.assertTrue(msg2, '执行失败:' + step1_txt)
        self.assertTrue(msg3, '执行失败:' + step1_txt)
        self.assertTrue(msg4, '执行失败:' + step2_txt)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

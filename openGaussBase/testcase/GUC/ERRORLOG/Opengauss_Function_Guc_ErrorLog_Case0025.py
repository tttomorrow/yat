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
Case Name   : 参数log_file_mode的值为0640，允许管理员所在用户组成员只能读日志文件，非管理员所在用户组成员不能读日志文件
Description :
    1.参数log_file_mode的值设置为640
    2.重启数据库，新生成pg日志
    3.验证新生成日志文件权限
Expect      :
    1.参数log_file_mode的值设置为640
    2.重启数据库，新生成pg日志
    3.验证新生成日志文件权限
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
                                    'pg_errorlog_case0025')

    def test_main(self):
        step_txt = '----查询log_file_mode初始值----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show log_directory;')
        self.log.info(f"log_directory is {result}")
        self.dir_init = result.strip().splitlines()[-2].strip()
        result = self.pri_sh.execut_db_sql('show log_file_mode;')
        self.log.info(f"log_file_mode is {result}")
        self.para_init = result.strip().splitlines()[-2]

        step_txt = '----step0:修改参数log_directory; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"log_directory='{self.dir_new}'",
                                        single=True)
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step1:修改参数log_file_mode为0640; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f'log_file_mode=0640')
        self.assertTrue(msg, '执行失败:' + step_txt)

        self.log.info('----step2:重启数据库，新生成pg日志----')
        restart_flag = self.pri_sh.restart_db_cluster()
        self.assertTrue(restart_flag)

        step_txt = '----step3:查询新日志权限是否是0640----'
        self.log.info(step_txt)
        shell_cmd = f'ls -t {self.dir_new} | head -1'
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"ls -al {file_name}|tr -s ' '|cut -d ' ' -f 1"
        file_mode = self.pri_root.sh(shell_cmd).result()
        self.log.info(file_mode)
        self.assertEqual(file_mode, '-rw-r-----', '执行失败:' + step_txt)

    def tearDown(self):
        step_txt1 = '----还原参数log_directory; expect:修改成功----'
        self.log.info(step_txt1)
        msg1 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"log_directory='{self.dir_init}'",
                                         single=True)

        step_txt2 = '----还原参数log_file_mode为初始值; expect:修改成功----'
        self.log.info(step_txt2)
        msg2 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'log_file_mode={self.para_init}')
        step_txt3 = '----重启数据库----'
        self.log.info(step_txt3)
        restart_flag = self.pri_sh.restart_db_cluster()

        step_txt = '----断言teardown执行成功----'
        self.log.info(step_txt)
        self.assertTrue(msg1, '执行失败:' + step_txt1)
        self.assertTrue(msg2, '执行失败:' + step_txt2)
        self.assertTrue(restart_flag, '执行失败:' + step_txt3)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

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
Case Name   : 参数log_timezone默认值验证
Description :
    1.查看参数log_timezone值
    2.查看pg日志打印时间
Expect      :
    1.查看参数log_timezone值为PRC
    2.查看pg日志打印时间为PRC时区时间
History     :
"""
import datetime
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
                                    'pg_errorlog_case0115')

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

        step_txt = '----step1:查看参数log_timezone的默认值 expect:默认值为PRC----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show log_timezone;')
        self.log.info(f"log_timezone is {result}")
        self.para1 = result.strip().splitlines()[-2].strip()
        self.assertEqual('PRC', self.para1, '执行失败:' + step_txt)

        step_txt = '----step2: 查看pg日志打印时间' \
                   'expect: 日志时间为PRC时区时间---'
        self.log.info(step_txt)
        self.log.info('----查看当前系统时间----')
        shell_cmd = 'date -R ;date "+%Y-%m-%d %H:%M:%S"'
        result = self.pri_root.sh(shell_cmd).result()
        sys_time = result.splitlines()[-1].strip()
        self.log.info(sys_time)
        date1 = datetime.datetime.strptime(sys_time, '%Y-%m-%d %H:%M:%S')

        self.log.info('----查看pg_log----')
        shell_cmd = f'''ls -t {self.dir_new} | head -1'''
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"tail -n 1 {file_name}|tr -s ' '|cut -d ' ' -f 1-2"
        self.log.info(shell_cmd)
        result = self.pri_root.sh(shell_cmd).result()[0:19]
        self.log.info(result)
        date2 = datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
        delta = date1 - date2
        self.log.info(delta)
        self.assertTrue(abs(delta.total_seconds()) < 60, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----还原参数log_directory; expect:修改成功----'
        self.log.info(step1_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"log_directory='{self.dir_init}'",
                                        single=True)
        step_txt = '----断言teardown执行成功----'
        self.log.info(step_txt)
        self.assertTrue(msg, '执行失败:' + step1_txt)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

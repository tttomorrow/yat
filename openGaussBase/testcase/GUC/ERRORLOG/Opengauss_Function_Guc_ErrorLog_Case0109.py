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
Case Name   : 查看参数log_lock_waits的默认值为off
Description :
    1.查看参数log_lock_waits的默认值
    2.设置deadlock_timeout参数为10S
    3.创建测试表并插入数据
    4.打开会话，进行表相关数据update操作并等待30s
    5.打开另一会话，对步骤3的表记录再次进行update操作，并等待30s
    6.等待deadlocke_timeout时间，查看pg日志
Expect      :
    1.查看参数log_lock_waits的默认值为off
    2.设置deadlock_timeout参数为10S成功
    3.创建测试表并插入数据成功
    4.打开会话，进行表相关数据update操作并等待30s
    5.打开另一会话，对步骤3的表记录再次进行update操作，并等待30s
    6.等待deadlocke_timeout时间，查看pg日志未打印锁等待记录消息
History     :
    modified：2022-3-29 by 5328113;修改pg_log目录，避免其他日志影响
"""
import os
import re
import time
import unittest

from testcase.utils.ComThread import ComThread
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
        self.tb_name = 'tb_Guc_ErrorLog_Case0109'
        self.match_msg1 = 'thread .* still waiting for ShareLock ' \
                          'on transaction .* after .* ms'
        self.match_msg2 = 'thread .* acquired ShareLock ' \
                          'on transaction .* after .* ms'
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    'pg_errorlog_case0109')

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

        step_txt = '----step1:查看参数log_lock_waits的默认值 expect：默认为off----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show deadlock_timeout;')
        self.log.info(f"deadlock_timeout is {result}")
        self.para2 = result.strip().splitlines()[-2]
        result = self.pri_sh.execut_db_sql('show log_lock_waits;')
        self.log.info(f"log_lock_waits is {result}")
        self.para1 = result.strip().splitlines()[-2].strip()
        self.assertEqual('off', self.para1, '执行失败:' + step_txt)

        step_txt = '----step2:设置设置deadlock_timeout参数为10S expect:设置成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'deadlock_timeout=10s')
        self.assertTrue(msg, '执行失败:' + step_txt)

        self.log.info('----重启数据库，避免其他用例关键日志信息影响断言----')
        self.pri_sh.restart_db_cluster()

        step_txt = '----step3: 创建测试表并插入数据，expect: 创建成功----'
        self.log.info(step_txt)
        create_sql = f'drop table if exists {self.tb_name};' \
            f'create table {self.tb_name}(id int,name text);' \
            f'insert into {self.tb_name} values(1,\'test1\');'
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn('INSERT 0 1', create_result, '执行失败:' + step_txt)

        step4_txt = '----step4: 打开会话，打开会话，进行表相关数据update操作并等待30s ' \
                    'expect:操作成功 ----'
        self.log.info(step4_txt)
        lock_sql1 = f'start transaction;' \
            f'update {self.tb_name} set name=\'test11\' where id =1;' \
            f'select pg_sleep(20);' \
            f'end;'
        session1 = ComThread(self.pri_sh.execut_db_sql, args=(lock_sql1,))
        session1.setDaemon(True)
        session1.start()
        time.sleep(1)

        step_txt = '----step5: 打开另一会话，对步骤3的表记录再次进行update操作 expect: 超时等待---'
        self.log.info(step_txt)
        lock_sql2 = f'update {self.tb_name} set name=\'test12\' where id =1;'
        lock_result = self.pri_sh.execut_db_sql(lock_sql2)
        self.log.info(lock_result)

        self.log.info('----会话1（步骤4）执行结果验证----')
        session1.join()
        session1_result = session1.get_result()
        self.log.info(session1_result)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, session1_result,
                      '执行失败:' + step4_txt)

        step_txt = '----step6: 等待deadlocke_timeout时间，查看pg日志 ' \
                   'expect: 打印未打印等待记录消息---'
        self.log.info('----查看pg_log----')
        shell_cmd = f'''ls -t {self.dir_new} | head -1'''
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"tail -n 30 {file_name} "
        self.log.info(shell_cmd)
        result = self.pri_root.sh(shell_cmd).result()
        self.log.info(result)
        match_result1 = len(re.findall(self.match_msg1, result))
        match_result2 = len(re.findall(self.match_msg2, result))
        self.assertEqual(0, match_result1, "执行失败" + step_txt)
        self.assertEqual(0, match_result2, "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清除表数据 expect:成功----'
        self.log.info(step1_txt)
        drop_sql = f'drop table if exists {self.tb_name};'
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)

        step2_txt = '----恢复参数 expect:成功----'
        self.log.info(step2_txt)
        msg1 = self.pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f'deadlock_timeout={self.para2}')

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

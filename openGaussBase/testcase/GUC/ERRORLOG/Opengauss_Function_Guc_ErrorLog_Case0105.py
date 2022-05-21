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
Case Name   : 查看参数log_hostname的默认值为off
Description :
    1.查看参数log_hostname的默认值
    2.设置log_connections、log_disconnections参数为on
    3.主机gsql -h连接主机、结束连接，查看主机pg日志
    4.备机gsql -h连接主机、结束连接，查看主机pg日志
Expect      :
    1.查看参数log_hostname的默认值为off
    2.设置log_connections、log_disconnections参数为on，设置成功
    3.主机gsql -h连接主机、结束连接，查看主机pg日志，连接、断连信息展示host为主机IP
    4.备机gsql -h连接主机、结束连接，查看主机pg日志，连接、断连信息展示host为备机IP
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

pri_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf('Standby' not in pri_sh.get_db_cluster_status('detail'),
                 'Single node, and subsequent codes are not executed.')
class ErrorLog(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:start----')
        self.pri_dbuser = Node('PrimaryDbUser')
        self.sta1_dbuser = Node('Standby1DbUser')
        self.pri_root = Node('PrimaryRoot')
        self.common = Common()
        self.constant = Constant()
        self.pri_ip = self.pri_dbuser.db_host
        self.sta1_ip = self.sta1_dbuser.db_host
        self.pri_hostname = self.pri_dbuser.sh('hostname').result()
        self.sta1_hostname = self.sta1_dbuser.sh('hostname').result()
        self.flag_msg = "-E 'connection received|disconnection:'"
        self.user = self.pri_dbuser.db_user
        self.password = self.pri_dbuser.db_password
        self.con_msg = f'-h {self.pri_ip} -U {self.user} -W {self.password}'
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    'pg_errorlog_case0105')

    def test_main(self):
        step_txt = '----查看参数log_directory默认值----'
        self.log.info(step_txt)
        result = pri_sh.execut_db_sql('show log_directory;')
        self.log.info(f"log_directory is {result}")
        self.dir_init = result.strip().splitlines()[-2].strip()

        step_txt = '----step0:修改参数log_directory; expect:修改成功----'
        self.log.info(step_txt)
        msg = pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        f"log_directory='{self.dir_new}'",
                                        single=True)
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step1：查看参数log_hostname的默认值 expect：值为off----'
        self.log.info(step_txt)
        result = pri_sh.execut_db_sql('show log_connections;')
        self.log.info(f"log_connections is {result}")
        self.para2 = result.strip().splitlines()[-2]
        result = pri_sh.execut_db_sql('show log_disconnections;')
        self.log.info(f"log_disconnections is {result}")
        self.para3 = result.strip().splitlines()[-2]
        result = pri_sh.execut_db_sql('show log_hostname;')
        self.log.info(f"log_checkpoints is {result}")
        self.para1 = result.strip().splitlines()[-2].strip()
        self.assertEqual('off', self.para1, '执行失败:' + step_txt)

        step_txt = '----step2:设置log_connections、log_disconnections' \
                   '参数为on expect:设置成功----'
        self.log.info(step_txt)
        msg = pri_sh.execute_gsguc('reload',
                                   self.constant.GSGUC_SUCCESS_MSG,
                                   'log_connections=on')
        self.assertTrue(msg, '执行失败:' + step_txt)
        msg = pri_sh.execute_gsguc('reload',
                                   self.constant.GSGUC_SUCCESS_MSG,
                                   'log_disconnections=on')
        self.assertTrue(msg, '执行失败:' + step_txt)

        self.log.info('----重启数据库，避免其他用例关键日志信息影响断言----')
        pri_sh.restart_db_cluster()

        step_txt = '----step3: 主机gsql -h连接主机、结束连接，查看主机pg日志 ' \
                   'expect:连接、断连信息展示host为主机IP ----'
        self.log.info(step_txt)
        sql = f'\q'
        result = pri_sh.execut_db_sql(sql, sql_type=self.con_msg)
        self.log.info(result)
        self.assertEqual('', result, '执行失败:' + step_txt)
        self.log.info('----查看pg_log----')
        shell_cmd = f'''ls -t {self.dir_new} | head -1'''
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name} | grep {self.flag_msg}"
        self.log.info(shell_cmd)
        result = self.pri_root.sh(shell_cmd).result()
        self.log.info(result)
        self.assertIn('host=' + self.pri_ip, result, '执行失败:' + step_txt)
        self.assertNotIn('host=' + self.pri_hostname, result,
                         '执行失败:' + step_txt)

        step_txt = '----step3: 备机gsql -h连接主机、结束连接，查看主机pg日志 ' \
                   'expect:连接、断连信息展示host为备机IP ----'
        self.log.info(step_txt)
        sql = f'\q'
        result = pri_sh.execut_db_sql(sql, sql_type=self.con_msg)
        self.log.info(result)
        self.assertEqual('', result, '执行失败:' + step_txt)
        self.log.info('----查看pg_log----')
        shell_cmd = f'''ls -t {self.dir_new} | head -1'''
        file_name = os.path.join(self.dir_new,
                                 self.pri_root.sh(shell_cmd).result())
        self.log.info(file_name)
        shell_cmd = f"cat {file_name} | grep {self.flag_msg}"
        self.log.info(shell_cmd)
        result = self.pri_root.sh(shell_cmd).result()
        self.log.info(result)
        self.assertIn('host=' + self.sta1_ip, result, '执行失败:' + step_txt)
        self.assertNotIn('host=' + self.sta1_hostname, result,
                         '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----恢复参数 ;expect :恢复成功----'
        self.log.info(step1_txt)
        msg1 = pri_sh.execute_gsguc('reload',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f'log_connections={self.para2}')
        msg2 = pri_sh.execute_gsguc('reload',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f'log_disconnections={self.para3}')

        step2_txt = '----还原参数log_directory; expect:修改成功----'
        self.log.info(step2_txt)
        msg3 = pri_sh.execute_gsguc('reload',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"log_directory='{self.dir_init}'",
                                         single=True)

        step_txt = '----断言teardown执行成功----'
        self.log.info(step_txt)
        self.assertTrue(msg1, '执行失败:' + step1_txt)
        self.assertTrue(msg2, '执行失败:' + step1_txt)
        self.assertTrue(msg3, '执行失败:' + step2_txt)

        self.log.info(f'----{os.path.basename(__file__)}:end----')

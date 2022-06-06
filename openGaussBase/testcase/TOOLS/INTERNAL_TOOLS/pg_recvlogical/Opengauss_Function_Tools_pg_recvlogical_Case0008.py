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
Case Type   : 系统内部使用工具
Case Name   : 逻辑复制pg_recvlogical -w 参数指定时，不使用密码进行连接，
              连接成功
Description :
    1.修改参数wal_level为logical;enable_slot_log为on
    2.主机pg_hba.conf文件中配置逻辑复制的用户白名单
    3.逻辑复制pg_recvlogical -w 参数指定
    4.清理环境
Expect      :
    1.修改成功
    2.配置成功
    3.本机初始用户不输入密码连接成功
    4.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(), '单机环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Tools_pg_recvlogical_Case0008开始执行----')
        self.constant = Constant()
        self.common = Common()
        self.primary_node = Node('PrimaryDbUser')
        self.username = self.primary_node.ssh_user
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.slot_name = 'solt_pg_recvlogical_0008'
        self.ha_port = str(int(self.primary_node.db_port) + 1)
        self.default_value1 = self.common.show_param('wal_level')
        self.default_value2 = self.common.show_param('enable_slot_log')

    def test_standby(self):
        text = '----step1:修改wal_level为logical;enable_slot_log为on;' \
               'expect: 修改成功----'
        self.log.info(text)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'enable_slot_log =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        self.assertTrue(restart_msg, '执行失败:' + text)

        text = '----step2:主机配置逻辑复制的用户;expect:配置成功----'
        self.log.info(text)
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
                  f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "local  replication  {self.primary_node.ssh_user}   ' \
                  f'trust"'
        self.log.info(guc_cmd)
        guc_res = self.primary_node.sh(guc_cmd).result()
        self.log.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败：' + text)
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
                  f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "host  replication  {self.primary_node.ssh_user}   ' \
                  f'127.0.0.1/32   trust"'
        self.log.info(guc_cmd)
        guc_res = self.primary_node.sh(guc_cmd).result()
        self.log.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败：' + text)
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
                  f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "host  replication  {self.primary_node.ssh_user}   ' \
                  f'::1/128   trust"'
        self.log.info(guc_cmd)
        guc_res = self.primary_node.sh(guc_cmd).result()
        self.log.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败：' + text)

        text = '----step4:逻辑复制pg_recvlogical -w 参数指定;' \
               'expect:不输入密码连接成功----'
        self.log.info(text)
        action_option = ['--create', '--start -s 2 -f - -v', '--drop']
        for act in action_option:
            create_cmd = f"pg_recvlogical " \
                         f"-d postgres " \
                         f"-S {self.slot_name} " \
                         f"-p {self.ha_port} " \
                         f"-w " \
                         f"{act} "
            execute_cmd = f'''source {macro.DB_ENV_PATH}
                       expect <<EOF
                       set timeout 30
                       spawn {create_cmd}
                       expect eof\n''' + '''EOF'''
            self.log.info(execute_cmd)
            exec_msg = self.primary_node.sh(execute_cmd).result()
            self.log.info(exec_msg)
            if act == action_option[1]:
                self.assertIn('confirming write up to', exec_msg,
                              '执行失败:' + text)
            self.assertNotIn('FATAL', exec_msg, '执行失败:' + text)

    def tearDown(self):
        text = '----step4:清理环境;expect:清理环境完成----'
        self.log.info(text)
        self.log.info('----主机pg_hba.conf文件恢复----')
        guc_cmd1 = f'source {macro.DB_ENV_PATH}; ' \
                   f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                   f'-h "local  replication  {self.primary_node.ssh_user}"'
        self.log.info(guc_cmd1)
        guc_res1 = self.primary_node.sh(guc_cmd1).result()
        self.log.info(guc_res1)
        guc_cmd2 = f'source {macro.DB_ENV_PATH}; ' \
                   f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                   f'-h "host  replication  {self.primary_node.ssh_user}   ' \
                   f'127.0.0.1/32"'
        self.log.info(guc_cmd2)
        guc_res2 = self.primary_node.sh(guc_cmd2).result()
        self.log.info(guc_res2)
        guc_cmd3 = f'source {macro.DB_ENV_PATH}; ' \
                   f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                   f'-h "host  replication  {self.primary_node.ssh_user}   ' \
                   f'::1/128"'
        self.log.info(guc_cmd3)
        guc_res3 = self.primary_node.sh(guc_cmd3).result()
        self.log.info(guc_res3)

        self.log.info('----修改参数wal_level,enable_slot_log为初始值----')
        mod_msg1 = Primary_SH.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f'wal_level={self.default_value1}')
        mod_msg2 = Primary_SH.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f'enable_slot_log='
                                            f'{self.default_value2}')
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()

        self.log.info('----断言tearDown执行成功----')
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res1,
                      '执行失败：' + text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res2,
                      '执行失败：' + text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res3,
                      '执行失败：' + text)
        self.assertTrue(mod_msg1, '执行失败:' + text)
        self.assertTrue(mod_msg2, '执行失败:' + text)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_pg_recvlogical_Case0008 finish----')

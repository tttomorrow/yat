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
Case Name   : 逻辑复制pg_recvlogical ,连接参数指定正确时
              --password/--username/--port/--host/--dbname，连接成功
Description :
    1.修改参数wal_level为logical;enable_slot_log为on
    2.主机pg_hba.conf文件中配置逻辑复制的用户白名单
    3.连接参数指定正确--password/--username/--port/--host/--dbname
    4.清理环境
Expect      :
    1.修改成功
    2.配置成功
    3.连接成功
    4.清理环境完成
History     :
"""
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
            '----Opengauss_Function_Tools_pg_recvlogical_Case0007开始执行----')
        self.constant = Constant()
        self.common = Common()
        self.primary_node = Node('PrimaryDbUser')
        self.u_name = 'u_pg_recvlogical_0007'
        self.slot_name = 'solt_pg_recvlogical_0007'
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
        result = Primary_SH.restart_db_cluster()
        self.assertTrue(result, '执行失败' + text)

        text = '----step2:主机配置逻辑复制的用户;expect: 配置成功----'
        self.log.info(text)
        create_cmd = f"drop user if exists {self.u_name};" \
                     f"create user {self.u_name} replication password " \
                     f"'{macro.COMMON_PASSWD}';"
        sql_cmd = Primary_SH.execut_db_sql(create_cmd)
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
                  f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "host  replication  {self.u_name}  ' \
                  f'{self.primary_node.db_host}/32  sha256"'
        self.log.info(guc_cmd)
        guc_res = self.primary_node.sh(guc_cmd).result()
        self.log.info(guc_res)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败：' + text)

        text = '----step3:连接参数指定正确--password/--username/--port/' \
               '--host/--dbname;expect:连接成功----'
        self.log.info(text)
        action_option = ['--create', '--start -s 2 -f - -v', '--drop']
        for act in action_option:
            create_cmd = f"pg_recvlogical " \
                         f"--dbname={self.primary_node.db_name} " \
                         f"--host={self.primary_node.db_host} " \
                         f"--username={self.u_name} " \
                         f"-S {self.slot_name} " \
                         f"--port={self.ha_port} " \
                         f"{act} " \
                         f"--password "
            execute_cmd = f'''source {macro.DB_ENV_PATH}
                       expect <<EOF
                       set timeout 30
                       spawn {create_cmd}
                       expect "Password:"
                       send "{macro.COMMON_PASSWD}\\n"
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
        self.log.info('----删除用户,逻辑复制槽----')
        self.log.info(text)
        del_cmd = Primary_SH.execut_db_sql(f"drop user if exists "
                                           f"{self.u_name};"
                                           f"select * from "
                                           f"pg_drop_replication_slot"
                                           f"('{self.slot_name}');")
        self.log.info(del_cmd)
        sql_cmd = Primary_SH.execut_db_sql(f"select * from "
                                           f"pg_replication_slots;")
        self.log.info(sql_cmd)

        self.log.info('----主机pg_hba.conf文件恢复----')
        guc_cmd = f'source {macro.DB_ENV_PATH}; ' \
                  f'gs_guc reload -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "host  replication  {self.u_name}  ' \
                  f'{self.primary_node.db_host}/32"'
        self.log.info(guc_cmd)
        guc_res = self.primary_node.sh(guc_cmd).result()
        self.log.info(guc_res)

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
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, del_cmd,
                      '执行失败:' + text)
        self.assertNotIn(self.slot_name, sql_cmd, '执行失败:' + text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, guc_res,
                      '执行失败：' + text)
        self.assertTrue(mod_msg1, '执行失败:' + text)
        self.assertTrue(mod_msg2, '执行失败:' + text)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '----Opengauss_Function_Tools_pg_recvlogical_Case0007 finish----')

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
Case Type   : security-auditing
Case Name   : 统一审计策略：对table对象的insert行为的审计，过滤user
Description :
    1.系统管理员用户创建两个用户
    2.系统管理员用户创建表，并赋予用户权限
    3.系统管理员用户创建资源标签
    4.系统管理员用户创建统一审计策略，过滤用户1
    5.用户1登录数据库执行insert语句
    6.用户2登录数据库执行insert语句
    7.查看/var/log/postgresql日志中是否审计了用户1的insert操作
Expect      :
    1.用户创建成功
    2.建表成功，赋予权限
    3.创建成功
    4.创建成功
    5.执行成功
    6.执行成功
    7.日志中审计到了用户1的insert操作的操作，未审计到用户2的insert操作的操作
History     :
"""
import os
import re
import unittest
from time import sleep
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '---Opengauss_Function_Security_Auditing_Case0133 start---')
        self.userNode = Node(node='PrimaryDbUser')
        self.primary_root = Node(node='PrimaryRoot')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.user1 = 'u01_security_auditing_0133'
        self.user2 = 'u02_security_auditing_0133'
        self.table = 'table_security_auditing_0133'
        self.res_label = 'rl_security_auditing_0133'
        self.audit_policy = 'ap_security_auditing_0133'
        self.log_file = '/var/log/postgresql'
        self.config_path = '/etc'
        self.default_adss = self.common.show_param('audit_dml_state_select')
        self.default_adml = self.common.show_param('audit_dml_state')
        self.default_policy = self.common.show_param('enable_security_policy')
        self.default_facility = self.common.show_param('syslog_facility')

    def test_encrypted(self):
        text = '---step1.1:备份配置文件并配置日志归档;expect:成功---'
        self.logger.info(text)
        cp_cmd = f"cp {os.path.join(self.config_path, 'rsyslog.conf')} " \
            f"{os.path.join(self.config_path, 'rsyslog_bak.conf')}"
        self.primary_root.sh(cp_cmd).result()
        mod_exe = f"echo 'local0.*  {self.log_file}' >> " \
            f"{os.path.join(self.config_path, 'rsyslog.conf')};" \
            f"service rsyslog restart"
        self.logger.info(mod_exe)
        mod_msg = self.primary_root.sh(mod_exe).result()
        self.logger.info(mod_msg)
        self.assertIn('restart rsyslog.service', mod_msg, '执行失败' + text)

        text = '---step1.2:设置enable_security_policy=on;expect:成功---'
        self.logger.info(text)
        result = self.sh_primy.execute_gsguc('reload',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f'enable_security_policy=on')
        self.assertEqual(True, result, '执行失败' + text)

        text = '---step1.3:设置audit_dml_state_select=1;expect:成功---'
        self.logger.info(text)
        result = self.sh_primy.execute_gsguc('reload',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f'audit_dml_state_select=1')
        self.assertEqual(True, result, '执行失败' + text)

        text = '---step1.4:设置audit_dml_state=1;expect:成功---'
        self.logger.info(text)
        result = self.sh_primy.execute_gsguc('reload',
                                             self.constant.GSGUC_SUCCESS_MSG,
                                             f'audit_dml_state=1')
        self.assertEqual(True, result, '执行失败' + text)

        text = '---step1.5:syslog_facility=local0;expect:成功---'
        self.logger.info(text)
        if self.default_facility != 'local0':
            result = self.sh_primy.execute_gsguc('reload',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f'syslog_facility=local0')
            self.assertEqual(True, result, '执行失败' + text)

        text = '---step1.6:系统管理员用户创建两个用户;expect:成功---'
        self.logger.info(text)
        sql_cmd1 = f'drop user if exists {self.user1} cascade;' \
            f'create user {self.user1} password ' \
            f'\'{macro.COMMON_PASSWD}\';' \
            f'drop user if exists {self.user2} cascade;' \
            f'create user {self.user2} ' \
            f'password \'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        self.assertIn('CREATE ROLE', msg1, '执行失败' + text)

        text = '---step2:系统管理员用户创建表，并赋予用户权限;expect:成功---'
        self.logger.info(text)
        sql_cmd2 = f'drop table if exists {self.table} cascade;' \
            f'create table {self.table}(id int,name varchar(30));' \
            f'insert into {self.table} values(6,\'{self.user1}\');' \
            f'grant all privileges on {self.table} to {self.user1};' \
            f'grant all privileges on {self.table} to {self.user2};'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.assertTrue(msg2.count('GRANT') == 2, '执行失败' + text)

        text = '---step3:系统管理员用户创建资源标签;expect:成功---'
        self.logger.info(text)
        sql_cmd3 = f'drop resource label if exists {self.res_label};' \
            f'create resource label {self.res_label} add table({self.table});'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertIn('CREATE RESOURCE LABEL', msg3, '执行失败' + text)

        text = '---step4:系统管理员用户创建统一审计策略，过滤用户1;expect:成功---'
        self.logger.info(text)
        sql_cmd4 = f'drop audit policy if exists {self.audit_policy};' \
            f'create audit policy {self.audit_policy} access insert' \
            f' on label({self.res_label}) filter on roles({self.user1});'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.assertIn('CREATE AUDIT POLICY', msg4, '执行失败' + text)

        text = '---step5:用户1登录数据库执行insert语句;expect:成功---'
        self.logger.info(text)
        sql_cmd5 = f'insert into {self.table} values(2,\'lily\');'
        excute_cmd5 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p {self.userNode.db_port} ' \
            f'-U {self.user1} -W {macro.COMMON_PASSWD} -c "{sql_cmd5}"'
        self.logger.info(excute_cmd5)
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.logger.info(msg5)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg5, '执行失败' + text)

        text = '---step6:用户2登录数据库执行insert语句;expect:成功---'
        self.logger.info(text)
        sql_cmd6 = f'insert into {self.table} values(3,\'bob\');'
        excute_cmd6 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p {self.userNode.db_port} ' \
            f'-U {self.user2} -W {macro.COMMON_PASSWD} -c "{sql_cmd6}"'
        self.logger.info(excute_cmd6)
        msg6 = self.userNode.sh(excute_cmd6).result()
        self.logger.info(msg6)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg6, '执行失败' + text)

        text = '--step7:查看postgresql日志中是否审计了用户1操作;expect:成功--'
        self.logger.info(text)
        sleep(2)
        exe_cmd7 = f'cat {self.log_file}'
        msg7 = self.primary_root.sh(exe_cmd7).result()
        self.logger.info(msg7)
        assert1 = re.search(
            f"user name.*{self.user1}.*access type.*[INSERT].*[OK]", msg7,
            re.S)
        self.assertTrue(assert1, '执行失败:' + text)
        self.assertNotIn(self.user2, msg7, '执行失败:' + text)

    def tearDown(self):
        text1 = '--step1:恢复配置文件信息;expect:成功--'
        self.logger.info(text1)
        recv_cmd = f"mv {os.path.join(self.config_path, 'rsyslog_bak.conf')}" \
            f" {os.path.join(self.config_path, 'rsyslog.conf')};" \
            f"rm -rf {self.log_file};" \
            f"service rsyslog restart"
        self.logger.info(recv_cmd)
        result1 = self.primary_root.sh(recv_cmd).result()

        text2 = '--step2:恢复参数默认值;expect:成功--'
        self.logger.info(text2)
        result2 = self.sh_primy.execute_gsguc('reload',
                            self.constant.GSGUC_SUCCESS_MSG,
                            f'enable_security_policy={self.default_policy}')
        result3 = self.sh_primy.execute_gsguc('reload',
                            self.constant.GSGUC_SUCCESS_MSG,
                            f'audit_dml_state_select={self.default_adss}')
        result4 = self.sh_primy.execute_gsguc('reload',
                            self.constant.GSGUC_SUCCESS_MSG,
                            f'syslog_facility={self.default_facility}')

        text3 = '--step3:清理用户及表;expect:成功--'
        self.logger.info(text3)
        clear_cmd = f'drop audit policy if exists {self.audit_policy};' \
            f'drop resource label if exists {self.res_label};' \
            f'drop table if exists {self.table} cascade;' \
            f'drop user if exists {self.user1} cascade;' \
            f'drop user if exists {self.user2} cascade;'
        clear_msg = self.sh_primy.execut_db_sql(clear_cmd)
        self.logger.info(clear_msg)
        self.assertIn('restart rsyslog.service', result1, '执行失败' + text1)
        self.assertEqual(True, result2, '执行失败' + text2)
        self.assertEqual(True, result3, '执行失败' + text2)
        self.assertEqual(True, result4, '执行失败' + text2)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, clear_msg, text3)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, clear_msg, text3)
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0133 finish----')

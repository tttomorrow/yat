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
Case Name   : 统一审计策略：对table对象的SELECT行为的审计，过滤gsql客户端
Description :
    1.系统管理员用户创建表
    2.系统管理员用户创建资源标签
    3.系统管理员用户创建统一审计策略
    4.用户1通过gsql客户端连接数据库执行select语句，查看/var/log/postgresql日志中是否
    审计了gsql客户端的操作
Expect      :
    1.建表成功
    2.创建成功
    3.创建成功
    4.日志中未审计到gsql客户端的操作
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
            '---Opengauss_Function_Security_Auditing_Case0130 start---')
        self.userNode = Node(node='PrimaryDbUser')
        self.primary_root = Node(node='PrimaryRoot')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.table = 'table_security_auditing_0130'
        self.res_label = 'rl_security_auditing_0130'
        self.audit_policy = 'ap_security_auditing_0130'
        self.log_file = '/var/log/postgresql'
        self.config_path = '/etc'
        self.default_adss = self.common.show_param('audit_dml_state_select')
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
        
        text = '---step1.4:syslog_facility=local0;expect:成功---'
        self.logger.info(text)
        if self.default_facility != 'local0':
            result = self.sh_primy.execute_gsguc('reload',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f'syslog_facility=local0')
            self.assertEqual(True, result, '执行失败' + text)
        
        text = '---step1.5:系统管理员用户创建表;expect:成功---'
        self.logger.info(text)
        sql_cmd2 = f'drop table if exists {self.table} cascade;' \
            f'create table {self.table}(id int,name varchar(30));' \
            f'insert into {self.table} values(6,\'name01\');'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.assertIn('INSERT 0 1', msg2, '执行失败' + text)
        
        text = '---step2:系统管理员用户创建资源标签;expect:成功---'
        self.logger.info(text)
        sql_cmd3 = f'drop resource label if exists {self.res_label};' \
            f'create resource label {self.res_label} add table({self.table});'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertIn('CREATE RESOURCE LABEL', msg3, '执行失败' + text)
        
        text = '---step3:系统管理员用户创建统一审计策略，过滤客户端;expect:成功---'
        self.logger.info(text)
        sql_cmd4 = f'drop audit policy if exists {self.audit_policy};' \
            f'create audit policy {self.audit_policy} access select' \
            f' on label({self.res_label}) filter ' \
            f'on APP(\'gsql\');'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.assertIn('CREATE AUDIT POLICY', msg4, '执行失败' + text)
        
        text = '--step4.1:系统管理员用户连接数据库执行select语句;expect:成功--'
        self.logger.info(text)
        sql_cmd5 = f'select id from {self.table};'
        excute_cmd5 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p {self.userNode.db_port} ' \
            f'-U {self.userNode.db_user} -W {self.userNode.db_password} ' \
            f'-h {self.userNode.db_host} -c "{sql_cmd5}"'
        self.logger.info(excute_cmd5)
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.common.equal_sql_mdg(msg5, 'id', '6', '(1 row)', flag='1')
        text = '--step4.2:查看postgresql日志中审计了gsql客户端的操作;expect:成功--'
        self.logger.info(text)
        sleep(2)
        exe_cmd6 = f'cat {self.log_file}'
        msg6 = self.primary_root.sh(exe_cmd6).result()
        self.logger.info(msg6)
        assert1 = re.search(
            f"user name.*{self.userNode.db_user}.*app_name.*gsql.*"
            f"access type.*[SELECT].*result.*[OK]", msg6, re.S)
        self.assertTrue(assert1, '执行失败:' + text)

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
            f'drop table if exists {self.table} cascade;'
        clear_msg = self.sh_primy.execut_db_sql(clear_cmd)
        self.logger.info(clear_msg)
        self.assertIn('restart rsyslog.service', result1, '执行失败' + text1)
        self.assertEqual(True, result2, '执行失败' + text2)
        self.assertEqual(True, result3, '执行失败' + text2)
        self.assertEqual(True, result4, '执行失败' + text2)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, clear_msg, text3)
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0130 finish----')

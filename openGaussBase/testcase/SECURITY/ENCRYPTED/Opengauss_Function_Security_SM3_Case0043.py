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
Case Type   : security_sm3
Case Name   : 创建用户时的加密算法sm3，认证方式md5，初始用户错误的密码通过JDBC连接数据库
Description :
    1.修改password_encryption_type=3
    2.pg_hba.conf文件中修改认证方式为md5
    3.初始用户通过JDBC错误的密码连接数据库
Expect      :
    1-2.参数设置成功
    3.数据库连接失败，初始用户不支持远程连接
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Security_sm3_Case0043 start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.primary_root = Node(node='PrimaryRoot')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.targetpath = "/home/jdbc_test"
        self.properties = os.path.join(self.targetpath, "jdbc_connect.conf")
        self.java_name = "jdbc_drop_schema_case0001"
        self.script_name = 'bcprov-jdk15on-1.68'
        self.config = os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')
        self.confignew = os.path.join(macro.DB_INSTANCE_PATH,
                                      'pg_hba_bak.conf')
        self.default_msg_list = ''
        self.logger.info('--------检查参数默认值--------')
        check_default = 'show password_encryption_type;'
        default_msg = self.sh_primy.execut_db_sql(check_default)
        self.logger.info(default_msg)
        self.default_msg_list = default_msg.splitlines()[2].strip()
        self.logger.info(self.default_msg_list)
        self.logger.info('--------备份白名单文件---------')
        cp_cmd = f"cp {self.config} {self.confignew}"
        self.userNode.sh(cp_cmd).result()
    
    def test_encrypted(self):
        text = '---step1:修改password_encryption_type=3;expect:成功---'
        self.logger.info(text)
        exe_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            '"password_encryption_type=3"'
        msg1 = self.userNode.sh(exe_cmd1).result()
        self.logger.info(msg1)
        check_cmd = 'show password_encryption_type;'
        check_msg = self.sh_primy.execut_db_sql(check_cmd)
        self.logger.info(check_msg)
        self.common.equal_sql_mdg(check_msg, 'password_encryption_type', '3',
                                  '(1 row)', flag='1')
        text = '---step2:pg_hba.conf文件中增加认证方式为md5;expect:成功---'
        self.logger.info(text)
        exe_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -h ' \
            f'"host {self.userNode.db_name} {self.userNode.ssh_user} ' \
            f'{self.userNode.db_host}/32 md5"'
        msg2 = self.userNode.sh(exe_cmd2).result()
        self.logger.info(msg2)
        exe_cmd3 = f'cat {self.config}'
        msg3 = self.userNode.sh(exe_cmd3).result()
        self.logger.info(msg3)
        self.assertIn(f'host {self.userNode.db_name} {self.userNode.ssh_user} '
                      f'{self.userNode.db_host}/32 md5', msg3,
                      '执行失败:' + text)
        text = '---step3:初始用户通过JDBC错误密码连接数据库;expect:失败---'
        self.logger.info(text)
        self.common.scp_file(self.primary_root,
                             f"{self.java_name}.java", self.targetpath)
        self.common.scp_file(self.primary_root,
                             f"{self.script_name}.jar", self.targetpath)
        result = self.primary_root.sh(
            f"touch {self.properties}").result()
        self.logger.info(result)
        text = '---step3.1:写配置文件;expect:成功---'
        self.logger.info(text)
        error_passwd = self.userNode.ssh_password + '_error'
        config = f'echo "password=' \
            f'{error_passwd}"> {self.properties}'
        self.primary_root.sh(config)
        config = f'echo "port={self.userNode.db_port}">> ' \
            f'{self.properties}'
        self.primary_root.sh(config)
        config = f'echo "hostname={self.userNode.db_host}">> ' \
            f'{self.properties}'
        self.primary_root.sh(config)
        config = f'echo "user={self.userNode.ssh_user}">> {self.properties}'
        self.primary_root.sh(config)
        config = f'echo "dbname={self.userNode.db_name}">> ' \
            f'{self.properties}'
        self.primary_root.sh(config)
        config = f'cat {self.properties}'
        result = self.primary_root.sh(config).result()
        self.logger.info(result)
        assert1 = "password=" in result and "port=" in result and \
                  "hostname=" in result and "user=" in result and \
                  "dbname=" in result
        self.assertTrue(assert1, '执行失败:' + text)
        text = '---step3.2:编译java脚本;expect:成功---'
        self.logger.info(text)
        scp_cmd = self.primary_root.scp_put(macro.JDBC_PATH,
                                        f"{self.targetpath}/postgresql.jar")
        self.logger.info(scp_cmd)
        cmd = f"javac -encoding utf-8 -cp " \
            f"{os.path.join(self.targetpath, 'postgresql.jar')} " \
            f"{os.path.join(self.targetpath, f'{self.java_name}.java')}"
        self.logger.info(cmd)
        result = self.primary_root.sh(cmd).result()
        self.logger.info(result)
        text = '---step3.3:运行java脚本，数据库连接失败;expect:成功---'
        self.logger.info(text)
        cmd_run = f"java -cp " \
            f"{os.path.join(self.targetpath, 'postgresql.jar')}:" \
            f"{os.path.join(self.targetpath, f'{self.script_name}.jar')}:" \
            f"{self.targetpath} {self.java_name} -F {self.properties}"
        self.logger.info(cmd_run)
        result = self.primary_root.sh(cmd_run).result()
        self.logger.info(result)
        assert2 = 'Forbid remote connection with initial user' in result and \
                  '连接失败' in result
        self.assertTrue(assert2, '执行失败:' + text)
    
    def tearDown(self):
        text = '---step:4.恢复配置文件中的信息;expect:成功---'
        self.logger.info(text)
        check_cmd = f'mv {self.confignew} {self.config};' \
            f'rm -rf {self.targetpath}'
        self.logger.info(check_cmd)
        self.primary_root.sh(check_cmd).result()
        restart_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M primary'
        restart_msg = self.userNode.sh(restart_cmd).result()
        self.logger.info(restart_msg)
        text = '---step:5.恢复加密方式配置;expect:成功---'
        self.logger.info(text)
        exe_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"password_encryption_type={self.default_msg_list}"'
        msg2 = self.userNode.sh(exe_cmd2).result()
        self.logger.info(msg2)
        sql_cmd3 = 'show password_encryption_type;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.logger.info('--Opengauss_Function_Security_sm3_Case0043 finish--')

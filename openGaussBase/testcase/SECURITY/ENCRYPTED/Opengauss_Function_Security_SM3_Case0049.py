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
Case Name   : 创建用户时加密算法MD5，认证方式sm3，非初始用户错误的密码通过JDBC连接数据库
Description :
    1.修改password_encryption_type=0
    2.pg_hba.conf文件中修改认证方式sm3
    3.非初始用户错误的密码通过JDBC登录数据库
Expect      :
    1-2.参数设置成功
    3.数据库连接失败
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
        self.logger.info('--Opengauss_Function_Security_sm3_Case0049 start--')
        self.userNode = Node('PrimaryDbUser')
        self.primary_root = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.user = 'u_security_sm3_0049'
        self.targetpath = "/home/jdbc_test"
        self.properties = os.path.join(self.targetpath, "jdbc_connect.conf")
        self.java_name = "jdbc_drop_schema_case0001"
        self.script_name = 'bcprov-jdk15on-1.68'
        self.config = os.path.join(self.DB_INSTANCE_PATH, 'pg_hba.conf')
        self.confignew = os.path.join(self.DB_INSTANCE_PATH, 'pg_hba_bak.conf')
        self.logger.info('--------获取参数默认值--------')
        self.default_msg_list = ''
        check_default = 'show password_encryption_type;'
        default_msg = self.sh_primy.execut_db_sql(check_default)
        self.logger.info(default_msg)
        self.default_msg_list = default_msg.splitlines()[2].strip()
        self.logger.info(self.default_msg_list)
        self.logger.info('--------备份白名单文件---------')
        cp_cmd = f"cp {self.config} {self.confignew}"
        self.userNode.sh(cp_cmd).result()
    
    def test_encrypted(self):
        text = '---step1:修改password_encryption_type=0;expect:成功---'
        self.logger.info(text)
        exe_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            '"password_encryption_type=0"'
        msg1 = self.userNode.sh(exe_cmd1).result()
        self.logger.info(msg1)
        check_cmd = 'show password_encryption_type;'
        check_msg = self.sh_primy.execut_db_sql(check_cmd)
        self.logger.info(check_msg)
        self.common.equal_sql_mdg(check_msg, 'password_encryption_type', '0',
                                  '(1 row)', flag='1')
        text = '---step2:pg_hba.conf文件中增加认证方式为md5;expect:成功---'
        self.logger.info(text)
        exe_cmd2 = f'grep  "IPv4 local connections:" {self.config}'
        msg2 = self.userNode.sh(exe_cmd2).result()
        self.logger.info(msg2)
        insert_messages = f"host {self.userNode.db_name} {self.user} " \
            f"{self.userNode.db_host}/32 sm3"
        exe_cmd3 = f'sed -i "/{msg2}/a\{insert_messages}" {self.config}'
        self.logger.info(exe_cmd3)
        msg3 = self.userNode.sh(exe_cmd3).result()
        self.logger.info(msg3)
        restart_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M primary'
        restart_msg = self.userNode.sh(restart_cmd).result()
        self.logger.info(restart_msg)
        text = '---step3:创建用户1;expect:成功---'
        self.logger.info(text)
        sql_cmd4 = f'create user {self.user} with password \'' \
            f'{macro.COMMON_PASSWD}\';'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.assertIn('CREATE ROLE', msg4, '执行失败:' + text)
        text = '---step4.1:写入配置文件，用户1设置错误的密码;expect:成功---'
        self.logger.info(text)
        self.common.scp_file(self.primary_root,
                             f"{self.java_name}.java", self.targetpath)
        self.common.scp_file(self.primary_root,
                             f"{self.script_name}.jar", self.targetpath)
        error_passwd = macro.COMMON_PASSWD + '_error'
        result = self.primary_root.sh(
            f"touch {self.properties}").result()
        self.logger.info(result)
        config = f'echo "password={error_passwd}"> {self.properties}'
        self.primary_root.sh(config)
        config = f'echo "port={self.userNode.db_port}">> ' \
            f'{self.properties}'
        self.primary_root.sh(config)
        config = f'echo "hostname={self.userNode.db_host}">> ' \
            f'{self.properties}'
        self.primary_root.sh(config)
        config = f'echo "user={self.user}">> {self.properties}'
        self.primary_root.sh(config)
        config = f'echo "dbname={self.userNode.db_name}">> ' \
            f'{self.properties}'
        self.primary_root.sh(config)
        config = f'cat {self.properties}'
        result = self.primary_root.sh(config).result()
        assert1 = "password=" in result and "port=" in result and \
                  "hostname=" in result and "user=" in result and \
                  "dbname=" in result
        self.assertTrue(assert1, '执行失败:' + text)
        text = '---step4.2:编译java脚本;expect:成功---'
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
        text = '---step4.3:运行java脚本，数据库连接成功;expect:成功---'
        self.logger.info(text)
        cmd = f"java -cp {os.path.join(self.targetpath, 'postgresql.jar')}:" \
            f"{os.path.join(self.targetpath, f'{self.script_name}.jar')}:" \
            f"{self.targetpath} {self.java_name} -F" \
            f" {self.properties}"
        result = self.primary_root.sh(cmd).result()
        self.logger.info(result)
        self.assertIn('连接失败', result, '执行失败:' + text)
    
    def tearDown(self):
        self.logger.info('-------1.恢复配置文件中的信息------')
        check_cmd = f'if [ -f {self.config} ];then mv {self.confignew} ' \
            f'{self.config};rm -rf {self.targetpath};fi'
        self.logger.info(check_cmd)
        self.primary_root.sh(check_cmd).result()
        restart_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M primary'
        restart_msg = self.userNode.sh(restart_cmd).result()
        self.logger.info(restart_msg)
        self.logger.info('-------2.恢复加密方式配置------')
        exe_cmd2 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            f'"password_encryption_type={self.default_msg_list}"'
        msg2 = self.userNode.sh(exe_cmd2).result()
        self.logger.info(msg2)
        sql_cmd3 = 'show password_encryption_type;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.logger.info('-------3.删除用户-------')
        sql_cmd4 = f'drop user {self.user}'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.logger.info('--Opengauss_Function_Security_sm3_Case0049 finish--')

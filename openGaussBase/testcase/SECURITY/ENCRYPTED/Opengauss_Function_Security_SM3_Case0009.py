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
Case Name   : 创建用户时的加密算法sha256，认证方式sm3,非初始用户错误的密码连接数据库
Description :
    1.修改password_encryption_type=2
    2.pg_hba.conf文件中修改认证方式为sm3
    3.创建普通用户{self.user}
    4.{self.user}用户错误密码登录数据库
Expect      :
    1-2.参数设置成功
    3.用户创建成功
    4.数据连接失败：Invalid username/password,login denied
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
        self.logger.info(
            '---Opengauss_Function_Security_sm3_Case0009 start---')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.user = 'u_security_sm3_0009'
        self.config = os.path.join(self.DB_INSTANCE_PATH, 'pg_hba.conf')
        self.confignew = os.path.join(self.DB_INSTANCE_PATH, 'pg_hba_bak.conf')
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
        text = '---step1:修改password_encryption_type=2;expect:成功---'
        self.logger.info(text)
        exe_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            '"password_encryption_type=2"'
        msg1 = self.userNode.sh(exe_cmd1).result()
        self.logger.info(msg1)
        check_cmd = 'show password_encryption_type;'
        check_msg = self.sh_primy.execut_db_sql(check_cmd)
        self.logger.info(check_msg)
        self.common.equal_sql_mdg(check_msg, 'password_encryption_type', '2',
                                  '(1 row)', flag='1')
        text = '---step2:pg_hba.conf文件中增加认证方式为sm3;expect:成功---'
        self.logger.info(text)
        exe_cmd2 = f'grep  "local.*all.*trust" {self.config}'
        msg2 = self.userNode.sh(exe_cmd2).result()
        self.logger.info(msg2)
        insert_messages = f"local {self.userNode.db_name} {self.user} sm3"
        exe_cmd3 = f'sed -i "/{msg2}/i\{insert_messages}" {self.config}'
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
        self.logger.info('--------4.使用用户1错误密码登录数据库--------')
        error_password = macro.COMMON_PASSWD + '_error'
        exe_cmd5 = f'source {self.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.user} ' \
            f'-W \'{error_password}\' -c "\\q"'
        self.logger.info(exe_cmd5)
        msg5 = self.userNode.sh(exe_cmd5).result()
        self.logger.info(msg5)
        self.assertIn('Invalid username/password,login denied', msg5,
                      '执行失败:' + text)
    
    def tearDown(self):
        self.logger.info('-------1.恢复配置文件中的信息------')
        check_cmd = f'if [ -f {self.config} ];then mv {self.confignew} ' \
            f'{self.config};fi'
        self.logger.info(check_cmd)
        self.userNode.sh(check_cmd).result()
        restart_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M primary'
        restart_msg = self.userNode.sh(restart_cmd).result()
        self.logger.info(restart_msg)
        self.logger.info('-------2.恢复加密方式配置------')
        exe_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            f'"password_encryption_type={self.default_msg_list}"'
        msg1 = self.userNode.sh(exe_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = 'show password_encryption_type;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.logger.info('-------3.删除用户------')
        sql_cmd3 = f'drop user {self.user}'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.logger.info(
            '----Opengauss_Function_Security_sm3_Case0009 finish----')

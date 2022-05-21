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
Case Name   : 创建用户时的加密算法sm3，认证方式sha256，初始用户正确的密码连接数据库
Description :
    1.修改password_encryption_type=3
    2.pg_hba.conf文件中修改认证方式为sha256
    3.初始用户正确的密码登录数据库
Expect      :
    1-2.参数修改成功
    3.数据库连接成功，初始用户实际加密方式sha256
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
        self.logger.info('--Opengauss_Function_Security_SM3_Case0010 start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.config = os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')
        self.confignew = os.path.join(macro.DB_INSTANCE_PATH,
                                      'pg_hba_bak.conf')
        self.default_msg_list = ''
        self.logger.info('--------检查参数默认值---------')
        check_default = 'show password_encryption_type;'
        default_msg = self.sh_primy.execut_db_sql(check_default)
        self.logger.info(default_msg)
        self.default_msg_list = default_msg.splitlines()[2].strip()
        self.logger.info(self.default_msg_list)
        self.logger.info('--------备份白名单文件---------')
        cp_cmd = f"cp {self.config} {self.confignew}"
        self.userNode.sh(cp_cmd).result()
    
    def test_encrypted(self):
        text = '---step1:修改password_encryption_type=3; expect:成功---'
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
        text = '---step2:pg_hba.conf文件中增加认证方式为sha256---'
        self.logger.info(text)
        exe_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -h ' \
            '"local all all sha256"'
        msg2 = self.userNode.sh(exe_cmd2).result()
        self.logger.info(msg2)
        exe_cmd3 = f'cat {self.config}'
        msg3 = self.userNode.sh(exe_cmd3).result()
        self.logger.info(msg3)
        self.assertIn('local all all sha256', msg3, '执行失败:' + text)
        text = '---step3:初始用户正确的密码登录数据库;expect:成功---'
        self.logger.info(text)
        exe_cmd5 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p ' \
            f'{self.userNode.db_port} -U {self.userNode.ssh_user} -W ' \
            f'{self.userNode.ssh_password} -c "\\q"'
        self.logger.info(exe_cmd5)
        msg5 = self.userNode.sh(exe_cmd5).result()
        self.logger.info(msg5)
        self.assertEqual('', msg5, '执行失败:' + text)
    
    def tearDown(self):
        text = '----step4:恢复配置文件中的信息；expect:成功----'
        self.logger.info(text)
        check_cmd = f'mv {self.confignew} {self.config}'
        self.logger.info(check_cmd)
        self.userNode.sh(check_cmd).result()
        restart_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M primary'
        restart_msg = self.userNode.sh(restart_cmd).result()
        self.logger.info(restart_msg)
        text = '----step5:恢复加密方式配置；expect:成功----'
        self.logger.info(text)
        exe_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"password_encryption_type={self.default_msg_list}"'
        msg1 = self.userNode.sh(exe_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = 'show password_encryption_type;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.logger.info(
            '----Opengauss_Function_Security_SM3_Case0010 finish----')

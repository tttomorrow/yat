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
Case Name   : 创建用户时的加密算法与认证过程中的加密算法均为sm3,初始用户-h远程连接数据库
Description :
    1.修改password_encryption_type=3
    2.pg_hba.conf文件中修改认证方式为sm3
    3.初始用户远程连接数据库
Expect      :
    1-2.参数修改成功
    3.数据库连接失败
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.userNode = Node(node='PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.config = os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')
        self.confignew = os.path.join(macro.DB_INSTANCE_PATH,
                                      'pg_hba_bak.conf')
        self.logger.info('-----检查参数默认值-----')
        self.default_param = self.common.show_param('password_encryption_type')
        self.logger.info(self.default_param)
        self.logger.info('-----备份白名单文件-----')
        cp_cmd = f"cp {self.config} {self.confignew}"
        self.userNode.sh(cp_cmd).result()
    
    def test_encrypted(self):
        text = '---step1:修改password_encryption_type=3; expect:成功---'
        self.logger.info(text)
        self.sh_primy.execute_gsguc('reload', self.constant.GSGUC_SUCCESS_MSG,
                                    f'password_encryption_type=3')
        check_msg = self.common.show_param('password_encryption_type')
        self.assertEqual('3', check_msg, '执行失败:' + text)
        
        text = '---step2:pg_hba.conf文件中增加认证方式为sm3;expect:成功---'
        self.logger.info(text)
        exe_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -h ' \
            f'"host {self.userNode.db_name} {self.userNode.ssh_user} ' \
            f'{self.userNode.db_host}/32 sm3"'
        self.common.get_sh_result(self.userNode, exe_cmd2)
        
        text = '---step3:初始用户远程连接数据库;expect:失败---'
        self.logger.info(text)
        msg3 = self.sh_primy.execut_db_sql('\\q', sql_type=f'-U '
        f'{self.userNode.ssh_user} -h {self.userNode.db_host}')
        self.logger.info(msg3)
        self.assertIn('Forbid remote connection with initial user', msg3,
                      '执行失败:' + text)
    
    def tearDown(self):
        text = '-----恢复配置文件中的信息-----'
        self.logger.info(text)
        check_cmd = f'mv {self.confignew} {self.config}'
        self.logger.info(check_cmd)
        check_msg = self.common.get_sh_result(self.userNode, check_cmd)
        restart_msg = self.sh_primy.restart_db_cluster()
        self.logger.info(restart_msg)
        
        text = '----恢复加密方式配置----'
        self.logger.info(text)
        exe_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -c ' \
            f'"password_encryption_type={self.default_param}"'
        self.common.get_sh_result(self.userNode, exe_cmd1)
        msg2 = self.common.show_param('password_encryption_type')
        self.logger.info(msg2)
        self.assertEqual(f'{self.default_param}', msg2, '执行失败:' + text)
        self.assertEqual(True, restart_msg, '执行失败:' + text)
        self.assertEqual('', check_msg, '执行失败:' + text)
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')

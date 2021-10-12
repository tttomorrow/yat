"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Type   : policy
Case Name   : 密码最小长度要求password_min_length=999
Description :
    1.在postgres.conf中设置password_min_length=999，重启数据库生效
    2.初始用户执行：create user wf with password 'Hu@123';
Expect      :
    1.设置成功，数据库重启成功
    2.提示密码至少包含999位
History     :
"""
import random
import string
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
logger = Logger()
class Policy(unittest.TestCase):
    def setUp(self):
        logger.info('==Opengauss_Function_Security_Policy_Case0049 start==')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        str_lst = []
        for j in range(10):
            str_lst.append(random.choice(string.ascii_lowercase))
        part_lst = str_lst[:6]
        str_passwd = "".join(part_lst)
        self.new_password1 = str_passwd.capitalize() + "@" + "1" * 992
        self.new_password2 = str_passwd.capitalize() + "@" + "1" * 991
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_policy(self):
        logger.info('-------------create user -------------')
        sql_modify = f'''source {self.DB_ENV_PATH};
            gs_guc set -N all -I all -c "password_max_length=999"
            gs_guc set -N all -I all -c "password_min_length=999"
            gs_om -t stop && gs_om -t start'''
        msg_modify = self.userNode.sh(sql_modify).result()
        logger.info(msg_modify)
        sql_cmd1 = f'create user wf with password \'{self.new_password1}\';'
        sql_cmd2 = f'create user user001 with password ' \
                   f'\'{self.new_password2}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn(self.Constant.PASSWORD_CONTAIN_AT_LEAST_MSG, msg2)
    def tearDown(self):
        logger.info('-----------恢复配置，并清理环境-----------')
        sql_modify = f'''source {self.DB_ENV_PATH};
            gs_guc set -N all -I all -c "password_max_length=32"
            gs_guc set -N all -I all -c "password_min_length=8"
            gs_om -t stop && gs_om -t start'''
        msg_modify = self.userNode.sh(sql_modify).result()
        logger.info(msg_modify)
        sql_cmd1 = 'drop user if exists wf cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info('==Opengauss_Function_Security_Policy_Case0049 finish==')

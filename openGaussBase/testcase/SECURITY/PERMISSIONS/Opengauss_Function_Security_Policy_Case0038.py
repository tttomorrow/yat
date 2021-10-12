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
Case Name   : 密码为0-9数字的最少要求个数password_min_digital=1
Description :
    1.在postgres.conf中设置password_min_digital=3，重启数据库生效
    2.初始用户执行：create user user001 with password 'Qazwsx@123';
    create user wf with password 'Qazwsx@h12';
Expect      :
    1.设置成功，数据库重启成功
    2.user001创建成功
    创建wf时提示密码至少包含3个数字
History     :
"""
import unittest
from yat.test import macro

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

logger = Logger()


class Policy(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Security_Policy_Case0038 start---')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.new_password1 = macro.COMMON_PASSWD.upper() + "qaz"
        self.Constant = Constant()
        self.configure = 'password_min_digital=1'
        msg0 = self.common.config_set_modify(self.configure)
        logger.info(msg0)
        status_msg = self.sh_primy.get_db_cluster_status()
        logger.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)

    def test_policy(self):
        logger.info('----------------create user ---------------')
        sql_cmd1 = 'create user user001 with password \'Xiaxia@hu3\';'
        sql_cmd2 = 'create user wf with password \'Xiaxia@hau\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.CREATE_ROLE_SUCCESS_MSG, msg1)
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.assertIn(self.Constant.PASSWORD_CONTAIN_AT_LEAST_MSG, msg2)

    def tearDown(self):
        logger.info('-----------恢复配置，并清理环境-----------')
        self.configure = 'password_min_digital=0'
        msg0 = self.common.config_set_modify(self.configure)
        logger.info(msg0)
        status_msg = self.sh_primy.get_db_cluster_status()
        logger.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)
        sql_cmd1 = 'drop user if exists wf cascade;' \
                   'drop user if exists user001 cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info('---Opengauss_Function_Security_Policy_Case0038 finish---')

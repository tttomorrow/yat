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
Case Type   : policy
Case Name   : 密码为a-z小写字母的最少要求个数password_min_lowercase=999
Description :
    1.在postgres.conf中设置password_min_lowercase=999，重启数据库生效
    2.初始用户执行：create user wf with password '$PASSWORD';
Expect      :
    1.设置成功，数据库重启成功
    2.提示密码至少包含999个小写字母
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
        logger.info('---Opengauss_Function_Security_Policy_Case0037 start---')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.new_password1 = macro.COMMON_PASSWD.upper() + "qaz"
        self.Constant = Constant()
        self.configure = 'password_min_lowercase=999'
        msg0 = self.common.config_set_modify(self.configure)
        logger.info(msg0)
        status_msg = self.sh_primy.get_db_cluster_status()
        logger.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)

    def test_policy(self):
        logger.info('-----------create user -----------------')
        sql_cmd1 = f'create user wf with password \'{self.new_password1}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertIn(self.Constant.PASSWORD_CONTAIN_AT_LEAST_MSG, msg1)

    def tearDown(self):
        logger.info('-----------恢复配置，并清理环境-----------')
        self.configure = 'password_min_lowercase=0'
        msg0 = self.common.config_set_modify(self.configure)
        logger.info(msg0)
        status_msg = self.sh_primy.get_db_cluster_status()
        logger.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)
        sql_cmd1 = 'drop user if exists wf cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info('Opengauss_Function_Security_Policy_Case0037 finish')

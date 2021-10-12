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
Case Name   : 密码最大长度要求password_max_length=6
Description :
    1.在postgres.conf中设置password_max_length=6，重启数据库生效
    2.初始用户执行：create user wf with password 'Hu@123';
    create user user001 with password 'Hua@123';
Expect      :
    1.设置成功，数据库重启成功
    2.CREATE ROLE
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
        logger.info('==Opengauss_Function_Security_Policy_Case0051 start==')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        str_lst = []
        for j in range(10):
            str_lst.append(random.choice(string.ascii_lowercase))
        part_lst = str_lst[:3]
        str_passwd = "".join(part_lst)
        self.new_password = str_passwd.capitalize() + "@" + "15"
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Constant = Constant()

    def test_policy(self):
        logger.info("------设置参数password_max_length=6--------")
        excute_cmd1 = f'''
            source {self.DB_ENV_PATH}
            gs_guc set -N all -I all -c "password_min_length=6"
            gs_guc set -N all -I all -c "password_max_length=6"
            gs_om -t stop && gs_om -t start
            '''
        logger.info(excute_cmd1)
        msg0 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg0)
        logger.info('-------检查数据库状态---------------')
        status_msg = self.sh_primy.get_db_cluster_status()
        logger.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)
        logger.info('---------------create user ---------------')
        sql_cmd1 = f'create user wf with password \'{self.new_password}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertTrue(msg1.find("CREATE ROLE") > -1)

    def tearDown(self):
        logger.info('-----------恢复配置，并清理环境-----------')
        excute_cmd1 = f'''
            source {self.DB_ENV_PATH};
            gs_guc set -N all -I all -c "password_max_length=32"
            gs_guc set -N all -I all -c "password_min_length=8"
            gs_om -t stop && gs_om -t start
            '''
        logger.info(excute_cmd1)
        msg0 = self.userNode.sh(excute_cmd1).result()
        logger.info(msg0)
        logger.info('-------检查数据库状态---------------')
        status_msg = self.sh_primy.get_db_cluster_status()
        logger.info(status_msg)
        self.assertTrue("Degraded" in status_msg or "Normal" in status_msg)
        sql_cmd1 = 'drop user if exists wf cascade;' \
                   'drop user if exists user001 cascade;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info('==Opengauss_Function_Security_Policy_Case0051 finish==')

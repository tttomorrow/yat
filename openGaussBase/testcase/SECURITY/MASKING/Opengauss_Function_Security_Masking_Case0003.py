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
Case Type   : security_masking
Case Name   : 普通用户无权限删除poladmin用户创建的资源标签
Description :
    1.普通用户创建资源标签：
    create resource label creditcard_lable;
Expect      :
    1.返回报错信息：ERROR:  Permission denied.
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        logger.info('---Opengauss_Function_Security_Masking_Case0003 start---')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_masking(self):
        logger.info('--------创建用户--------')
        sql_cmd1 = f'create user poladmin with POLADMIN password \'' \
                   f'{macro.COMMON_PASSWD}\';' \
                   f'create user user001 with password \'' \
                   f'{macro.COMMON_PASSWD}\';'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info('--------开启安全策略开关--------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                      f'"enable_security_policy=on"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        sql_cmd3 = f'show enable_security_policy;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'enable_security_policy', 'on',
                                  '(1 row)', flag='1')
        logger.info('--------创建资源标签--------')
        sql_cmd4 = 'create resource label creditcard_lable;'
        excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U poladmin -W \'' \
                      f'{macro.COMMON_PASSWD}\' -c "{sql_cmd4}"'
        logger.info(excute_cmd4)
        msg4 = self.userNode.sh(excute_cmd4).result()
        logger.info(msg4)
        self.assertTrue('CREATE RESOURCE LABEL' in msg4)
        logger.info('--------普通用户删除资源标签--------')
        sql_cmd5 = 'drop resource label creditcard_lable;'
        excute_cmd5 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U user001 -W \'' \
                      f'{macro.COMMON_PASSWD}\' -c "{sql_cmd5}"'
        logger.info(excute_cmd5)
        msg5 = self.userNode.sh(excute_cmd5).result()
        logger.info(msg5)
        self.assertTrue('ERROR:  Permission denied' in msg5)
        logger.info('--------poladmin用户删除资源标签--------')
        sql_cmd6 = 'drop resource label creditcard_lable;'
        excute_cmd6 = f'source {self.DB_ENV_PATH};' \
                      f'gsql -d {self.userNode.db_name} -p ' \
                      f'{self.userNode.db_port} -U poladmin -W \'' \
                      f'{macro.COMMON_PASSWD}\' -c "{sql_cmd6}"'
        logger.info(excute_cmd6)
        msg6 = self.userNode.sh(excute_cmd6).result()
        logger.info(msg6)
        self.assertTrue('DROP RESOURCE LABEL' in msg6)

    def tearDown(self):
        logger.info('-------清理环境---------')
        sql_cmd1 = f'drop user poladmin;drop user user001;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        self.assertTrue(msg1.count('DROP ROLE') == 2)
        logger.info('--------关闭安全策略开关--------')
        excute_cmd2 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
                      f'"enable_security_policy=off"'
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        sql_cmd3 = f'show enable_security_policy;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        self.common.equal_sql_mdg(msg3, 'enable_security_policy', 'off',
                                  '(1 row)', flag='1')
        logger.info(
            '---Opengauss_Function_Security_Masking_Case0003 finish---')

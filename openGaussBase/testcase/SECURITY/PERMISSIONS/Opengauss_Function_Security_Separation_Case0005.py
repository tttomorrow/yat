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
Case Type   : security-Separation_rights
Case Name   : 三权分立后系统管理员对表空间有访问的权限
Description :
    1.初始用户执行：CREATE USER sysadmin01 WITH SYSADMIN password '$PASSWORD';
                    CREATE TABLESPACE fastspace RELATIVE LOCATION
                    'tablespace/tablespace_2';
    2.sysadmin01 用户执行：SELECT spcname FROM pg_tablespace;
Expect      :
    1.CREATE ROLE
    CREATE TABLESPACE
    2.spcname
    -------------------
    pg_default | pg_globa l fastspace
    (3 rows)
History     :
"""
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
        logger.info('-Opengauss_Function_Security_Separation_Case0005 start-')
        self.common = Common()
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()

    def test_policy(self):
        logger.info('--------create user ------------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -D {macro.DB_INSTANCE_PATH}' \
                      f' -c "enableSeparationOfDuty=on"' \
                      f'gs_om -t stop && gs_om -t start'
        msg0 = self.userNode.sh(excute_cmd0).result()
        logger.info(msg0)
        sql_cmd1 = f'''CREATE USER sysadmin01 WITH SYSADMIN password \
            '{macro.COMMON_PASSWD}';
            CREATE TABLESPACE fastspace RELATIVE LOCATION 
            'tablespace/tablespace_2';'''
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        sql_cmd2 = 'SELECT spcname FROM pg_tablespace;'
        excute_cmd2 = f'''source {self.DB_ENV_PATH};
            gsql -d {self.userNode.db_name} -p {self.userNode.db_port} -U \
            sysadmin01 -W '{macro.COMMON_PASSWD}' -c "{sql_cmd2}"
            '''
        logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        logger.info(msg2)
        self.assertTrue('fastspace' in msg2 and 'pg_default' in msg2)

    def tearDown(self):
        logger.info('----------恢复配置，并清理环境-----------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};' \
                      f'gs_guc set -D {macro.DB_INSTANCE_PATH}' \
                      f' -c "enableSeparationOfDuty=off";' \
                      f'om -t stop && gs_om -t start'
        msg0 = self.userNode.sh(excute_cmd0).result()
        logger.info(msg0)
        sql_cmd1 = 'DROP TABLESPACE IF EXISTS fastspace;' \
                   'DROP USER sysadmin01;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        logger.info('Opengauss_Function_Security_Separation_Case0005 finish')

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
Case Type   : 服务端工具
Case Name   : 如果参数是一个字符串变量，则使用-c parameter="'value'"
            或者使用-c "parameter = 'value'"
Description :
    1.查看krb_caseins_users默认值
    2.修改配置文件中参数，同时发送信号量到postgresql.conf
    3.检查是否设置成功
    4.恢复设置
Expect      :
    1.显示成功
    2.设置完成
    3.设置成功
    4.恢复完成
History     : 
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0036开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools(self):
        LOG.info('---------------步骤1.查看krb_caseins_users默认值---------------')
        sql_cmd = self.commonsh.execut_db_sql(f'show krb_caseins_users;')
        LOG.info(sql_cmd)
        self.assertIn('off', sql_cmd)

        LOG.info('----步骤2.修改配置文件中参数，同时发送信号量到postgresql.conf----')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -N all -I all -c "krb_caseins_users=\'on\'"'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('Success to perform gs_guc!', msg)

        LOG.info('------------------步骤3.检查是否设置成功------------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc check -N all -D {macro.DB_INSTANCE_PATH} ' \
            f'-c "krb_caseins_users";'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("krb_caseins_users='on'", msg)

    def tearDown(self):
        LOG.info('------------------步骤4.恢复默认值------------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -N all -I all -c "krb_caseins_users=off";'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0036执行结束----')

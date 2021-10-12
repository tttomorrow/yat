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
Case Type   : 服务端工具
Case Name   : 使用gs_guc reload进行参数设定，未指定-N参数，在备节点上执行
Description :
    1.查看默认值
    2.使用gs_guc reload进行参数设定，不指定-N，在备节点上执行
    3.查看设置后的参数值
    4.恢复设置
    5.查看设置后的参数
Expect      :
    1.默认krb_caseins_users=null
    2.修改成功
    3.查看设置后的参数：只会修改备节点的参数值
    4.恢复设置
    5.查看设置后的参数成功
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
Primary_SH = CommonSH('PrimaryDbUser')


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0022开始执行----')
        self.dbuser_node = Node('dbuser')
        self.standby1_dbuser = Node('Standby1DbUser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    @unittest.skipIf(1 == Primary_SH.get_node_num(), '单机环境不执行')
    def test_server_tools1(self):
        LOG.info('----步骤1.查看krb_caseins_users默认值----')
        sql_cmd = self.commonsh.execut_db_sql(f'show krb_caseins_users;')
        LOG.info(sql_cmd)
        self.assertIn('off', sql_cmd)
        LOG.info('----步骤2.使用gs_guc reload进行参数设定，不指定-N，在备节点上执行----')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -I all -c  krb_caseins_users=on'
        LOG.info(check_cmd)
        msg = self.standby1_dbuser.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("Success to perform gs_guc!", msg)

        LOG.info('------------------步骤3.查看设置后的参数值----------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'cat {macro.DB_INSTANCE_PATH}/postgresql.conf|grep ' \
            f'krb_caseins_users;gs_guc check -N all ' \
            f'-D {macro.DB_INSTANCE_PATH} -c "krb_caseins_users"'
        LOG.info(check_cmd)
        msg = self.standby1_dbuser.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("krb_caseins_users = on", msg)

        LOG.info('-----------步骤4.使用gs_guc reload恢复默认值-----------')
        check_cmd = f'''hostname'''
        LOG.info(check_cmd)
        hostname = self.standby1_dbuser.sh(check_cmd).result()
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -N {hostname} -I all -c  krb_caseins_users=off'
        LOG.info(check_cmd)
        msg = self.standby1_dbuser.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn(' Failed instances: 0', msg)

        LOG.info('------------------步骤5.查看设置后的参数值------------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'cat {macro.DB_INSTANCE_PATH}/postgresql.conf|grep ' \
            f'krb_caseins_users;gs_guc check -N all ' \
            f'-D {macro.DB_INSTANCE_PATH} -c "krb_caseins_users" '
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("krb_caseins_users=off", msg)

    def tearDown(self):
        LOG.info('------------------无需清理环境----------------------')
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0022执行结束----')

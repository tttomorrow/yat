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
Case Name   : 使用gs_guc reload进行参数设定，并指定-N为主节点
Description :
    1.查看默认值
    2.使用gs_guc reload进行参数设定，并指定-N为主节点：
    3.查看设置后的参数值
    4.使用gs_guc reload恢复默认值
    5.查看设置后的参数值
Expect      :
    1.默认krb_caseins_users=off
    2.修改成功
    3.查看设置后的参数：(主备节点的参数值都会被修改)krb_caseins_users=off
    4.恢复设置成功
    5，查看参数值生效
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
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0021开始执行-----')
        self.dbuser = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        LOG.info('-----步骤1.查看krb_caseins_users默认值-----')
        sql_cmd = self.commonsh.execut_db_sql(f'show krb_caseins_users;')
        LOG.info(sql_cmd)
        self.assertIn('off', sql_cmd)

        LOG.info('----步骤2.使用gs_guc reload进行参数设定，不指定-N，在主节点上执行----')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -I all -c  krb_caseins_users=on'
        LOG.info(check_cmd)
        msg = self.dbuser.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("Success to perform gs_guc!", msg)

        LOG.info('----------------步骤3.查看设置后的参数值------------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'cat {macro.DB_INSTANCE_PATH}/postgresql.conf|grep ' \
            f'krb_caseins_users;gs_guc check -N all ' \
            f'-D {macro.DB_INSTANCE_PATH} -c " krb_caseins_users" '
        LOG.info(check_cmd)
        msg = self.dbuser.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("krb_caseins_users = on", msg)

        LOG.info('-----步骤4.使用gs_guc reload恢复默认值-----')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -N all -I all -c  krb_caseins_users=off'
        LOG.info(check_cmd)
        msg = self.dbuser.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('ALL: Success to perform gs_guc!', msg)

        LOG.info('------------------步骤5.查看设置后的参数值------------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'cat {macro.DB_INSTANCE_PATH}/postgresql.conf|grep ' \
            f'krb_caseins_users;gs_guc check -N all ' \
            f'-D {macro.DB_INSTANCE_PATH} -c " krb_caseins_users"'
        LOG.info(check_cmd)
        msg = self.dbuser.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn("krb_caseins_users=off", msg)

    def tearDown(self):
        LOG.info('------------------步骤6.恢复默认值------------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -N all -I all -c  krb_caseins_users=off'
        LOG.info(check_cmd)
        msg = self.dbuser.sh(check_cmd).result()
        LOG.info(msg)
        LOG.info('---------重启数据库---------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail;' \
            f'gs_om -t restart;'
        LOG.info(check_cmd)
        msg = self.dbuser.sh(check_cmd).result()
        LOG.info(msg)
        LOG.info('-----Opengauss_Function_Tools_gs_guc_Case0021执行结束-----')

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
Case Name   : 将已设置的参数值修改为默认值不使用参数set或者reload
Description :
    1.查看allow_system_table_mods默认值
    2.设置allow_system_table_mods
    3.重启数据库
    4.检查设置后的值是否成功
    5.不使用set或reload将已设置的参数值修改为默认值
    6.使用reload将已设置的参数值修改为默认值
    7.检查设置后的值
    8.恢复设置
    9.重启数据库
Expect      :
    1.显示成功
    2.设置完成
    3.重启成功
    4.设置成功
    5.执行失败：gs_guc: no operation specified
    Try "gs_guc --help" for more information
    6.修改为默认值完成
    7.默认值设置成功
    8.恢复设置完成
    9.重启成功
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
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0031开始执行----')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools(self):
        LOG.info('----步骤1.查看allow_system_table_mods默认值----')
        sql_cmd = self.commonsh.execut_db_sql(f'show allow_system_table_mods;')
        LOG.info(sql_cmd)
        self.assertIn('off', sql_cmd)

        LOG.info('----步骤2.设置allow_system_table_mods为off----')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc set -N all -I all -c "allow_system_table_mods=off"'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('Success to perform gs_guc!', msg)

        LOG.info('-------------------步骤3.重启数据库------------------')
        self.commonsh.restart_db_cluster()
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)

        LOG.info('------------------步骤4.查看设置是否成功------------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc check -N all -D {macro.DB_INSTANCE_PATH} ' \
            f'-c " allow_system_table_mods";'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('allow_system_table_mods=off', msg)

        LOG.info('----步骤5.不使用set或reload将已设置的参数值修改为默认值----')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc  -N all -I all -c "allow_system_table_mods=on";'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('gs_guc: no operation specified', msg)

        LOG.info('----步骤6.使用reload将已设置的参数值修改为默认值----')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload  -N all -I all -c "allow_system_table_mods=off";'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('Success to perform gs_guc!', msg)

        LOG.info('------------------步骤6.检查设置后的值------------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc check -N all -D {macro.DB_INSTANCE_PATH} ' \
            f'-c " allow_system_table_mods";'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        self.assertIn('allow_system_table_mods=off', msg)

    def tearDown(self):
        LOG.info('------------------步骤7.恢复设置------------------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc set -N all -I all -c "allow_system_table_mods=off"'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)

        LOG.info('---------------------重启数据库--------------------')
        LOG.info('-------重启数据库------')
        check_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t status --detail;' \
            f'gs_om -t restart;'
        LOG.info(check_cmd)
        msg = self.dbuser_node.sh(check_cmd).result()
        LOG.info(msg)
        LOG.info('----Opengauss_Function_Tools_gs_guc_Case0031执行结束----')

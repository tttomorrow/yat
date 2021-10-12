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
Case Type   : 系统内部使用工具
Case Name   : 备机执行gs_ctl promote使用-D指定不正确数据库实例目录是否成功
Description :
    1.创建恢复文件
    2.执行gs_ctl promote指定-D设置参数为不正确的数据库实例目录(备机执行)
Expect      :
    1.创建恢复文件成功
    2.执行gs_ctl promote指定-D设置参数为不正确的数据库实例目录失败
History     :
"""

import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0063开始执行-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('-------若为单机环境，后续不执行，直接通过-------')
        query_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.user_node = Node('Standby1DbUser')

        LOG.info('----创建文件并执行promote-------')
        excute_cmd = f"touch {macro.DB_INSTANCE_PATH}/recovery.conf ;"
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl promote -D {macro.DB_BACKUP_PATH} ;
            '''
        LOG.info(excute_cmd)
        excute_msg = self.user_node.sh(excute_cmd).result()
        LOG.info(excute_msg)
        self.assertNotIn('server promoting', excute_msg)

    def tearDown(self):
        LOG.info('----this is tearDown------')
        query_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(query_cmd)
        query_msg = self.PrimaryNode.sh(query_cmd).result()
        LOG.info(query_msg)
        if 'Standby' not in query_msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.user_node = Node('Standby1DbUser')
        rm_cmd = f"rm -rf {macro.DB_INSTANCE_PATH}/recovery.conf ;"
        LOG.info(rm_cmd)
        rm_msg = self.user_node.sh(rm_cmd).result()
        LOG.info(rm_msg)
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0063执行完成----')

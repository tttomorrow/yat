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
Case Type   : 系统内部使用工具
Case Name   : 备机执行gs_ctl notify使用-D指定正确数据库实例目录是否成功
Description :
    1.以pending的方式启动备机
    2.查看集群状态，备节点是否为pending状态
    3.备机指定正确的数据库实录目录执行notify
    4.查看集群状态，备节点是否为primary
Expect      :
    1.以pending的方式启动备机成功
    2.查看集群状态成功，备节点为pending状态
    3.备机指定正确的数据库实录目录执行notify成功
    4.查看集群状态，备节点为primary
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0096开始执行-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_standby = CommonSH('PrimaryDbUser')

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
            self.StandbyNode = Node('Standby1DbUser')
            self.sh_standby = CommonSH('Standby1DbUser')

        LOG.info('--------------以pending的方式启动备机------------------')
        start_cmd = f'''source {macro.DB_ENV_PATH};
                    gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M pending ;
                    '''
        LOG.info(start_cmd)
        start_msg = self.StandbyNode.sh(start_cmd).result()
        LOG.info(start_msg)
        self.assertIn(self.constant.RESTART_SUCCESS_MSG, start_msg)

        LOG.info('----------------查看备机状态-------------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl query -D {macro.DB_INSTANCE_PATH}; 
            '''
        LOG.info(excute_cmd)
        msg = self.StandbyNode.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn('Pending', msg)

        LOG.info('---------备机指定正确的数据库实录目录执行notify------')
        query_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl notify  -D {macro.DB_INSTANCE_PATH} -M standby ;
            '''
        LOG.info(query_cmd)
        query_msg = self.StandbyNode.sh(query_cmd).result()
        LOG.info(query_msg)
        status = self.sh_standby.get_db_instance_status()
        self.assertTrue(status)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
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
            self.StandbyNode = Node('Standby1DbUser')
            self.sh_standby = CommonSH('Standby1DbUser')
        LOG.info('----------------恢复集群状态------------------')
        query_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M standby ;
            '''
        LOG.info(query_cmd)
        query_msg = self.StandbyNode.sh(query_cmd).result()
        LOG.info(query_msg)
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0096执行完成---')

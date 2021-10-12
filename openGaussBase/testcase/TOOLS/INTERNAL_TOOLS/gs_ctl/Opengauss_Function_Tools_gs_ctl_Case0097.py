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
Case Name   : 备机执行gs_ctl notify指定-M为standby,重启后查看操作是否生效
Description :
    1.以pending的方式启动备机（备机执行）
    2.查看集群状态，备节点是否为pending状态
    3.备机执行notify并指定-M的值为standby
    4.查看集群状态，备节点是否为standby
    5.重启数据库
    6.查看主备是否恢复
Expect      :
    1.以pending的方式启动备机成功
    2.查看集群状态成功，备节点为pending状态
    3.备机执行notify并指定-M的值为standby成功
    4.查看集群状态，备节点为standby成功
    5.重启数据库成功
    6.查看主备状态，主备节点已恢复
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
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0097开始执行-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

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

        LOG.info('---------------------重启数据库--------------------')
        self.sh_primary.restart_db_cluster()
        status = self.sh_primary.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)

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
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0097执行完成---')

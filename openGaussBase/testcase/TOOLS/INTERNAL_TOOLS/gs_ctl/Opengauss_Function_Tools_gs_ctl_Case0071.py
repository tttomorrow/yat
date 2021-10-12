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
Case Name   : 主机在start状态下执行failover
Description :
    1.在备机上执行failover（备机执行）
    2.执行refrashconf进行信息写入
    3.重启集群
    4.检查主备是否切换成功
    5.进行备机重建恢复备机状态
Expect      :
    1.在备机上执行failover成功
    2.执行refrashconf进行信息写入失败
    3.重启集群成功
    4.检查主备状态，主备切换失败，备机状态为need repair
    5.恢复备机成功
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
        LOG.info('--------------------this is setup--------------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0071开始执行-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('------------若为单机环境，后续不执行，直接通过-------')
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

        LOG.info('-----------------进行备升主---------------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl failover -D {macro.DB_INSTANCE_PATH} -m fast ;
            '''
        LOG.info(excute_cmd)
        msg = self.StandbyNode.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.FAILOVER_SUCCESS_MSG, msg)

        LOG.info('-----------------进行refreshconf---------------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t refreshconf;
            '''
        LOG.info(excute_cmd)
        excute_msg = self.StandbyNode.sh(excute_cmd).result()
        LOG.info(excute_msg)
        self.assertNotIn(self.constant.REFRESHCONF_SUCCESS_MSG, excute_msg)

        LOG.info('---------------------重启数据库--------------------')
        self.sh_primary.restart_db_cluster()
        status = self.sh_primary.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)

        LOG.info('-----------------查看主备状态---------------------')
        status_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(status_cmd)
        status_msg = self.StandbyNode.sh(status_cmd).result()
        LOG.info(status_msg)
        self.node_msg = query_msg.splitlines()[10].strip()
        self.assertIn('Primary', self.node_msg)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        LOG.info('-------若为单机环境，后续不执行，直接通过-------')
        status_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(status_cmd)
        status_msg = self.PrimaryNode.sh(status_cmd).result()
        LOG.info(status_msg)
        if 'Standby' not in status_msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.StandbyNode = Node('Standby1DbUser')
        LOG.info('-----------------恢复集群-备机重建---------------')
        recover_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl build -D {macro.DB_INSTANCE_PATH};
            '''
        LOG.info(recover_cmd)
        recover_msg = self.StandbyNode.sh(recover_cmd).result()
        LOG.info(recover_msg)
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0071执行完成----')

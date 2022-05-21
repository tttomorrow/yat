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
Case Name   : 执行failover后不执行gs_om -t refreshconf，重启后查看切换是否成功
Description :
    1.关闭主数据库(主机执行)
    2.在备机上执行failover（备机执行）
    3.检查主备是否切换成功
    4.重启数据库集群
    5.检查数据库主备节点状态
Expect      :
    1.关闭主数据库成功
    2.在备机上执行failover成功
    3.集群主备节点切换成功
    4.重启数据库成功
    5.数据库主备节点切换为原有主备状态
History     :
"""

import unittest
import re
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()
primary_sh = CommonSH('PrimaryDbUser')


@unittest.skipIf('Standby' not in primary_sh.get_db_cluster_status('detail'),
                 'Single node, and subsequent codes are not executed.')
class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0065开始执行-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.StandbyNode = Node('Standby1DbUser')
        self.node_num = primary_sh.get_node_num()

    def test_system_internal_tools(self):
        text = '---step1:主节点关闭数据库   expect:停库成功---'
        LOG.info(text)
        stop_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl stop -D {macro.DB_INSTANCE_PATH};'''
        LOG.info(stop_cmd)
        stop_msg = self.PrimaryNode.sh(stop_cmd).result()
        LOG.info(stop_msg)
        self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG, stop_msg,
                      '执行失败' + text)

        text = '---step2:在备1节点上进行failover   expect:成功---'
        LOG.info(text)
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl failover -D {macro.DB_INSTANCE_PATH} -m fast;'''
        LOG.info(excute_cmd)
        excute_msg = self.StandbyNode.sh(excute_cmd).result()
        LOG.info(excute_msg)
        self.assertIn(self.constant.FAILOVER_SUCCESS_MSG, excute_msg,
                      '执行失败' + text)

        text = '---step3:检查主备切换后状态   expect:主机切换为备机---'
        LOG.info(text)
        status1 = primary_sh.get_db_cluster_status(param='detail')
        LOG.info(status1)
        self.assertIn('S Primary', status1, '执行失败' + text)

        text = '---step4:重启数据库集群   expect:成功---'
        LOG.info(text)
        primary_sh.restart_db_cluster()
        status2 = primary_sh.get_db_cluster_status()
        self.assertTrue("Normal" in status2 or 'Degraded' in status2)

        text = '---step5:再次查看数据库主备状态   expect:原主机状态恢复---'
        LOG.info(text)
        status3 = primary_sh.get_db_cluster_status(param='detail')
        LOG.info(status3)
        self.assertIn('P Primary', status3, '执行失败' + text)

    def tearDown(self):
        LOG.info('--------------this is tearDown-------------------')
        LOG.info('----重建备机----')
        build_msg_list = primary_sh.get_standby_and_build()
        LOG.info(build_msg_list)
        LOG.info('---检查数据库状态---')
        status = primary_sh.get_db_cluster_status(param='all')
        LOG.info(status)
        regex_res = re.findall('instance_state.*:.*Normal', status)
        LOG.info(regex_res)
        self.assertEqual(len(regex_res), self.node_num)
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0065执行完成----')

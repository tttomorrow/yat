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
Case Name   : 生成动态配置文件(备机failover或switchover成主机后，需要执行此操作)
Description :
    1.查看数据库状态：gs_om -t status --detail
    2.在备机上执行switchover：gs_ctl switchover  -D /XXX/dn1
    3.执行refrashconf进行信息写入:gs_om -t refreshconf
    4.重启集群:gs_om -t stop; gs_om -t start;
    5.检查主备是否切换成功:gs_om -t status --detail
    6.在备机上执行switchover：gs_ctl switchover -D /XXX/dn1
    7.执行refrashconf进行信息写入:gs_om -t refreshconf
    8.重启集群:gs_om -t stop; gs_om -t start;
    9.检查主备是否切换成功:gs_om -t status --detail
Expect      :
    1.状态显示正常，确定主备机
    2.在备机上执行switchover成功
    3.执行refrashconf进行信息写入成功
    4.重启集群成
    5.检查主备状态，主备切换成功
    6.在备机上执行switchover成功
    7.执行refrashconf进行信息写入成功
    8.重启集群成功
    9.检查主备状态，主备切换成功
History     : 
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0011start--')
        self.Pri_dbuser = Node('PrimaryDbUser')
        self.Sta_dbuser = Node('Standby1DbUser')
        self.constant = Constant()
        self.commonsh = CommonSH()

    def test_server_tools1(self):
        self.logger.info('----------------1.查询数据库状态----------------')
        status_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f' gs_om -t status --detail ;'
        self.logger.info(status_cmd1)
        status_msg1 = self.Pri_dbuser.sh(status_cmd1).result()
        self.logger.info(status_msg1)
        self.assertTrue("Degraded" in status_msg1 or "Normal" in status_msg1)

        self.logger.info('-------------2.在备机上执行switchover------------')
        switchover_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_ctl switchover  -D {macro.DB_INSTANCE_PATH};'
        self.logger.info(switchover_cmd1)
        switchover_msg1 = self.Sta_dbuser.sh(switchover_cmd1).result()
        self.logger.info(switchover_msg1)
        self.assertTrue('switchover completed' in switchover_msg1)

        self.logger.info('----------3.执行refrashconf进行信息写入----------')
        refrashconf_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t refreshconf;'
        self.logger.info(refrashconf_cmd1)
        refrashcon_msg1 = self.Sta_dbuser.sh(refrashconf_cmd1).result()
        self.logger.info(refrashcon_msg1)
        self.assertIn('Successfully generated dynamic configuration file',
                      refrashcon_msg1)

        self.logger.info('----------4.重启集群----------')
        cluster_cmd1 = self.commonsh.restart_db_cluster()
        self.logger.info(cluster_cmd1)

        self.logger.info('------------- 5.检查主备是否切换成功--------------')
        status_cmd2 = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_om -t status --detail ;'
        self.logger.info(status_cmd2)
        status_msg2 = self.Pri_dbuser.sh(status_cmd2).result()
        self.logger.info(status_msg2)
        self.node_msg = status_msg2.splitlines()[10].strip()
        self.assertTrue("Degraded" in status_msg2 or "Normal" in status_msg2)
        self.assertIn('Standby', self.node_msg)
        self.logger.info('-------------6.在备机上执行switchover------------')
        switchover_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_ctl switchover -D {macro.DB_INSTANCE_PATH};'
        self.logger.info(switchover_cmd2)
        switchover_msg2 = self.Pri_dbuser.sh(switchover_cmd2).result()
        self.logger.info(switchover_msg2)
        self.assertTrue("switchover completed" in switchover_msg2)

        self.logger.info('----------7.执行refrashconf进行信息写入----------')
        refrashconf_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_om -t refreshconf;'
        self.logger.info(refrashconf_cmd2)
        refrashcon_msg2 = self.Pri_dbuser.sh(refrashconf_cmd2).result()
        self.logger.info(refrashcon_msg2)
        self.assertIn('Successfully generated dynamic '
                      'configuration file', refrashcon_msg2)

        self.logger.info('----------8.重启集群----------')
        cluster_cmd2 = self.commonsh.restart_db_cluster()
        self.logger.info(cluster_cmd2)

        self.logger.info('------------- 9.检查主备是否切换成功-------------')
        status_cmd3 = f'source {macro.DB_ENV_PATH}; ' \
            f'gs_om -t status --detail ;'
        self.logger.info(status_cmd3)
        status_msg3 = self.Pri_dbuser.sh(status_cmd3).result()
        self.logger.info(status_msg3)
        self.assertTrue("Degraded" in status_msg3 or "Normal" in status_msg3)
        self.node_msg = status_msg3.splitlines()[10].strip()
        self.assertIn('Primary', self.node_msg)

    def tearDown(self):
        status_cmd = f''' source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        self.logger.info(status_cmd)
        status_msg = self.Pri_dbuser.sh(status_cmd).result()
        self.logger.info(status_msg)
        self.node_msg = status_msg.splitlines()[10].strip()
        self.logger.info(self.node_msg)
        if 'Standby' in self.node_msg:
            self.logger.info('--------------恢复主备状态--------------')
            recover_cmd = f'''source {macro.DB_ENV_PATH};
                        gs_ctl switchover -D {macro.DB_INSTANCE_PATH};
                        gs_om -t refreshconf;
                        '''
            self.logger.info(recover_cmd)
            recover_msg = self.Pri_dbuser.sh(recover_cmd).result()
            self.logger.info(recover_msg)
        else:
            return '主备节点正常'
        self.logger.info('--Opengauss_Function_Tools_gs_om_Case0011finish--')


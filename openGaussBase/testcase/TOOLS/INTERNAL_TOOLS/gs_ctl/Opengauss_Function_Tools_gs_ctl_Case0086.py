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
Case Name   : switchover后原有数据是否损坏
Description :
    1.主机执行事务
    2.在备机上执行switchover（备机执行）
    3.执行refrashconf进行信息写入
    4.重启集群
    5.检查主备是否切换成功
    6.查询事务是否存在
Expect      :
    1.主机执行事务成功
    2.在备机上执行switchover成功
    3.执行refrashconf进行信息写入成功
    4.重启集群成功
    5.检查主备状态，主备切换成功
    6.查询事务成功，事务存在且未损坏
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
        LOG.info('--------------this is setup-----------------------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0086开始执行-----')
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

        LOG.info('-----------------执行事务---------------------')
        msg = self.sh_primary.execut_db_sql('create table testzl (a integer);')
        LOG.info(msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, msg)

        LOG.info('-----------------执行switchover---------------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl switchover -D {macro.DB_INSTANCE_PATH} -m fast ;
            '''
        LOG.info(excute_cmd)
        msg = self.StandbyNode.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.SWITCHOVER_SUCCESS_MSG, msg)

        LOG.info('-----------------进行refreshconf---------------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t refreshconf;
            '''
        LOG.info(excute_cmd)
        msg = self.StandbyNode.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.REFRESHCONF_SUCCESS_MSG, msg)

        LOG.info('---------------------重启数据库--------------------')
        self.sh_primary.restart_db_cluster()
        status = self.sh_primary.get_db_cluster_status()
        self.assertTrue("Normal" in status or 'Degraded' in status)

        LOG.info('-----------------查看主备状态---------------------')
        status_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(status_cmd)
        status_msg = self.PrimaryNode.sh(status_cmd).result()
        LOG.info(status_msg)
        self.node_msg = status_msg.splitlines()[10].strip()
        self.assertIn('Standby', self.node_msg)

        LOG.info('----------------查询事务---------------------')
        msg = self.sh_primary.execut_db_sql('select count(*) from testzl;')
        LOG.info(msg)
        self.assertIn('0', msg)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        status_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t status --detail;
            '''
        LOG.info(status_cmd)
        status_msg = self.PrimaryNode.sh(status_cmd).result()
        LOG.info(status_msg)
        self.node_msg = status_msg.splitlines()[10].strip()
        LOG.info(self.node_msg)
        if 'Standby' in self.node_msg:
            LOG.info('--------------恢复主备状态--------------')
            recover_cmd = f'''source {macro.DB_ENV_PATH};
                gs_ctl switchover -D {macro.DB_INSTANCE_PATH} -m fast;
                gs_om -t refreshconf;
                '''
            LOG.info(recover_cmd)
            recover_msg = self.PrimaryNode.sh(recover_cmd).result()
            LOG.info(recover_msg)
        else:
            return '主备节点正常'
        clear_msg = self.sh_primary.execut_db_sql('drop table if exists testzl;')
        LOG.info(clear_msg)
        LOG.info('----Opengauss_Function_Tools_gs_ctl_Case0086执行完成-----')

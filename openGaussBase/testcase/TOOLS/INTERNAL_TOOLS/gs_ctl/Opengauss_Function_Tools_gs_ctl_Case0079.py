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
Case Name   : 执行gs_ctl switchover指定-m的值为fast，switchover后活跃
                事务是否回滚
Description :
    1.开启事务
    2.执行事务，不做提交
    3.开启新的session指定-m设置参数为fast，在备机switchover
    4.执行refrashconf进行信息写入
    5.查看事务是否回滚
Expect      :
    1.开启事务成功
    2.执行事务，不做提交成功
    3.开启新的session指定-m设置参数为fast，在备机switchover成功
    4.执行refrashconf进行信息写入成功
    5.查看事务失败，事务回滚
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
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
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0079开始执行-----')
        self.constant = Constant()
        self.common = Common()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.sh_standby = CommonSH('Standby1DbUser')
        self.StandbyNode = Node('Standby1DbUser')

    def test_system_internal_tools(self):
        LOG.info('-----------------开启并执行事务事务---------------')
        transaction_msg = self.sh_primary.execut_db_sql('''drop table if \
            exists testzl; 
            start transaction; 
            create table testzl (a integer);''')
        LOG.info(transaction_msg)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, transaction_msg)

        LOG.info('-----------------执行switchover---------------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl switchover -D {macro.DB_INSTANCE_PATH} -m fast -U \
            {self.StandbyNode.ssh_user} -P {self.StandbyNode.ssh_password};
            '''
        LOG.info(excute_cmd)
        excute_msg = self.StandbyNode.sh(excute_cmd).result()
        LOG.info(excute_msg)
        self.assertIn(self.constant.SWITCHOVER_SUCCESS_MSG, excute_msg)

        LOG.info('-----------------进行refreshconf---------------------')
        excute_cmd = f'''source {macro.DB_ENV_PATH};
            gs_om -t refreshconf;
            '''
        LOG.info(excute_cmd)
        excute_msg = self.StandbyNode.sh(excute_cmd).result()
        LOG.info(excute_msg)
        self.assertIn(self.constant.REFRESHCONF_SUCCESS_MSG, excute_msg)

        LOG.info('----------------查看事务-------------------')
        transaction_msg = self.sh_primary.execut_db_sql(
            'select count(*) from testzl')
        LOG.info(transaction_msg)
        self.assertIn(self.constant.NOT_EXIST, transaction_msg)

    def tearDown(self):
        LOG.info('--------------this is tearDown--------------')
        LOG.info('-------检查主备同步状态，等待同步------')
        node_num = self.common.get_node_num(self.PrimaryNode)
        LOG.info(node_num)
        consistency_flag = self.sh_standby.check_location_consistency(
            'primary', node_num, 300)

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
                gs_ctl switchover -D {macro.DB_INSTANCE_PATH} -m fast -t 300;
                gs_om -t refreshconf;
                '''
            LOG.info(recover_cmd)
            self.recover_msg = self.PrimaryNode.sh(recover_cmd).result()
            LOG.info(self.recover_msg)

        LOG.info('---再次获取数据库节点状态---')
        status = self.sh_primary.get_db_cluster_status('detail')
        LOG.info(status)
        self.assertTrue('P Primary' in status)
        self.assertTrue(consistency_flag)
        self.assertTrue(self.constant.SWITCH_SUCCESS_MSG in self.recover_msg
            and self.constant.REFRESH_SUCCESS_MSG in self.recover_msg)
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0079执行完成---')



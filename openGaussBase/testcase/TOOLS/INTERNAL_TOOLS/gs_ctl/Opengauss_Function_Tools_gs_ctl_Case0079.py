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
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class SystemInternalTools(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0079开始执行-----')
        self.constant = Constant()
        self.PrimaryNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('-----------若为单机环境，后续不执行，直接通过----------')
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
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0079执行完成---')

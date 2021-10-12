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
Case Name   : 结合-r参数执行备机重建是否成功
Description :
    1.进行备机重建
    2.查看数据库状态，检验是否重建成功
Expect      :
    1.进行备机重建成功
    2.查看数据库状态，备机重建成功
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
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0099开始执行-----')
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

        LOG.info('--------------进行备机重建------------------')
        build_cmd = f'''source {macro.DB_ENV_PATH};
                    gs_ctl build -D {macro.DB_INSTANCE_PATH} -r 1 ;
                    '''
        LOG.info(build_cmd)
        build_msg = self.StandbyNode.sh(build_cmd).result()
        LOG.info(build_msg)
        self.assertIn(self.constant.RESTART_SUCCESS_MSG, build_msg)

        LOG.info('----------------查看备机状态-------------------')
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
        restart_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl restart -D {macro.DB_INSTANCE_PATH} -M standby ;
            '''
        LOG.info(restart_cmd)
        restart_msg = self.StandbyNode.sh(restart_cmd).result()
        LOG.info(restart_msg)
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0099执行完成---')

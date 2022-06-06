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
Case Name   : 使用querybuild指定正确的数据库实例目录，查看数据库重建进度
Description :
    1.进行备机重建
    2.查看数据库重建进度
Expect      :
    1.进行备机重建成功
    2.查看数据库重建进度成功
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
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0107开始执行-----')
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
            gs_ctl build -D {macro.DB_INSTANCE_PATH} ;
            '''
        LOG.info(build_cmd)
        build_msg = self.StandbyNode.sh(build_cmd).result()
        LOG.info(build_msg)
        self.assertIn(self.constant.RESTART_SUCCESS_MSG, build_msg)

        LOG.info('----------------查看备机重建进度-------------------')
        progress_cmd = f'''source {macro.DB_ENV_PATH};
            gs_ctl querybuild -D {macro.DB_BACKUP_PATH} ;
            '''
        LOG.info(progress_cmd)
        progress_msg = self.StandbyNode.sh(progress_cmd).result()
        LOG.info(progress_msg)
        self.assertIn('not exist', progress_msg)

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
        LOG.info('---Opengauss_Function_Tools_gs_ctl_Case0107执行完成---')

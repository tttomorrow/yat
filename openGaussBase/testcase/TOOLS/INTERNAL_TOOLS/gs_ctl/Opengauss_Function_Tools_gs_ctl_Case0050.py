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
Case Name   : gs_ctl stop使用-D指定正确数据库实例目录备机是否可以关闭成功
Description :
    1.gs_ctl指定-D设置参数为不正确的数据库实例目录，stop关闭备机
    2.查看集群状态备机是否为关闭状态
Expect      :
    1.gs_ctl指定-D设置参数为不正确的数据库实例目录，stop关闭备机成功
    2.查看集群状态，备机为关闭状态
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

LOG = Logger()


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        LOG.info('----this is setup------')
        LOG.info(
            '---Opengauss_Function_Tools_gs_ctl_Case0050开始执行-----')
        self.constant = Constant()
        self.env_path = macro.DB_ENV_PATH
        self.instance_path = macro.DB_INSTANCE_PATH
        self.my_path = macro.DB_BACKUP_PATH
        self.PrimaryNode = Node('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info(
            '-------若为单机环境，后续不执行，直接通过-------')
        excute_cmd = f''' source {self.env_path}
                                  gs_om -t status --detail
                                 '''
        LOG.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        LOG.info(msg)
        if 'Standby' not in msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.user_node = Node('Standby1DbUser')
            self.sh_standby = CommonSH('Standby1DbUser')

        LOG.info('----查看集群状态-------')
        status = self.sh_standby.get_db_cluster_status()
        self.assertTrue(status)

        LOG.info('----关闭数据库备机-------')
        excute_cmd = f'''
                    source {self.env_path};
                    gs_ctl stop -D {self.my_path} ;
                        '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.NOT_EXIST, msg)

        LOG.info('----查看备机状态-------')
        excute_cmd = f'''
                        source {self.env_path};
                        gs_ctl query -D {self.instance_path} ; 
                            '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn('Normal', msg)

    def tearDown(self):
        LOG.info('----this is tearDown------')
        excute_cmd = f''' source {self.env_path}
                                          gs_om -t status --detail
                                         '''
        LOG.info(excute_cmd)
        msg = self.PrimaryNode.sh(excute_cmd).result()
        LOG.info(msg)
        if 'Standby' not in msg:
            return '单机环境，后续不执行，直接通过'
        else:
            self.user_node = Node('Standby1DbUser')
            self.sh_standby = CommonSH('Standby1DbUser')
        LOG.info('----恢复集群状态------')
        is_start = self.sh_standby.start_db_cluster()
        LOG.info(is_start)
        LOG.info(
            '-----Opengauss_Function_Tools_gs_ctl_Case0050执行完成---')

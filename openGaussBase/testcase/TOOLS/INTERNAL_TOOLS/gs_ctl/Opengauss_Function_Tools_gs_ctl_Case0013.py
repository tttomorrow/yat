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
Case Name   : 单节点关闭数据库后gs_ctl start -M在主节点指定pending启动
Description :
    1.关闭正在运行的主机
    2.指定-M设置值为pending启动主机
    3.查看主机状态pending模式是否启动正常
    4.恢复主节点
Expect      :
    1.关闭正在运行的主机成功
    2.指定-M设置值为pending启动主机成功
    3.查看主机状态pending模式启动正常
    4.恢复主节点
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
        LOG.info('----------------this is setup-----------------------')
        LOG.info(
            '---Opengauss_Function_Tools_gs_ctl_Case0013开始执行-----')
        self.constant = Constant()
        self.env_path = macro.DB_ENV_PATH
        self.my_path = macro.DB_MY_PATH
        self.instance_path = macro.DB_INSTANCE_PATH
        self.user_node = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('---------关闭正在运行的主机------------')
        is_stop = self.sh_primary.stop_db_instance()
        self.assertTrue(is_stop)

        LOG.info('-------------以pending模式开启主机-------------------')
        excute_cmd = f'''
                    source {self.env_path};
                    gs_ctl start -D {self.instance_path} -M pending; 
                        '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.RESTART_SUCCESS_MSG, msg)

        LOG.info('----------------查看主机状态-------------------')
        excute_cmd = f'''
                    source {self.env_path};
                    gs_ctl query -D {self.instance_path}; 
                        '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn('Pending', msg)

        LOG.info('----------------恢复主机状态-------------------')
        excute_cmd = f'''
                    source {self.env_path};
                    gs_ctl restart -D {self.instance_path} -M primary; 
                        '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.RESTART_SUCCESS_MSG, msg)

        LOG.info('----------------查看主机状态-------------------')
        status = self.sh_primary.get_db_instance_status()
        self.assertTrue(status)

    def tearDown(self):
        LOG.info('----------------this is tearDown-----------------------')
        LOG.info('----------------恢复主机状态-------------------')
        excute_cmd = f'''
                        source {self.env_path};
                        gs_ctl restart -D {self.instance_path} -M primary; 
                            '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        LOG.info(
            '-----Opengauss_Function_Tools_gs_ctl_Case0013执行完成---')

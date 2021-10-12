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
Case Name   : gs_ctl start指定-o "OPTIONS"启动是否报错
Description :
    1.关闭运行正常的集群
    2.使用-o option参数启动数据库
    3.恢复集群状态
Expect      :
    1.关闭运行正常的集群成功
    2.使用-o option参数启动数据库失败
    3.恢复集群状态成功
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
            '---Opengauss_Function_Tools_gs_ctl_Case0016开始执行-----')
        self.constant = Constant()
        self.env_path = macro.DB_ENV_PATH
        self.instance_path = macro.DB_INSTANCE_PATH
        self.user_node = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('---------关闭正在运行的集群------------')
        is_stop = self.sh_primary.stop_db_cluster()
        self.assertTrue(is_stop)

        LOG.info('------------使用-o option参数启动数据库--------------')
        excute_cmd = f'''
                    source {self.env_path};
                    gs_ctl start -D {self.instance_path} -M primary -o option; 
                        '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.argument_error, msg)

    def tearDown(self):
        LOG.info('----------------this is tearDown-----------------------')
        LOG.info('----------------恢复集群状态------------------')
        is_start = self.sh_primary.start_db_cluster()
        LOG.info(is_start)
        LOG.info(
            '-----Opengauss_Function_Tools_gs_ctl_Case0016执行完成---')

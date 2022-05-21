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
Case Name   : gs_ctl start指定-l FILENAME，当指定文件在数据库实例
                目录下启动主机（参数后指定文件路径）
Description :
    1.关闭运行正常的集群
    2.使用开启数据库的用户在实例目录下创建文件
    3.使用-l参数并指定文件路径启动数据库
    4.查看gsctl_test.dat文件中是否有记录信息
    5.查看集群状态，主机正常启动
Expect      :
    1.关闭运行正常的集群成功
    2.使用开启数据库的用户在实例目录下创建文件成功
    3.使用-l参数并指定该文件路径启动数据库成功
    4.查看gsctl_test.dat文件中，文件中有记录信息
    5.查看集群状态，主机正常启动
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
            '---Opengauss_Function_Tools_gs_ctl_Case0017开始执行-----')
        self.constant = Constant()
        self.env_path = macro.DB_ENV_PATH
        self.instance_path = macro.DB_INSTANCE_PATH
        self.user_node = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')

    def test_system_internal_tools(self):
        LOG.info('---------关闭正在运行的主机------------')
        is_stop = self.sh_primary.stop_db_instance()
        self.assertTrue(is_stop)

        LOG.info('-----------在实例目录下创建文件------------------')
        excute_cmd = f'''
                    touch {self.instance_path}/gsctl_test.dat; 
                        '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], msg)

        LOG.info('----------------启动数据库-------------------')
        excute_cmd = f'''
                    source {self.env_path};
                    gs_ctl start -D {self.instance_path} -M primary \
                    -l {self.instance_path}/gsctl_test.dat; 
                        '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn(self.constant.RESTART_SUCCESS_MSG, msg)

        LOG.info('----------------查看gsctl_test.dat文件-------------------')
        excute_cmd = f'''
                    du -h {self.instance_path}/gsctl_test.dat ;
                        '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        res = msg.split()[0]
        self.assertTrue(float(res[:-1]) > 0)

        LOG.info('----------------查看集群状态-------------------')
        status = self.sh_primary.get_db_cluster_status()
        self.assertTrue(status)

    def tearDown(self):
        LOG.info('----------------this is tearDown-----------------------')
        LOG.info('----------------恢复集群状态------------------')
        is_start = self.sh_primary.start_db_cluster()
        LOG.info(is_start)
        LOG.info('-----------删除创建文件------------------')
        excute_cmd = f'''
                        rm -rf {self.instance_path}/gsctl_test.dat;
                                '''
        LOG.info(excute_cmd)
        msg = self.user_node.sh(excute_cmd).result()
        LOG.info(msg)
        LOG.info(
            '-----Opengauss_Function_Tools_gs_ctl_Case0017执行完成---')

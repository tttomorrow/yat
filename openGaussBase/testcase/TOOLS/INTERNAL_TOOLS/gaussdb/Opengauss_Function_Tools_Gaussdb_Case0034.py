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
Case Type   : tools
Case Name   : 启动gaussdb进程时，主数据库使用-M参数设置本端以pending模式启动是否成功
Description :
    1.关闭正在运行的数据库（主数据库）
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2..查看进程，确定关闭成功
    ps -ef|grep zl
    3.使用gaussdb工具设置-M参数为本端以pending模式启动
    gaussdb -D /opt/openGauss_zl/cluster/dn1 -p 19701 -M  pending &
    4.验证-查看集群状态，该节点是否为pending状态
    gs_om -t status --detail
    5.恢复数据库状态
    gs_ctl notify -D /opt/openGauss_zl/cluster/dn1 -M primary
Expect      :
    1.关闭正在运行的数据库成功
    2.查看进程，数据库连接进程不存在，数据库关闭成功
    3.使用gaussdb工具设置-M参数为本端以pending模式启动成功
    4.查看集群状态成功，主节点为pending启动
    5.恢复数据库状态成功
History     :
"""
import unittest
from testcase.utils.ComThread import ComThread
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_Gaussdb_Case0034 start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_systools(self):
        self.logger.info('-------若为单机环境不执行-------')
        excute_cmd = f' source {self.DB_ENV_PATH};' \
                     f'gs_om -t status --detail'
        self.logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg)
        if 'Standby' not in msg:
            return '单机环境不执行'
        else:
            self.logger.info('--------关闭正在运行的数据库--------')
            excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                          f'gs_ctl stop -D {self.DB_INSTANCE_PATH}'
            self.logger.info(excute_cmd1)
            msg1 = self.userNode.sh(excute_cmd1).result()
            self.logger.info(msg1)
            self.logger.info('--------查看进程，确定关闭成功--------')
            excute_cmd2 = f'ps -ef|grep {self.userNode.ssh_user}'
            self.logger.info(excute_cmd2)
            msg2 = self.userNode.sh(excute_cmd2).result()
            self.logger.info(msg2)
            self.assertFalse(self.DB_INSTANCE_PATH in msg2)
            self.logger.info('----使用gaussdb工具设置-M参数为本端以主机模式启动---')
            excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                          f'gaussdb -D {self.DB_INSTANCE_PATH} -p ' \
                          f'{self.userNode.db_port} -M pending'
            self.logger.info(excute_cmd3)
            thread_2 = ComThread(self.userNode.sh, args=(excute_cmd3,))
            thread_2.setDaemon(True)
            thread_2.start()
            thread_2.join(10)
            excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                          f'gs_om -t status --detail'
            msg4 = self.userNode.sh(excute_cmd4).result()
            self.logger.info(msg4)
            self.assertTrue(msg4.find('P Pending') > -1)
            self.logger.info('--------恢复数据库状态---------')
            excute_cmd5 = f'source {self.DB_ENV_PATH};' \
                          f'gs_ctl notify -D ' \
                          f'{self.DB_INSTANCE_PATH} -M primary'
            self.logger.info(excute_cmd5)
            thread_3 = ComThread(self.userNode.sh, args=(excute_cmd5,))
            thread_3.setDaemon(True)
            thread_3.start()
            thread_3.join(10)
            sql_cmd3 = 'drop user if exists user006 cascade;'
            msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
            self.logger.info(msg3)
            self.assertTrue(msg3.find('DROP ROLE') > -1)

    def tearDown(self):
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0034 finish-')

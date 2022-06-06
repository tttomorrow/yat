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
Case Name   : 在集群主机上使用gaussdb指定--single参数启动是否成功
Description :
    1.关闭正在运行的数据库（主机）
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.使用gaussdb工具指定--single启动数据库(不使用后台运行，直接运行)
    gaussdb --single -D /opt/openGauss_zl/cluster/dn1 -p 19701 postgres
    3.查看集群状态是否正常
    gs_om -t status --detail
    4.恢复-重启主数据库
    gs_ctl restart -D /opt/openGauss_zl/cluster/dn1 -M primary
Expect      :
    1.关闭正在运行的数据库成功
    2.使用gaussdb工具指定--single启动数据库成功
    3.查看数据库状态成功，集群状态异常，该节点状态为stop
    4.恢复-重启主数据库成功
History     :
"""
import unittest
from time import sleep

from yat.test import Node
from yat.test import macro
from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0054 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_systools(self):
        self.logger.info('-------若为单机环境，后续不执行-------')
        excute_cmd = f'source {self.DB_ENV_PATH};gs_om -t status --detail'
        self.logger.info(excute_cmd)
        msg0 = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg0)
        if 'Standby' not in msg0:
            return self.logger.info('单机环境，后续不执行!')
        else:
            self.logger.info('--------关闭正在运行的数据库--------')
            excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                          f'gs_ctl stop -D {self.DB_INSTANCE_PATH}'
            self.logger.info(excute_cmd1)
            msg1 = self.userNode.sh(excute_cmd1).result()
            self.logger.info(msg1)
            self.logger.info('--------查看进程，确定关闭成功--------')
            excute_cmd2 = f'ps -ef|grep \'gaussdb --single -D\''
            self.logger.info(excute_cmd2)
            msg2 = self.userNode.sh(excute_cmd2).result()
            self.logger.info(msg2)
            self.assertFalse(self.DB_INSTANCE_PATH in msg2)
            self.logger.info('-------使用gaussdb工具后台运行进程--------')
            excute_cmd3 = f'source {self.DB_ENV_PATH};gaussdb --single -D ' \
                          f'{self.DB_INSTANCE_PATH} -p ' \
                          f'{self.userNode.db_port} {self.userNode.db_name}'
            self.logger.info(excute_cmd3)
            thread_2 = ComThread(self.userNode2.sh, args=(excute_cmd3,))
            thread_2.setDaemon(True)
            thread_2.start()
            thread_2.join(10)
            self.logger.info('------------查看进程-----------')
            excute_cmd4 = 'ps -ef | grep \'gaussdb --single -D\''
            self.logger.info(excute_cmd4)
            msg4 = self.userNode.sh(excute_cmd4).result()
            self.logger.info(msg4)
            self.logger.info('------------杀掉gaussdb进程-----------')
            excute_cmd6 = 'ps -ef | grep \'gaussdb --single -D\' |grep -v ' \
                          '\'grep\' | awk \'{{print $2}}\' | ' \
                          'xargs kill -9'
            self.logger.info(excute_cmd6)
            msg6 = self.userNode.sh(excute_cmd6).result()
            self.logger.info(msg6)
            sleep(5)
            self.logger.info('------------再次查看进程-----------')
            excute_cmd5 = 'ps -ef | grep \'gaussdb --single -D\''
            msg5 = self.userNode.sh(excute_cmd5).result()
            self.logger.info(msg5)
            self.logger.info('------------恢复数据库-----------')
            excute_cmd7 = f'source {self.DB_ENV_PATH};gs_ctl restart -D ' \
                          f'\'{self.DB_INSTANCE_PATH}\' -M primary'
            msg7 = self.userNode.sh(excute_cmd7).result()
            self.logger.info(msg7)
            self.logger.info('----------查看环境是否恢复状态---------')
            check_status_cmd = f'source {self.DB_ENV_PATH};gs_om -t status ' \
                               f'--detail'
            msg8 = self.userNode.sh(check_status_cmd).result()
            self.logger.info(msg8)
            if 'Standby' in msg8:
                self.logger.info('-----------检查主备状态正常----------')
                self.assertTrue(
                    'P Primary Normal' in msg8 and 'S Standby Normal' in msg8)
            else:
                self.logger.info('-----------检查单机状态正常----------')
                self.assertTrue('P Primary Normal' in msg8)

    def tearDown(self):
        self.logger.info('Opengauss_Function_Tools_Gaussdb_Case0054 finish')

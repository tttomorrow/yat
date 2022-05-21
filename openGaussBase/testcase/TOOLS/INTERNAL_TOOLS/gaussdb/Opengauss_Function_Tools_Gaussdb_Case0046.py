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
Case Name   : 在集群备节点上执行gaussdb指定--single_node启动是否成功
Description :
    1.关闭正在运行的数据库(备机)
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.使用gaussdb工具指定--single_node启动数据库
    gaussdb -D /opt/openGauss_zl/cluster/dn1 -p 19701 --single_node &
    3.查看集群状态是否正常
    gs_om -t status --detail
    4.恢复-重启备数据库
    gs_ctl restart -D /opt/openGauss_zl/cluster/dn1 -M standby
    5.进行备机重建
    gs_ctl build -D /opt/openGauss_zl/cluster/dn1 -b full
Expect      :
    1.关闭正在运行的数据库成功
    2.使用gaussdb工具指定--single_node启动数据库成功
    3.查看数据库状态成功，集群状态异常
    4.恢复-重启备数据库成功
    5.进行备机重建成功
History     :
"""
import unittest
import datetime
from time import sleep

from testcase.utils.ComThread import ComThread
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0046 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH

    def test_systools(self):
        self.logger.info('-------若为单机环境，后续不执行-------')
        excute_cmd = f'source {self.DB_ENV_PATH};gs_om -t status --detail'
        self.logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg)
        if '6002' not in msg:
            self.logger.info('单机环境，后续不执行!')
        else:
            self.standbyNode = Node(node='Standby1DbUser')
            self.standbyNode2 = Node('Standby1DbUser')
            self.sh_standby = CommonSH('Standby1DbUser')
            self.common = Common()
            self.logger.info("--------关闭正在运行的数据库--------")
            excute_cmd1 = f'''source {self.DB_ENV_PATH};
                gs_ctl stop -D {self.DB_INSTANCE_PATH}'''
            self.logger.info(excute_cmd1)
            msg1 = self.standbyNode.sh(excute_cmd1).result()
            self.logger.info(msg1)
            self.logger.info('--------查看进程，确定关闭成功--------')
            excute_cmd2 = f'ps -ef|grep {self.userNode.ssh_user}'
            self.logger.info(excute_cmd2)
            msg2 = self.standbyNode.sh(excute_cmd2).result()
            self.logger.info(msg2)
            self.assertFalse(self.DB_INSTANCE_PATH in msg2)
            self.logger.info('----使用gaussdb工具启动---')
            excute_cmd3 = f'source {self.DB_ENV_PATH};gaussdb -D ' \
                          f'{self.DB_INSTANCE_PATH} -p' \
                          f' {self.userNode.db_port} --single_node'
            self.logger.info(excute_cmd3)
            thread_2 = ComThread(self.standbyNode2.sh, args=(excute_cmd3,))
            thread_2.setDaemon(True)
            thread_2.start()
            thread_2.join(10)
            excute_cmd4 = f'source {self.DB_ENV_PATH};' \
                          f'gs_om -t status --detail'
            self.logger.info(excute_cmd4)
            msg4 = self.standbyNode.sh(excute_cmd4).result()
            self.logger.info(msg4)
            self.assertTrue(msg4.find('P Primary Normal') > -1)
            self.logger.info('----恢复数据库状态---')
            excute_cmd5 = f'''source {self.DB_ENV_PATH};
                 gs_ctl restart -D {self.DB_INSTANCE_PATH} -M standby'''
            self.logger.info(excute_cmd5)
            msg5 = self.standbyNode.sh(excute_cmd5).result()
            self.logger.info(msg5)
            excute_cmd6 = f'source {self.DB_ENV_PATH};gs_om -t status --detail'
            self.logger.info(excute_cmd6)
            msg6 = self.standbyNode.sh(excute_cmd6).result()
            self.logger.info(msg6)
            self.assertTrue(msg6.find('P Primary Normal') > -1)
            self.logger.info('----------备机重建--------')
            excute_cmd7 = f'''source {self.DB_ENV_PATH};
                 gs_ctl build -D {self.DB_INSTANCE_PATH} -b full'''
            self.logger.info(excute_cmd7)
            msg7 = self.standbyNode2.sh(excute_cmd7).result()
            self.logger.info(msg7)
            self.logger.info('----------查看备机状态--------')
            start_time = datetime.datetime.now()
            while True:
                sleep(10)
                excute_cmd8 = f'source {self.DB_ENV_PATH};' \
                              f'gs_om -t status --detail'
                self.logger.info(excute_cmd8)
                msg8 = self.standbyNode.sh(excute_cmd8).result()
                self.logger.info(msg8)
                if 'S Standby Normal' in msg8:
                    self.assertTrue(msg8.find('S Standby Normal'))
                    break
                else:
                    end_time = datetime.datetime.now()
                    if (end_time - start_time).seconds > 600:
                        break
                    else:
                        continue

    def tearDown(self):
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0046 finish-')

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
Case Name   : gaussdb升级模式指定-u参数启动是否成功
Description :
    1.关闭正在运行的数据库
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.使用gaussdb工具指定-u启动数据库
    gaussdb -D /opt/openGauss_agl/cluster/dn1/ -u 1 &
Expect      :
    1.关闭正在运行的数据库成功
    2.gaussdb指定-u参数启动成功
History     :
"""
import datetime
import unittest
from time import sleep
from yat.test import Node
from yat.test import macro
from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0082 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')

    def test_systools(self):
        self.logger.info('--------关闭正在运行的数据库--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_ctl stop -D ' \
                      f'{self.DB_INSTANCE_PATH}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-------使用gaussdb工具后台运行进程--------')
        excute_cmd3 = f'source {self.DB_ENV_PATH};gaussdb -D ' \
                      f'{self.DB_INSTANCE_PATH} -p {self.userNode.db_port}' \
                      f' -u 1'
        self.logger.info(excute_cmd3)
        thread_2 = ComThread(self.userNode2.sh, args=(excute_cmd3,))
        thread_2.setDaemon(True)
        thread_2.start()
        thread_2.join(10)
        self.logger.info('------------连接数据库-----------')
        sql_cmd3 = 'drop user if exists user006 cascade;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find('DROP ROLE') > -1)
        self.logger.info('----------查看环境是否主备，主备需恢复状态---------')
        check_status_cmd = f'source {self.DB_ENV_PATH};gs_om -t status ' \
                           f'--detail'
        check_status_msg = self.userNode.sh(check_status_cmd).result()
        self.logger.info(check_status_msg)
        if 'Standby' in check_status_msg:
            self.standbyNode = Node(node='Standby1DbUser')
            self.logger.info('------------恢复主备集群状态-----------')
            excute_cmd6 = f'source {self.DB_ENV_PATH};' \
                          f'gs_ctl restart -D \'{self.DB_INSTANCE_PATH}\' ' \
                          f'-M primary'
            msg6 = self.userNode.sh(excute_cmd6).result()
            self.logger.info(msg6)
            self.logger.info('------------重建备机-----------')
            excute_cmd7 = f'source {self.DB_ENV_PATH};' \
                          f'gs_ctl build -D {self.DB_INSTANCE_PATH} -b full'
            self.logger.info(excute_cmd7)
            msg7 = self.standbyNode.sh(excute_cmd7).result()
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
        else:
            self.logger.info('单机环境不需要恢复')
        excute_cmd9 = f'source {self.DB_ENV_PATH};gs_om -t status --detail'
        msg9 = self.userNode.sh(excute_cmd9).result()
        self.logger.info(msg9)
        if 'Standby' in msg9:
            self.logger.info('-----------检查主备状态正常----------')
            self.assertTrue(
                'P Primary Normal' in msg9 and 'S Standby Normal' in msg9)
        else:
            self.logger.info('-----------检查单机状态正常----------')
            self.assertTrue('P Primary Normal' in msg9)


def tearDown(self):
    self.logger.info('Opengauss_Function_Tools_Gaussdb_Case0082 finish')

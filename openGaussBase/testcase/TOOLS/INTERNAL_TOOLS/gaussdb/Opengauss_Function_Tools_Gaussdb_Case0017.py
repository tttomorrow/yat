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
Case Type   : tools
Case Name   : 启动gaussdb进程时，备机使用-h参数指定备机hostname启动是否成功
Description :
    1.关闭正在运行的数据库（备机）
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.查看进程，确定关闭成功
    ps -ef|grep zl
    3.使用gaussdb工具后台运行进程
    gaussdb -D /opt/openGauss_zl/cluster/dn1 -p 19701 -h ctuphispra01694
    -M standby &
Expect      :
    1.关闭正在运行的数据库成功
    2.查看进程，数据库连接进程不存在，数据库关闭成功
    3.使用gaussdb工具指定备机hostname启动数据库进程成功
History     :
"""
import unittest
from multiprocessing import Process
from testcase.utils.ComThread import ComThread
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_Gaussdb_Case0017 start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.process = Process()

    def test_systools(self):
        self.logger.info('-------若为单机环境，后续不执行-------')
        excute_cmd = f''' source {self.DB_ENV_PATH}
                           gs_om -t status --detail'''
        self.logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg)
        if 'Standby' not in msg:
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
            self.logger.info("--------查看进程，确定关闭成功--------")
            excute_cmd2 = f'''ps -ef|grep {self.userNode.ssh_user}'''
            self.logger.info(excute_cmd2)
            msg2 = self.standbyNode.sh(excute_cmd2).result()
            self.logger.info(msg2)
            self.assertFalse(self.DB_INSTANCE_PATH in msg2)
            self.logger.info("-------使用gaussdb工具后台运行进程--------")
            standby_cmd = f'''source {self.DB_ENV_PATH}
                            cat /etc/hostname;'''
            self.logger.info(standby_cmd)
            standby_hostname = self.standbyNode.sh(standby_cmd).result()
            self.logger.info(standby_hostname)
            excute_cmd3 = f'''source {self.DB_ENV_PATH};
                gaussdb -D {self.DB_INSTANCE_PATH} -p {self.userNode.db_port} \
    -h {standby_hostname} -M standby'''
            self.logger.info(excute_cmd3)
            thread_2 = ComThread(self.standbyNode2.sh, args=(excute_cmd3,))
            thread_2.setDaemon(True)
            thread_2.start()
            thread_2.join(10)
            self.logger.info("------------查看数据库是否正常链接-----------")
            sql_cmd2 = '''select user;'''
            msg2 = self.sh_standby.execut_db_sql(sql_cmd2)
            self.logger.info(msg2)
            self.common.equal_sql_mdg(msg2, 'current_user',
                                    self.standbyNode.ssh_user, '(1 row)',
                                    flag='1')

    def tearDown(self):
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0017 finish-')

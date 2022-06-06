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
Case Name   : 单机数据库启动gaussdb进程时，使用-d参数设置其值为1-5是否可以成功
Description :
    1.关闭正在运行的数据库
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.查看进程，确定关闭成功
    ps -ef|grep zl
    3.使用gaussdb工具后台运行进程，分别设置-d参数的值为1-5
    gaussdb -D /opt/openGauss_luz/cluster/dn1 -p 19703 -d 1 &
    gaussdb -D /opt/openGauss_luz/cluster/dn1 -p 19703 -d 2 &
    gaussdb -D /opt/openGauss_luz/cluster/dn1 -p 19703 -d 3 &
    gaussdb -D /opt/openGauss_luz/cluster/dn1 -p 19703 -d 4 &
    gaussdb -D /opt/openGauss_luz/cluster/dn1 -p 19703 -d 5 &
Expect      :
    1.关闭正在运行的数据库成功
    2.查看进程，数据库连接进程不存在，数据库关闭成功
    3.使用gaussdb工具后台启动数据库进程成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0061 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

    def test_systools(self):
        self.logger.info('-------若为主备环境，后续不执行-------')
        excute_cmd = f'source {self.DB_ENV_PATH};gs_om -t status --detail'
        self.logger.info(excute_cmd)
        msg0 = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg0)
        if 'Standby' in msg0:
            return self.logger.info('主备环境，后续不执行!')
        else:
            self.logger.info('--------关闭正在运行的数据库--------')
            close_db_cmd1 = f'source {self.DB_ENV_PATH};' \
                            f'gs_ctl stop -D {self.DB_INSTANCE_PATH}'
            self.logger.info(close_db_cmd1)
            close_msg1 = self.userNode.sh(close_db_cmd1).result()
            self.logger.info(close_msg1)
            self.logger.info('---使用gaussdb工具后台运行进程，设置-d参数的值为1---')
            excute_cmd1 = f'source {self.DB_ENV_PATH};gaussdb -D' \
                          f'{self.DB_INSTANCE_PATH} -p' \
                          f' {self.userNode.db_port} -d 1'
            self.logger.info(excute_cmd1)
            thread_2 = ComThread(self.userNode2.sh, args=(excute_cmd1,))
            thread_2.setDaemon(True)
            thread_2.start()
            thread_2.join(10)
            thread2_result = thread_2.get_result()
            self.logger.info(thread2_result)
            self.logger.info('-----验证数据库可以连接-----')
            connect_cmd1 = 'drop user if exists user006 cascade;'
            connect_msg1 = self.sh_primy.execut_db_sql(connect_cmd1)
            self.logger.info(connect_msg1)
            self.assertTrue(connect_msg1.find('DROP ROLE') > -1)
            self.logger.info('---使用gaussdb工具后台运行进程，设置-d参数的值为2---')
            excute_cmd2 = f'source {self.DB_ENV_PATH};gaussdb -D' \
                          f'{self.DB_INSTANCE_PATH} -p' \
                          f' {self.userNode.db_port} -d 2'
            self.logger.info(excute_cmd2)
            thread_3 = ComThread(self.userNode2.sh, args=(excute_cmd2,))
            thread_3.setDaemon(True)
            thread_3.start()
            thread_3.join(10)
            thread3_result = thread_3.get_result()
            self.logger.info(thread3_result)
            self.logger.info('-----验证数据库可以连接-----')
            connect_cmd2 = 'drop user if exists user006 cascade;'
            connect_msg2 = self.sh_primy.execut_db_sql(connect_cmd2)
            self.logger.info(connect_msg2)
            self.assertTrue(connect_msg2.find('DROP ROLE') > -1)
            self.logger.info('---使用gaussdb工具后台运行进程，设置-d参数的值为3---')
            excute_cmd3 = f'source {self.DB_ENV_PATH};gaussdb -D' \
                          f'{self.DB_INSTANCE_PATH} -p' \
                          f' {self.userNode.db_port} -d 3'
            self.logger.info(excute_cmd3)
            thread_4 = ComThread(self.userNode2.sh, args=(excute_cmd3,))
            thread_4.setDaemon(True)
            thread_4.start()
            thread_4.join(10)
            thread4_result = thread_4.get_result()
            self.logger.info(thread4_result)
            self.logger.info('-----验证数据库可以连接-----')
            connect_cmd3 = 'drop user if exists user006 cascade;'
            connect_msg3 = self.sh_primy.execut_db_sql(connect_cmd3)
            self.logger.info(connect_msg3)
            self.assertTrue(connect_msg3.find('DROP ROLE') > -1)
            self.logger.info('---使用gaussdb工具后台运行进程，设置-d参数的值为4---')
            excute_cmd4 = f'source {self.DB_ENV_PATH};gaussdb -D' \
                          f'{self.DB_INSTANCE_PATH} -p' \
                          f' {self.userNode.db_port} -d 4'
            self.logger.info(excute_cmd4)
            thread_5 = ComThread(self.userNode2.sh, args=(excute_cmd4,))
            thread_5.setDaemon(True)
            thread_5.start()
            thread_5.join(10)
            thread5_result = thread_5.get_result()
            self.logger.info(thread5_result)
            self.logger.info('-----验证数据库可以连接-----')
            connect_cmd4 = 'drop user if exists user006 cascade;'
            connect_msg4 = self.sh_primy.execut_db_sql(connect_cmd4)
            self.logger.info(connect_msg4)
            self.assertTrue(connect_msg4.find('DROP ROLE') > -1)
            self.logger.info('---使用gaussdb工具后台运行进程，设置-d参数的值为5---')
            excute_cmd5 = f'source {self.DB_ENV_PATH};gaussdb -D' \
                          f'{self.DB_INSTANCE_PATH} -p' \
                          f' {self.userNode.db_port} -d 5'
            self.logger.info(excute_cmd5)
            thread_6 = ComThread(self.userNode2.sh, args=(excute_cmd5,))
            thread_6.setDaemon(True)
            thread_6.start()
            thread_6.join(10)
            thread6_result = thread_6.get_result()
            self.logger.info(thread6_result)
            self.logger.info('-----验证数据库可以连接-----')
            connect_cmd5 = 'drop user if exists user006 cascade;'
            connect_msg5 = self.sh_primy.execut_db_sql(connect_cmd5)
            self.logger.info(connect_msg5)
            self.assertTrue(connect_msg5.find('DROP ROLE') > -1)

    def tearDown(self):
        self.logger.info('Opengauss_Function_Tools_Gaussdb_Case0061 finish')

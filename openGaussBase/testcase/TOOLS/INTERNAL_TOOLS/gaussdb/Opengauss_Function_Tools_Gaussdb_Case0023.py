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
Case Name   : 启动gaussdb进程时，使用-k参数指定正确的套接字文件目录启动是否成功
Description :
    1.查询套接字文件目录
    show unix_socket_directory;
    2.关闭正在运行的数据库（主机）
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    3.查看进程，确定关闭成功
    ps -ef|grep zl
    4.使用gaussdb工具后台运行进程
    gaussdb -D /opt/openGauss_zl/cluster/dn1 -p 19701 -k /opt/openGauss_zl
    /cluster/tmp -M primary &
Expect      :
    1.关闭正在运行的数据库成功
    2.查看进程，数据库连接进程不存在，数据库关闭成功
    3.查询套接字文件目录成功
    4.使用gaussdb工具-k指定正确的套接字文件目录启动数据库进程成功
History     :
"""
import os
import unittest
from testcase.utils.ComThread import ComThread
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Tools_Gaussdb_Case0023 start--')
        self.userNode = Node('PrimaryDbUser')
        self.userNode2 = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')

    def test_systools(self):
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
        self.logger.info("-------使用gaussdb工具后台运行进程--------")
        file_path = os.path.join(self.DB_INSTANCE_PATH, '../tmp')
        excute_cmd3 = f'source {self.DB_ENV_PATH};' \
                      f'gaussdb -D {self.DB_INSTANCE_PATH} -p ' \
                      f'{self.userNode.db_port} -k {file_path} -M primary'
        self.logger.info(excute_cmd3)
        thread_2 = ComThread(self.userNode2.sh, args=(excute_cmd3,))
        thread_2.setDaemon(True)
        thread_2.start()
        thread_2.join(10)
        msg_result_2 = thread_2.get_result()
        self.logger.info(msg_result_2)
        sql_cmd3 = 'drop user if exists user006 cascade;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find('DROP ROLE') > -1)

    def tearDown(self):
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0023 finish-')

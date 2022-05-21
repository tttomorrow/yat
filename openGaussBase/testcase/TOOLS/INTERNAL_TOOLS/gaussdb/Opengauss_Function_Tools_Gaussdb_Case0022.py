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
Case Name   : 启动gaussdb进程时，主机使用-h参数指定未知的host启动是否有合理报错
Description :
    1.关闭正在运行的数据库（主机）
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.查看进程，确定关闭成功
    ps -ef|grep zl
    3.使用gaussdb工具后台运行进程
    gaussdb -D /opt/openGauss_zl/cluster/dn1 -p 19701 -h 11.187.183.94 -M
    primary &
    4.恢复-重启数据库
    gs_ctl restart -D /opt/openGauss_zl/cluster/dn1 -M primary
Expect      :
    1.关闭正在运行的数据库成功
    2.查看进程，数据库连接进程不存在，数据库关闭成功
    3.使用gaussdb工具指定未知host启动数据库进程失败，提示信息为：FATAL:
    could not create listen socket for "11.187.183.94:19701"
    4.重启数据库成功
History     :
"""
import os
import unittest
from multiprocessing import Process
from testcase.utils.ComThread import ComThread
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.userNode = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
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
            self.logger.info("--------关闭正在运行的数据库--------")
            excute_cmd1 = f'''source {self.DB_ENV_PATH};
                    gs_ctl stop -D {self.DB_INSTANCE_PATH}'''
            self.logger.info(excute_cmd1)
            msg1 = self.userNode.sh(excute_cmd1).result()
            self.logger.info(msg1)
            self.logger.info("--------查看进程，确定关闭成功--------")
            excute_cmd2 = f'''ps -ef|grep {self.userNode.ssh_user}'''
            self.logger.info(excute_cmd2)
            msg2 = self.userNode.sh(excute_cmd2).result()
            self.logger.info(msg2)
            self.assertFalse(self.DB_INSTANCE_PATH in msg2)
            self.logger.info("-------使用gaussdb工具后台运行进程--------")
            excute_cmd3 = f'''source {self.DB_ENV_PATH};
                gaussdb -D {self.DB_INSTANCE_PATH} -p \
{self.userNode.db_port} -h 10.10.10.10 -M primary &'''
            self.logger.info(excute_cmd3)
            thread_2 = ComThread(self.userNode.sh, args=(excute_cmd3,))
            thread_2.setDaemon(True)
            thread_2.start()
            thread_2.join(10)
            msg_result_2 = thread_2.get_result()
            self.logger.info(msg_result_2.result())
            self.logger.info('------------检查数据库是否启动-----------')
            sql_cmd4 = 'drop user if exists user006 cascade;'
            msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
            self.logger.info(msg4)
            self.assertTrue(msg4.find('failed to connect') > -1)
            self.logger.info('-----------主机重启-----------')
            execute_cmd5 = f'source {self.DB_ENV_PATH};gs_ctl restart -D ' \
                           f'{self.DB_INSTANCE_PATH} -M primary'
            msg5 = self.userNode.sh(execute_cmd5).result()
            self.logger.info(msg5)
            self.logger.info('------------检查数据库状态-----------')
            execute_cmd6 = f'source {self.DB_ENV_PATH};' \
                           f'gs_om -t status --detail'
            msg6 = self.userNode.sh(execute_cmd6).result()
            self.logger.info(msg6)
            self.assertTrue(
                'P Primary Normal' in msg6 and 'S Standby Normal' in msg6)

    def tearDown(self):
        # 无须清理环境
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

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
Case Name   : 启动gaussdb进程时，主机使用-h参数指定未知的hostname启动是否有合理报错
Description :
    1.关闭正在运行的数据库（主机）
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.查看进程，确定关闭成功
    ps -ef|grep zl
    3.使用gaussdb工具后台运行进程
    gaussdb -D /opt/openGauss_zl/cluster/dn1 -p 19701 -h henc00000 &
    4.恢复-重启数据库
    gs_ctl restart -D /opt/openGauss_zl/cluster/dn1 -M primary
Expect      :
    1.关闭正在运行的数据库成功
    2.查看进程，数据库连接进程不存在，数据库关闭成功
    3.使用gaussdb工具指定未知hostname启动数据库进程失败，提示信息为：
    FATAL:  could not create listen socket for "henc00000:19701"
    4.重启数据库成功
History     :
"""
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
        self.logger.info('--Opengauss_Function_Tools_Gaussdb_Case0018 start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.primaryRoot = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.process = Process()

    def test_systools(self):
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
            gaussdb -D {self.DB_INSTANCE_PATH} -p {self.userNode.db_port} \
    -h henc00000 -M standby'''
        self.logger.info(excute_cmd3)
        thread_2 = ComThread(self.userNode.sh, args=(excute_cmd3,))
        thread_2.setDaemon(True)
        thread_2.start()
        thread_2.join(10)
        msg_result_2 = thread_2.get_result()
        self.logger.info(msg_result_2.result())
        self.logger.info("------------恢复重启数据库-----------")
        excute_cmd3 = f'''source {self.DB_ENV_PATH};
                gs_ctl restart -D {self.DB_INSTANCE_PATH} -M primary'''
        self.logger.info(excute_cmd3)
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        sql_cmd4 = '''drop user if exists user006 cascade;'''
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.assertTrue(msg4.find("DROP ROLE") > -1)

    def tearDown(self):
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0018 finish-')

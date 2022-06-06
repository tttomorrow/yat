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
Case Name   : 启动gaussdb进程时，使用-S参数设置值大于最大值，启动是否成功
Description :
    1.关闭正在运行的数据库
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.使用gaussdb工具设置-S参数的值大于最大值，启动数据库
    gaussdb -D /opt/openGauss_zl/cluster/dn1 -p 19701 -S 2147483648 -M primary
Expect      :
    1.关闭正在运行的数据库成功
    2.使用gaussdb工具设置-S参数的值大于最大值，启动数据库失败
History     :
"""
import unittest
import os
from multiprocessing import Process

from testcase.utils.ComThread import ComThread
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'---{os.path.basename(__file__)} start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
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
        self.logger.info("----使用gaussdb工具设置-p参数为不存在的端口号启动---")
        excute_cmd3 = f'''source {self.DB_ENV_PATH};
             gaussdb -D {self.DB_INSTANCE_PATH} -p {self.userNode.db_port} \
-S 2147483648 -M primary'''
        self.logger.info(excute_cmd3)
        thread_2 = ComThread(self.userNode2.sh, args=(excute_cmd3,))
        thread_2.setDaemon(True)
        thread_2.start()
        thread_2.join(10)
        msg_result_2 = thread_2.get_result()
        self.logger.info(msg_result_2.result())
        excute_cmd3 = '''drop user if exists user006 cascade;'''
        msg3 = self.sh_primy.execut_db_sql(excute_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find("failed to connect") > -1)

    def tearDown(self):
        self.logger.info('-----------恢复数据库状态-----------')
        excute_cmd1 = f'''source {self.DB_ENV_PATH};
                gs_om -t stop && gs_om -t start'''
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        excute_cmd2 = '''drop user if exists user006 cascade;'''
        msg2 = self.sh_primy.execut_db_sql(excute_cmd2)
        self.logger.info(msg2)
        self.assertTrue(msg2.find("DROP ROLE") > -1)
        self.logger.info(f'---{os.path.basename(__file__)} finish---')

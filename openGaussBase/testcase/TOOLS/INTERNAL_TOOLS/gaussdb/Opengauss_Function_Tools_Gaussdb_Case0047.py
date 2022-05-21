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
Case Name   : 在单机数据库上执行gaussdb指定--single_node启动是否成功
Description :
    1.关闭正在运行的数据库
    gs_ctl stop -D /opt/openGauss_luz/cluster/dn1
    2.使用gaussdb工具指定--single_node启动数据库
    gaussdb -D /opt/openGauss_luz/cluster/dn1 -p 19703 --single_node &
    3.查看集群状态是否正常
    gs_om -t status --detail
Expect      :
    1.关闭正在运行的数据库成功
    2.使用gaussdb工具指定--single_node启动数据库成功
    3.查看数据库状态成功，集群状态正常
History     :
"""
import unittest
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
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0047 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.process = Process()

    def test_systools(self):
        self.logger.info('-------若为主备环境，后续不执行-------')
        excute_cmd = f''' source {self.DB_ENV_PATH}
                   gs_om -t status --detail'''
        self.logger.info(excute_cmd)
        msg = self.userNode.sh(excute_cmd).result()
        self.logger.info(msg)
        if '6002' in msg or '6003' in msg:
            return '主备环境，后续不执行!'
        else:
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
            self.logger.info("----使用gaussdb工具启动---")
            excute_cmd3 = f'''source {self.DB_ENV_PATH};
                 gaussdb -D {self.DB_INSTANCE_PATH} -p \
{self.userNode.db_port} --single_node'''
            self.logger.info(excute_cmd3)
            thread_2 = ComThread(self.userNode.sh, args=(excute_cmd3,))
            thread_2.setDaemon(True)
            thread_2.start()
            thread_2.join(10)
            excute_cmd4 = f'''source {self.DB_ENV_PATH};
                        gs_om -t status --detail'''
            self.logger.info(excute_cmd4)
            msg4 = self.userNode.sh(excute_cmd4).result()
            self.logger.info(msg4)
            self.assertTrue(msg4.find("P Primary Normal") > -1)

    def tearDown(self):
        self.logger.info('------清理内存，预防重启失败------')
        excute_cmd1 = 'echo 3 > /proc/sys/vm/drop_caches'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0047 finish-')

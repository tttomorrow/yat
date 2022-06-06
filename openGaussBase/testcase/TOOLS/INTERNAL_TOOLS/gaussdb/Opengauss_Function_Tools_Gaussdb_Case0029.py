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
Case Name   : 启动gaussdb进程时，使用-N参数设置服务器接受的客户端连接的最大数为负数，
                启动是否成功
Description :
    1.查看当前最大连接数
    show max_connections;
    2.关闭正在运行的数据库（主机）
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    3.查看进程，确定关闭成功
    ps -ef|grep zl
    4.使用gaussdb工具指定-N参数设置最大连接数为小数，后台运行进程
    gaussdb -D /opt/openGauss_zl/cluster/dn1 -p 19701 -N -10  -M primary &
    5.恢复-重启数据库
    gs_ctl restart -D /opt/openGauss_zl/cluster/dn1 -M primary
Expect      :
    1.查看当前最大连接数成功
    2.关闭正在运行的数据库成功
    3.查看进程，数据库连接进程不存在，数据库关闭成功
    4.使用gaussdb工具指定-N参数设置最大连接数为小数，启动数据库进程失败，提示信息为：
    FATAL:  invalid value for parameter "max_connections": "-10"
    5.重启数据库成功
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
        self.logger.info(f'---{os.path.basename(__file__)} start---')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.process = Process()

    def test_systools(self):
        self.logger.info("-------------查看当前最大连接数-----------")
        sql_cmd0 = '''show max_connections;'''
        msg0 = self.sh_primy.execut_db_sql(sql_cmd0)
        self.logger.info(msg0)
        self.common.equal_sql_mdg(msg0, 'max_connections', '5000', '(1 row)',
                                flag='1')
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
        self.logger.info("-----使用gaussdb工具指定指定-N参数设置最大连接数为负数----")
        excute_cmd3 = f'''source {self.DB_ENV_PATH};
             gaussdb -D {self.DB_INSTANCE_PATH} -p {self.userNode.db_port} \
-N -10 -M primary
            '''
        self.logger.info(excute_cmd3)
        thread_2 = ComThread(self.userNode2.sh, args=(excute_cmd3,))
        thread_2.setDaemon(True)
        thread_2.start()
        thread_2.join(10)
        msg_result_2 = thread_2.get_result()
        self.logger.info(msg_result_2.result())

        sql_cmd3 = '''drop user if exists user006 cascade;'''
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find("failed to connect") > -1)

    def tearDown(self):
        self.logger.info('-------恢复配置-----------')
        excute_cmd1 = f'''source {self.DB_ENV_PATH};
            gs_om -t stop && gs_om -t start;'''
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = '''show max_connections;'''
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'max_connections', '5000', '(1 row)',
                                flag='1')
        self.logger.info(f'---{os.path.basename(__file__)} finish---')

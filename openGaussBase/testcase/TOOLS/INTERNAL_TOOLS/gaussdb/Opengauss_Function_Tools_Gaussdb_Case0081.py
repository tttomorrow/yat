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
Case Name   : gaussdb指定-x参数开启自启动模式是否成功
Description :
    1.关闭正在运行的数据库
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.使用gaussdb工具指定-x启动数据库自启动模式
    gaussdb --boot -D /opt/openGauss_agl/cluster/dn1/ -x 2 &
Expect      :
    1.关闭正在运行的数据库成功
    2.gaussdb指定-x参数开启自启动模式成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '主备环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0081 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH

    def test_systools(self):
        self.logger.info('--------关闭正在运行的数据库--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_ctl stop -D ' \
                      f'{self.DB_INSTANCE_PATH}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('-------使用gaussdb工具后台运行进程--------')
        excute_cmd3 = f'source {self.DB_ENV_PATH};gaussdb --boot -D ' \
                      f'{self.DB_INSTANCE_PATH} -x 2'
        self.logger.info(excute_cmd3)
        thread_2 = ComThread(self.userNode2.sh, args=(excute_cmd3,))
        thread_2.setDaemon(True)
        thread_2.start()
        thread_2.join(10)
        self.logger.info('------------连接数据库-----------')
        sql_cmd3 = 'drop user if exists user006 cascade;'
        msg3 = Primary_SH.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        self.assertTrue(msg3.find('failed to connect') > -1)
        self.logger.info('----------恢复状态---------')
        excute_single = f'source {self.DB_ENV_PATH};' \
                        f'gs_ctl start -D \'{self.DB_INSTANCE_PATH}\';'
        single_msg = self.userNode.sh(excute_single).result()
        self.logger.info(single_msg)
        self.logger.info('--------检查集群状态是否正常--------')
        excute_cmd9 = f'source {self.DB_ENV_PATH};gs_om -t status --detail'
        msg9 = self.userNode.sh(excute_cmd9).result()
        self.assertTrue('P Primary Normal' in msg9)

    def tearDown(self):
        self.logger.info('Opengauss_Function_Tools_Gaussdb_Case0081 finish')

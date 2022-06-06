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
Case Name   : 使用gaussdb开启自启动模式是否成功
Description :
    1.关闭正在运行的数据库
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.直接使用gaussdb工具指定自启动方式启动数据库是否无明显感知
    gaussdb --boot -D /opt/openGauss_zl/cluster/dn1  
    3.恢复-重启数据库
    gs_ctl restart -D /opt/openGauss_zl/cluster/dn1 -M primary
Expect      :
    1.关闭正在运行的数据库成功
    2.使用gaussdb工具设置数据库自启动成功，无明显感知（执行完成后自动退出，无报错）
    3.恢复-重启主数据库成功
History     :
"""
import unittest
from time import sleep

from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '主备环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0067 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH

    def test_systools(self):
        self.logger.info('--------关闭正在运行的数据库--------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};gs_ctl stop -D ' \
                      f'{self.DB_INSTANCE_PATH}'
        self.logger.info(excute_cmd1)
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        self.logger.info('--------查看进程，确定关闭成功--------')
        excute_cmd2 = f'ps -ef|grep {self.userNode.ssh_user}'
        self.logger.info(excute_cmd2)
        msg2 = self.userNode.sh(excute_cmd2).result()
        self.logger.info(msg2)
        self.assertFalse(self.DB_INSTANCE_PATH in msg2)
        self.logger.info('-------使用gaussdb工具后台运行进程--------')
        excute_cmd3 = f'source {self.DB_ENV_PATH};gaussdb --boot -D ' \
                      f'{self.DB_INSTANCE_PATH}'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        sql_cmd4 = 'drop user if exists user006 cascade;'
        msg4 = Primary_SH.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.assertTrue('failed to connect' in msg4)
        self.logger.info('------------恢复数据库-----------')
        excute_cmd5 = f'source {self.DB_ENV_PATH};gs_ctl start -D' \
                      f' {self.DB_INSTANCE_PATH} -M primary;'
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.logger.info(msg5)
        sleep(3)
        sql_cmd6 = 'drop user if exists user006 cascade;'
        msg6 = Primary_SH.execut_db_sql(sql_cmd6)
        self.logger.info(msg6)
        self.assertTrue(msg6.find('DROP ROLE') > -1)

    def tearDown(self):
        self.logger.info('Opengauss_Function_Tools_Gaussdb_Case0067 finish')

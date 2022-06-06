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
Case Name   : 使用gaussdb开启自启动模式，未将--boot参数第一位是否成功
Description :
    1.关闭正在运行的数据库
    gs_ctl stop -D /opt/openGauss_zl/cluster/dn1
    2.直接使用gaussdb工具指定自启动方式启动数据库是否无明显感知
    gaussdb -D /opt/openGauss_zl/cluster/dn1  --boot
    3.恢复-重启数据库
    gs_ctl restart -D /opt/openGauss_zl/cluster/dn1 -M primary
Expect      :
    1.关闭正在运行的数据库成功
    2.使用gaussdb工具设置数据库自启动失败，报错信息为：FATAL:  --boot requires a value
    3.恢复-重启主数据库成功
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('-Opengauss_Function_Tools_Gaussdb_Case0068 start-')
        self.userNode = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()

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
        excute_cmd3 = f'source {self.DB_ENV_PATH};gaussdb -D' \
                      f' {self.DB_INSTANCE_PATH} --boot'
        msg3 = self.userNode.sh(excute_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.find('--boot requires a value'))
        self.logger.info("------------恢复数据库-----------")
        excute_cmd5 = f'source {self.DB_ENV_PATH};gs_ctl restart -D ' \
                      f'{self.DB_INSTANCE_PATH};'
        msg5 = self.userNode.sh(excute_cmd5).result()
        self.logger.info(msg5)
        sql_cmd6 = 'drop user if exists user006 cascade;'
        msg6 = self.sh_primy.execut_db_sql(sql_cmd6)
        self.logger.info(msg6)
        self.assertTrue(msg6.find('DROP ROLE') > -1)

    def tearDown(self):
        self.logger.info('Opengauss_Function_Tools_Gaussdb_Case0068 finish')

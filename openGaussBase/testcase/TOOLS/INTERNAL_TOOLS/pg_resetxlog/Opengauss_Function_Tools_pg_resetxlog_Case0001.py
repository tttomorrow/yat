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
Case Name   : 数据库在运行状态，执行pg_resetxlog命令
Description :
    1.执行pg_resetxlog命令
    pg_resetxlog /opt/openGauss_zl/cluster/dn1/
    2.查看执行结果，是否有提示信息
Expect      :
    1.执行pg_resetxlog命令失败
    2.执行失败，提示信息为pid文件已存在
History     :
"""
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')
Logger = Logger()


@unittest.skipIf('Standby' not in Primary_SH.get_db_cluster_status('detail'),
                 '单机环境不执行')
class Tools(unittest.TestCase):
    def setUp(self):
        Logger.info(
            '---Opengauss_Function_Tools_pg_resetxlog_Case0001 start---')
        self.userNode = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH

    def test_systools(self):
        Logger.info('-------若为单机环境，后续不执行-------')
        excute_cmd0 = f'source {self.DB_ENV_PATH};gs_om -t status --detail'
        Logger.info(excute_cmd0)
        msg0 = self.userNode.sh(excute_cmd0).result()
        Logger.info(msg0)
        Logger.info('--执行pg_resetxlog命令失败，提示信息为pid文件已存--')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'pg_resetxlog {self.DB_INSTANCE_PATH};'
        Logger.info(excute_cmd1)
        execute_msg1 = self.userNode.sh(excute_cmd1).result()
        Logger.info(execute_msg1)
        self.assertTrue(
            execute_msg1.find('lock file "postmaster.pid" exists') > -1)

    def tearDown(self):
        Logger.info(
            '----Opengauss_Function_Tools_pg_resetxlog_Case0001 finish----')

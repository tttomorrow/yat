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
Case Name   : 执行初始化数据库命令gs_initdb：指定参数--show，显示内部设置
Description :
    1.执行命令：gs_initdb -D $data/ --nodename=single -w $password --show
Expect      :
    1.内部设置内容打印到屏幕上
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger

Logger = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        Logger.info('----Opengauss_Function_gs_initdb_Case0033 start----')
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH, 'datadir')

    def test_systools(self):
        Logger.info('------执行gs_initdb命令------')
        excute_cmd1 = f'source {self.DB_ENV_PATH};' \
                      f'gs_initdb -D {self.dir_path} --nodename=single --show'
        Logger.info(excute_cmd1)
        msg2 = self.userNode.sh(excute_cmd1).result()
        Logger.info(msg2)
        msg_list = ['VERSION', 'PGDATA', 'share_path', 'PGPATH',
                    'POSTGRES_SUPERUSERNAME', 'POSTGRES_BKI',
                    'POSTGRES_DESCR', 'POSTGRES_SHDESCR',
                    'POSTGRESQL_CONF_SAMPLE', 'MOT_CONF_SAMPLE',
                    'PG_HBA_SAMPLE', 'PG_IDENT_SAMPLE']
        for content in msg_list:
            self.assertTrue(content in msg2)

    def tearDown(self):
        Logger.info('---Opengauss_Function_gs_initdb_Case0033 finish---')

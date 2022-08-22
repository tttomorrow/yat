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
Case Type   : dolphin
Case Name   : 恢复数据库
Description :
    1、查询当前数据库
    2、删除兼容b库并重新创建数据库
    2、删除插件依赖文件
Expect      :
    1、成功
    2、成功
    3、成功
History     :
"""

import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class CompatibilityTest02(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.common = Common()
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.constant = Constant()
        self.part_path = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.put_path1 = os.path.join(self.part_path, 'app', 'lib',
                                      'postgresql')
        self.put_path2 = os.path.join(self.part_path, 'app', 'share',
                                      'postgresql', 'extension')
        self.log.info('判断操作系统')
        cmd = 'arch'
        res = self.user_node.sh(cmd).result().strip()
        self.dir_name = 'plat_X86' if res == 'x86_64' else 'plat_ARM'
        self.plugin_path = os.path.dirname(
            os.path.dirname(os.path.dirname(macro.FTP_PATH)))
        self.dolphin_path = os.path.join(self.plugin_path,
                                         'plugins', 'dolphin', self.dir_name)
        self.get_path1 = os.path.join(self.dolphin_path, 'dolphin.so')

    def test_dolphin(self):
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        text = '--step1:查询当前数据库;expect:成功--'
        self.log.info(text)
        sql_cmd = "select current_database();"
        self.log.info(sql_cmd)
        sql_res = self.sh_primary.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn(self.user_node.db_name, sql_res, '执行失败' + text)

    def tearDown(self):
        text = '----step2:删除兼容b库并重新创建数据库;expect:成功----'
        self.log.info(text)
        sql_cmd = f"drop database if exists {self.user_node.db_name};" \
                  f"create database {self.user_node.db_name};"
        self.log.info(sql_cmd)
        sql_res = self.sh_primary.execut_db_sql(sql_cmd, dbname='postgres')
        self.log.info(sql_res)
        text = '--step3:删除插件依赖文件;expect:成功--'
        self.log.info(text)
        rm_cmd = f"rm -rf {self.put_path1}/b_sql_plugin.so;" \
                 f"rm -rf {self.put_path2}/b_sql_plugin.control;" \
                 f"rm -rf {self.put_path2}/b_sql_plugin--1.0.sql"
        self.log.info(rm_cmd)
        rm_msg = self.user_node.sh(rm_cmd).result()
        self.log.info(rm_msg)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_res,
                      '执行失败' + text)
        self.assertEqual(len(rm_msg), 0, '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

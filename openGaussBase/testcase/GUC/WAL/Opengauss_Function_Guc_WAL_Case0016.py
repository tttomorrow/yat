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
Case Type   : GUC
Case Name   : 查看参数wal_segment_size，并尝试修改（用户不可修改）
Description :
    1、查看wal_segment_size默认值；
    show wal_segment_size;
    2、修改wal_segment_size为正常值10MB,校验其预期结果；
    gs_guc set -D {cluster/dn1} -c "wal_segment_size=10MB";
Expect      :
    1、显示默认值；
    2、参数修改失败；
History     :
"""

import sys
import unittest
from yat.test import macro
from yat.test import Node

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('PrimaryDbUser')

class Guctestcase(unittest.TestCase):
    def setUp(self):
        logger.info("------------------------Opengauss_Function_Guc_WAL_Case0016开始执行-----------------------------")
        self.userNode = Node('PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.Constant = Constant()
        self.stopstartCmd = f'source {macro.DB_ENV_PATH};gs_om -t stop && gs_om -t start'
        self.statusCmd = f'source {macro.DB_ENV_PATH};gs_om -t status --detail'

    def test_common_user_permission(self):
        logger.info("------------------------查询wal_segment_size 期望：默认值10MB---------------------------")
        sql_cmd = commonsh.execut_db_sql(f'''show wal_segment_size;''')
        logger.info(sql_cmd)
        self.assertIn("16MB", sql_cmd)

        logger.info("-----------修改wal_segment_size为正常值10MB,校验其预期结果；-------------")
        logger.info("----------期望：设置失败-------------")
        sql_cmd = '''source ''' + self.DB_ENV_PATH + f''';gs_guc reload -D {self.DB_INSTANCE_PATH} -c "wal_segment_size=10MB"'''
        logger.info(sql_cmd)
        msg = self.userNode.sh(sql_cmd).result()
        logger.info(msg)
        self.assertIn(self.Constant.SQL_WRONG_MSG[1], msg)

    def tearDown(self):
        logger.info("--------------------------------恢复默认值无需恢复-----------------------------------")
        logger.info("-------------------------Opengauss_Function_Guc_WAL_Case0016执行结束---------------------------")
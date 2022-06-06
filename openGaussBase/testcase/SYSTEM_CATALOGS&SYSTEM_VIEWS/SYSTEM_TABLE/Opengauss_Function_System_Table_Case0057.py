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
Case Type   : 系统表
Case Name   : 测试系统表PG_STATISTIC字段与数据类型
Description :
    1.查看系统表PG_STATISTIC的表结构
    2.该表字段与对应字段数据类型是否正确
Expect      :
    1.查看系统表PG_STATISTIC的表结构成功
    2.该表字段与字段数据类型对应正确
History     :
"""

import sys
import unittest
from yat.test import Node
from yat.test import macro

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class IndexFileDamaged(unittest.TestCase):
    def setUp(self):
        logger.info('----------------this is setup-----------------------')
        logger.info('--------------Opengauss_Function_System_Table_Case0057开始执行--------------')
        self.userNode = Node('dbuser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.com = Common()
        self.comsh = CommonSH('dbuser')
        self.expect_result_dict = {
            'Column': ['starelid', 'starelkind', 'staattnum', 'stainherit', 'stanullfrac', 'stawidth', 'stadistinct',
                       'stakind1', 'stakind2', 'stakind3', 'stakind4', 'stakind5', 'staop1', 'staop2', 'staop3',
                       'staop4', 'staop5', 'stanumbers1', 'stanumbers2', 'stanumbers3', 'stanumbers4', 'stanumbers5',
                       'stavalues1', 'stavalues2', 'stavalues3', 'stavalues4', 'stavalues5', 'stadndistinct',
                       'staextinfo'],
            'Type': ['oid', '"char"', 'smallint', 'boolean', 'real', 'integer', 'real', 'smallint', 'smallint',
                     'smallint', 'smallint', 'smallint', 'oid', 'oid', 'oid', 'oid', 'oid', 'real[]', 'real[]',
                     'real[]', 'real[]', 'real[]', 'anyarray', 'anyarray', 'anyarray', 'anyarray', 'anyarray', 'real',
                     'text']}

    def test_Index_file_damaged(self):
        logger.info('----------------------------查看表结构-----------------------------')
        msg = self.comsh.execut_db_sql('\d PG_STATISTIC')
        logger.info(msg)
        result_dict = self.com.format_sql_result(msg)
        logger.info(result_dict)
        del result_dict['Modifiers']
        self.assertDictEqual(self.expect_result_dict, result_dict)

    def tearDown(self):
        logger.info('----------------this is tearDown-----------------------')
        # 无须清理环境
        logger.info('-----------------------Opengauss_Function_System_Table_Case0057执行完成-----------------------------')

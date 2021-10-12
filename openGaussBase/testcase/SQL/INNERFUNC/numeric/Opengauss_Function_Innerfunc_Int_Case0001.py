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
Case Type   : 时间/日期函数
Case Name   : 数据库格式为B风格时，函数int1()、int2()、int4()的使用
Description :
    1.创建B风格的数据库
    2.数据库B风格情况下使用函数in1()、int2()、int4()
Expect      :
    1.创建B风格的数据库成功
    2.数据库B风格情况下使用函数in1()、int2()、int4()成功
History     : 
"""

import unittest
from yat.test import macro
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()


class Functions(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_Int_Case0001开始-')
        self.dbuser_node = Node('dbuser')
        self.constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_manage(self):
        LOG.info('---步骤1.创建B风格的数据库---')
        sql_cmd = self.commonsh.execut_db_sql(f'create database test_int '
                                              f'dbcompatibility \'B\';')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)

        LOG.info('---步骤2.数据库B风格情况下使用函数in1()、int2()、int4()---')
        sql_cmd = f'select int1(\'abc\');' \
            f'select int2(\'你好\');' \
            f'select int4(\'abc\');'
        excute_cmd = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d test_int -p ' \
            f'{self.dbuser_node.db_port} -c "{sql_cmd}"'
        LOG.info(excute_cmd)
        msg = self.dbuser_node.sh(excute_cmd).result()
        LOG.info(msg)
        self.assertIn('0', msg)

    def tearDown(self):
        LOG.info('------------------------清理环境-------------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'drop database test_int;')
        LOG.info(sql_cmd)
        LOG.info('---Opengauss_Function_Innerfunc_Int_Case0001执行结束----')

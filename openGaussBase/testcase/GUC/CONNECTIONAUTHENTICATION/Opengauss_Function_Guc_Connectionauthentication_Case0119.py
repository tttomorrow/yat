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
Case Type   : GUC参数--连接认证
Case Name   : 使用alter system set修改数据库参数application_name
Description :
        1.查询application_name默认值
        2.alter system set方法修改参数值为dn_6001
        3.恢复默认值
Expect      :
        1.显示默认值gsql
        2.设置失败
        3.恢复默认值完成
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

commonsh = CommonSH('dbuser')


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0119start-')
        self.Constant = Constant()
        self.userNode = Node('dbuser')

    def test_application_name(self):
        self.log.info('步骤1:查询application_name默认值')
        sql_cmd = commonsh.execut_db_sql('''show application_name;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        self.log.info('步骤2:set方法修改参数值')
        sql_cmd = commonsh.execut_db_sql("alter system set application_name "
                                         "to 'dn_6001';")
        self.log.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd)

    def tearDown(self):
        self.log.info('---------无须清理环境---------')
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0119finish-')

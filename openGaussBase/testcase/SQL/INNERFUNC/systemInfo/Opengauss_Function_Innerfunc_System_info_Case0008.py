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
Case Type   : 系统信息函数
Case Name   :  pg_is_other_temp_schema(oid) 查看是否为另一个会话的临时模式
Description :
    1.pg_is_other_temp_schema(oid) 查看是否为另一个会话的临时模式,
    没有创建临时表,oid为0
Expect      :
     1.返回f
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Functions(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_Innerfunc_System_Info_Case0008开始')
        self.commonsh = CommonSH('dbuser')

    def test_func_sys_info(self):
        self.log.info('-step1:pg_is_other_temp_schema(oid) 查看是否为另一个'
                      '会话的临时模式,没有创建临时表,oid为0;expect:返回f-')
        sql_cmd = self.commonsh.execut_db_sql('select  pg_is_other_temp_schema'
                                              '(0);')
        self.log.info(sql_cmd)
        self.assertIn('f', sql_cmd)

    def tearDown(self):
        self.log.info('-------无需清理环境-------')
        self.log.info('Opengauss_Function_Innerfunc_System_Info_Case0008结束')

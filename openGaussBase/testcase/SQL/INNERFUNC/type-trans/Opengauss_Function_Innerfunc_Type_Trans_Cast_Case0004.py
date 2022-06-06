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
Case Type   : 功能测试
Case Name   : cast函数转换合法值为浮点数
Description :
    步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
    步骤 2.入参是符合转换的类型
Expect      : 
    步骤 1：数据库状态正常
    步骤 2：成功转换为浮点数类型
History     : 
"""
import unittest
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class Cast_function(unittest.TestCase):

    def setUp(self):
        logger.info("--------Opengauss_Function_Innerfunc_Type_Trans_Cast_Case0004开始执行------------")
        self.commonsh = CommonSH('dbuser')

    def test_function(self):
        logger.info("--------------------------------入参给定浮点数------------------------------------")

        sql_list = [r"""select cast('7.12345678' as real);""",
                    r"""select cast('1234567.12345678' as double precision);""",
                    r"""select cast(123456789123456.12345678 as real);""",
                    r"""select cast(1234.1234567891298765 as double precision);""",
                    r"""select cast(1234567891234567.12345678::double precision as real);"""]

        result_list = ['7.12346', '1234567.12345678', '1.23457e+14', '1234.12345678913', '1.23457e+15']
        for i in range(5):
            msg = self.commonsh.execut_db_sql(sql_list[i])
            logger.info(msg)
            self.assertTrue(msg.splitlines()[2].strip() == result_list[i])

    def tearDown(self):
        logger.info('----------Opengauss_Function_Innerfunc_Type_Trans_Cast_Case0004执行结束---------')

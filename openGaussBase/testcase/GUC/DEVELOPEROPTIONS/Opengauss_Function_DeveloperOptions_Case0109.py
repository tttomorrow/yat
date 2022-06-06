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
Case Type   : GUC
Case Name   : 创建函数，参数个数为8193,合理报错
Description :
        1.查询max_function_args默认值
        2.创建函数，参数个数为8193
Expect      :
        1.显示默认值为8192
        2.合理报错
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DeveloperOptions(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '------Opengauss_Function_DeveloperOptions_Case0109start------')
        self.constant = Constant()
        self.com = CommonSH('dbuser')
        self.fun_name = "fun_DeveloperOptions_Case0109"
        self.args = ','.join(
            ['para' + str(i) + ' int' for i in range(1, 8194)])

    def test_max_function_args(self):
        text = '--步骤1:查看默认值;expect:默认值为8192--'
        self.log.info(text)
        sql_cmd = self.com.execut_db_sql(f'''show max_function_args;''')
        self.log.info(sql_cmd)
        self.assertEqual('8192', sql_cmd.split('\n')[2].strip(),
                         '执行失败:' + text)
        text = '--步骤2:创建函数，参数个数为8193;expect:合理报错--'
        self.log.info(text)
        sql_cmd = self.com.execut_db_sql(f'''CREATE OR REPLACE FUNCTION \
        {self.fun_name}({self.args}) RETURNS integer AS \$\$
                BEGIN
                        RETURN i + 1;
                END;
        \$\$ LANGUAGE plpgsql;
        ''')
        self.log.info(sql_cmd)
        self.assertIn('RROR:  functions cannot have more than 8192 arguments',
                      sql_cmd, '执行失败:' + text)

    def tearDown(self):
        self.log.info('无须清理环境')
        self.log.info(
            '----Opengauss_Function_DeveloperOptions_Case0109finish---')

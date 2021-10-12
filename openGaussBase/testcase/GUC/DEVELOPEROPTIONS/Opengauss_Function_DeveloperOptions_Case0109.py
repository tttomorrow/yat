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
Case Name   : 创建函数，参数个数为667,合理报错
Description :
        1.查询max_function_args默认值
        2.创建函数，参数个数为667
Expect      :
        1.显示默认值为666
        2.合理报错
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class DeveloperOptions(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '------Opengauss_Function_DeveloperOptions_Case0109start------')
        self.constant = Constant()
        self.args = ','.join(['para' + str(i) + ' int' for i in range(1, 668)])

    def test_max_function_args(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql(f'''show max_function_args;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 创建函数，报错
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql(f'''
        create or replace function func_052 ({self.args})
       returns SETOF RECORD
as \$\$
begin
    result_1 = i + 1;
    result_2 = i * 10;
return next;
end;
\$\$language plpgsql;''')
        LOG.info(sql_cmd)
        self.assertIn(
        'ERROR:  functions cannot have more than 666 arguments', sql_cmd)

    def tearDown(self):
        LOG.info('----------------this is teardown-----------------------')
        LOG.info(
            '----Opengauss_Function_DeveloperOptions_Case0109finish---')

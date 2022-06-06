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
Case Name   : 使用gs_guc set方法设置参数max_function_args
Description :
        1.查询max_function_args默认值
        2.测试点一：创建函数，参数个数为8192个
        3.测试点二：修改参数值为12345
        4.恢复参数默认值
Expect      :
        1.显示默认值为666
        2.创建成功
        3.合理报错，为固定参数，用户无法修改此参数，只能查看
        4.默认值恢复成功
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DeveloperOptions(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '------Opengauss_Function_DeveloperOptions_Case0052start------')
        self.constant = Constant()
        self.com = CommonSH('dbuser')
        self.args = ','.join(
            ['para' + str(i) + ' int' for i in range(1, 8193)])
        self.fun_name = "fun_DeveloperOptions_Case0052"

    def test_max_function_args(self):
        text = '--步骤1:查看默认值;expect:默认值是8192--'
        self.log.info(text)
        sql_cmd = self.com.execut_db_sql('''show max_function_args;''')
        self.log.info(sql_cmd)
        self.assertEqual('8192', sql_cmd.split('\n')[2].strip(),
                         '执行失败:' + text)
        text = '--步骤2:创建函数，参数个数为8192个;expect:创建成功--'
        self.log.info(text)
        sql_cmd = self.com.execut_db_sql(f'''CREATE OR REPLACE FUNCTION \
        {self.fun_name}({self.args}) RETURNS integer AS \$\$
                BEGIN
                        RETURN i + 1;
                END;
        \$\$ LANGUAGE plpgsql;
        ''')
        self.log.info(sql_cmd)
        self.assertIn('CREATE FUNCTION', sql_cmd, '执行失败:' + text)
        text = '--步骤3:设置参数为12345并重启数据库;expect:设置报错--'
        self.log.info(text)
        sql_cmd = self.com.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'max_function_args = 12345')
        self.log.info(sql_cmd)
        self.assertFalse(sql_cmd, '执行失败:' + text)
        text = '--步骤4:查询该参数修改后的值;expect:参数值不变--'
        self.log.info(text)
        sql_cmd = self.com.execut_db_sql('''show max_function_args;''')
        self.log.info(sql_cmd)
        self.assertIn('8192', sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--步骤5:恢复默认值;expect:恢复完成--'
        self.log.info(text)
        sql_cmd = self.com.execut_db_sql(f'''drop function {self.fun_name};''')
        self.log.info(sql_cmd)
        sql_cmd = self.com.execut_db_sql('''show max_function_args;''')
        self.log.info(sql_cmd)
        if "8192" != sql_cmd.split('\n')[-2].strip():
            msg = self.com.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         'max_function_args=8192')
            self.log.info(msg)
            msg = self.com.restart_db_cluster()
            self.log.info(msg)
        status = self.com.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.com.execut_db_sql('''show max_function_args;''')
        self.log.info(sql_cmd)
        self.log.info(
            '----Opengauss_Function_DeveloperOptions_Case0052finish---')

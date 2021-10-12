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
Case Name   : 修改参数max_stack_depth，观察预期结果；
Description :
        1、查询max_stack_depth默认值；
        2、创建复杂函数
        3、修改max_stack_depth为3MB，重启使其生效，并校验其预期结果；
        4、恢复默认值；
Expect      :
        1、显示默认值2MB；
        2、创建失败，因为该值较小，导致无法执行复杂的函数
        3、参数修改成功，校验修改后系统参数值为3MB；
        4、恢复默认值成功；
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Deletaduit(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '---Opengauss_Function_Guc_Resource_Case00045.py start----')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')
        self.args = ','.join(['para' + str(i) + ' int' for i in range(1, 667)])

    def test_startdb(self):
        self.log.info('查询该参数默认值')
        sql_cmd = self.commonsh.execut_db_sql(f'''show max_stack_depth;''')
        self.log.info(sql_cmd)
        self.assertEqual('2MB', sql_cmd.splitlines()[-2].strip())
        self.log.info('创建复杂函数')
        sql_cmd = self.commonsh.execut_db_sql(f'''create or replace function \
        func_052 ({self.args})
        returns SETOF RECORD
        as \$\$
        begin
            result_1 = i + 1;
            result_2 = i * 10;
        return next;
        end;
        \$\$language plpgsql;''')
        self.log.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd)
        self.log.info('gs_guc set设置max_stack_depth')
        msg = self.commonsh.execute_gsguc('set',
                                          self.Constant.GSGUC_SUCCESS_MSG,
                                          'max_stack_depth=3MB')
        self.log.info(msg)
        self.assertTrue(msg)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('查询修改后的值')
        sql_cmd = self.commonsh.execut_db_sql(f'''show max_stack_depth;''')
        self.log.info(sql_cmd)
        self.assertIn('3MB', sql_cmd)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''show max_stack_depth;''')
        self.log.info(sql_cmd)
        if "2MB" != sql_cmd.splitlines()[-2].strip():
            msg = self.commonsh.execute_gsguc('set',
                                              self.Constant.GSGUC_SUCCESS_MSG,
                                              "max_stack_depth='2MB'")
            self.log.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('-Opengauss_Function_Guc_Resource_Case0045.py执行完成-')

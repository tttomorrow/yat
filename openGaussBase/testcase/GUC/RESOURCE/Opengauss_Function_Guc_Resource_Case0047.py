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
Case Name   : 修改参数cstore_buffers，观察预期结果；
Description :
        1、查询cstore_buffers默认值；
        2、修改cstore_buffers为30mb，重启使其生效，并校验其预期结果；
        3、创建列存表并使用explain语句
        4、恢复默认值；
Expect      :
        1、显示默认值；
        2、参数修改成功，校验修改后系统参数值为30MB；
        3、列存表使用explain语句后，显示Buffers: shared hit信息
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
            '---Opengauss_Function_Guc_Resource_Case00047.py start------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_startdb(self):
        self.log.info('查询该参数默认值')
        sql_cmd = self.commonsh.execut_db_sql(f'''show cstore_buffers;''')
        self.log.info(sql_cmd)
        self.assertEqual('1GB', sql_cmd.splitlines()[-2].strip())
        self.log.info('gs_guc set设置cstore_buffers')
        msg = self.commonsh.execute_gsguc('set',
                                          self.Constant.GSGUC_SUCCESS_MSG,
                                          'cstore_buffers=30MB')
        self.log.info(msg)
        self.assertTrue(msg)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('查询修改后的值')
        sql_cmd = self.commonsh.execut_db_sql(f'''show cstore_buffers;''')
        self.log.info(sql_cmd)
        self.assertIn('30MB', sql_cmd)
        self.log.info('创建列存表后执行explain')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists t_tbl;
            create table t_tbl(a int, b int) with(orientation='column');
            explain (analyze,buffers) select * from t_tbl;''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd)
        self.assertIn('Buffers: shared hit', sql_cmd)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql('drop table if exists t_tbl;')
        self.log.info(sql_cmd)
        sql_cmd = self.commonsh.execut_db_sql(f'''show cstore_buffers;''')
        self.log.info(sql_cmd)
        if "1GB" != sql_cmd.splitlines()[-2].strip():
            msg = self.commonsh.execute_gsguc('set',
                                              self.Constant.GSGUC_SUCCESS_MSG,
                                              f"cstore_buffers='1GB'")
            self.log.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(
            '-----Opengauss_Function_Guc_Resource_Case0047.py执行完成-----')

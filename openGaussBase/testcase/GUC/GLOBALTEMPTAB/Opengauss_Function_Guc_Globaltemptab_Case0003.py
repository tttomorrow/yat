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
Case Name   : 使用set to方式修改max_active_global_temporary_table为10，观察预期结果
Description :
    1、查询max_active_global_temporary_table默认值
       show max_active_global_temporary_table;
    2、使用set to方式修改max_active_global_temporary_table为10,
      set max_active_global_temporary_table to 10;
      校验其结果，show max_active_global_temporary_table;
    3、创建全局临时表;
    4、恢复默认值;
Expect      :
    1、显示默认值，1000;
    2、参数修改成功，校验参数值为10;
    3、创建全局临时表成功;
    4、恢复默认值成功;
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()


class GucTestCase(unittest.TestCase):
    def setUp(self):
        logger.info("===Opengauss_Function_Guc_Globaltemptab_Case0003开始执行===")
        self.constant = Constant()
        self.comsh = CommonSH('PrimaryDbUser')
        self.table = 'test'
        self.config_param = 'show max_active_global_temporary_table;'
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_guc(self):
        logger.info("====查询max_active_global_temporary_table期望，默认值1000====")
        sql_cmd1 = self.comsh.execut_db_sql(self.config_param)
        logger.info(sql_cmd1)
        self.assertEqual('1000', sql_cmd1.splitlines()[-2].strip())

        logger.info("===修改max_active_global_temporary_table为10，期望：重启设置成功===")
        logger.info("======创建全局临时表======")
        set_cmd = f'''set max_active_global_temporary_table to 10;
            show max_active_global_temporary_table;\
            drop table if exists {self.table};\
            create global temp table {self.table}(c_int int);'''
        set_res = self.comsh.execut_db_sql(set_cmd)
        logger.info(set_res)
        self.assertIn('SET', set_res)
        self.assertIn('10\n', set_res)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, set_res)

    def tearDown(self):
        logger.info("======清理环境，恢复默认值======")
        clear_cmd = self.comsh.execut_db_sql(
            f'''drop table if exists {self.table}''')
        logger.info(clear_cmd)
        sql_cmd = self.comsh.execut_db_sql(self.config_param)
        logger.info(sql_cmd)
        if '1000' not in sql_cmd.splitlines()[-2].strip():
            self.comsh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "max_active_global_temporary_table=1000")
            result = self.comsh.restart_db_cluster()
            logger.info(result)
        status = self.comsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        logger.info("===Opengauss_Function_Guc_Globaltemptab_Case0003执行结束===")

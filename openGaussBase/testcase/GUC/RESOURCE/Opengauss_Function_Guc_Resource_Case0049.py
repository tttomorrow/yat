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
Case Name   : 修改参数bulk_read_ring_size，观察预期结果；
Description :
        1、查询bulk_read_ring_size默认值；
        2、修改bulk_read_ring_size为30mb，重启使其生效，并校验其预期结果；
        3、恢复默认值；
Expect      :
        1、显示默认值；
        2、参数修改成功，校验修改后系统参数值为30MB；
        3、恢复默认值成功；
History     : 
"""
import sys
import unittest

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

class Deletaduit(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-----------Opengauss_Function_Guc_Resource_Case00049.py start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_startdb(self):
        # 查询该参数默认值;
        sql_cmd = self.commonsh.execut_db_sql(f'''show bulk_read_ring_size;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 使用设置gs_guc set设置bulk_read_ring_size
        msg = self.commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'bulk_read_ring_size=30MB')
        self.log.info(msg)
        self.assertTrue(msg)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status)
        # 查询修改后的值;
        sql_cmd = self.commonsh.execut_db_sql(f'''show bulk_read_ring_size;''')
        self.log.info(sql_cmd)
        self.assertIn('30MB', sql_cmd)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''show bulk_read_ring_size;''')
        self.log.info(sql_cmd)
        if self.res not in sql_cmd:
            msg = self.commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG,
                                              f'''bulk_read_ring_size={self.res}''')
            self.log.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status)
        self.log.info( '--------------Opengauss_Function_Guc_Resource_Case0049.py执行完成---------------')

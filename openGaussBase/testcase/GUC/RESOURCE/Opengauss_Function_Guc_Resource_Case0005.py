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
Case Name   : guc参数-资源消耗-修改参数enable_memory_limit，观察预期结果；
Description :
        1、查询enable_memory_limit默认值；
        2、查询视图：
        3、修改enable_memory_limit为off，重启使其生效，并校验其预期结果；
        4、查询视图：
        5、恢复默认值；
Expect      :
        1、显示默认值
        2、视图信息显示正确
        3、重启后参数修改成功，校验修改后系统参数值为off（查看视图会报错）
        4、视图信息显示错误
        5、恢复默认值成功
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
        self.log.info('-----------Opengauss_Function_Guc_Resource_Case0005.py start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_startdb(self):
        # 查询该参数默认值;
        sql_cmd = self.commonsh.execut_db_sql(f'''show enable_memory_limit;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 设置enable_memory_limit为off
        msg = self.commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'enable_memory_limit=off')
        self.log.info(msg)
        self.assertTrue(msg)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        self.assertTrue(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status)
        # 查询视图GS_TOTAL_MEMORY_DETAIL失败
        Sqlmdg = self.commonsh.execut_db_sql('''SELECT * FROM GS_TOTAL_MEMORY_DETAIL;''')
        self.log.info(Sqlmdg)
        self.assertIn('unsupported view for memory protection feature is disabled', Sqlmdg)

    def tearDown(self):
        self.log.info('----------------恢复默认值-----------------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''show enable_memory_limit;''')
        self.log.info(sql_cmd)
        if self.res not in sql_cmd:
            msg = self.commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, f'''enable_memory_limit={self.res}''')
            self.log.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status)
        self.log.info(
            '-----------------------Opengauss_Function_Guc_Resource_Case0005.py执行完成-----------------------------')

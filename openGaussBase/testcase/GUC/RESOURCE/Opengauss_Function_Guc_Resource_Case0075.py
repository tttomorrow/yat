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
Case Name   : 修改enable_adio_debug，观察其预期结果（因当前版本暂不支持开启异步IO功能，目前正向用例只校验默认值与修改方式，预期结果后期补全）；
Description :
        1、查询enable_adio_debug默认值；
           show enable_adio_debug;
        2、修改enable_adio_debug为on，重启使其生效，并校验其预期结果；这个参数不让设置，会强制关闭
           gs_guc set -D /cluster/dn1 -c "enable_adio_debug=on"
           gs_om -t stop && gs_om -t start
           show enable_adio_debug;
        3、恢复默认值；
Expect      :
        1、显示默认值；
        2、参数修改成功，校验修改后系统参数值为on；
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
        self.log.info('-----------Opengauss_Function_Guc_Resource_Case0075.py start------------')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_startdb(self):
        # 查询该参数默认值;
        sql_cmd = self.commonsh.execut_db_sql(f'''show enable_adio_debug;''')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        # 使用设置gs_guc set设置enable_adio_debug
        msg = self.commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG, 'enable_adio_debug=on')
        self.log.info(msg)
        self.assertTrue(msg)
        msg = self.commonsh.restart_db_cluster()
        self.log.info(msg)
        self.assertTrue(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status)
        sql_cmd = self.commonsh.execut_db_sql(f'''show enable_adio_debug;''')
        self.log.info(sql_cmd)
        # 这个参数不让设置，会强制关闭
        self.assertIn('off', sql_cmd)

    def tearDown(self):
        self.log.info('----------------恢复默认值----------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''show enable_adio_debug;''')
        self.log.info(sql_cmd)
        if self.res not in sql_cmd:
            msg = self.commonsh.execute_gsguc('set', self.Constant.GSGUC_SUCCESS_MSG,
                                              f'''show enable_adio_debug={self.res}''')
            self.log.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.log.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Normal" in status)
        self.log.info('--------------Opengauss_Function_Guc_Resource_Case0075.py执行完成---------------')

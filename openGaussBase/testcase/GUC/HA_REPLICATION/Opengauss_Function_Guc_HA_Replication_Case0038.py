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
Case Name   : 使用gs_guc set方法设置参数hot_standby为无效值,合理报错
Description :
        1.查询hot_standby默认值
        2.修改参数值为字符test
        3.修改参数值为空串
        4.修改参数值为1234
        5.恢复参数默认值
Expect      :
        1.显示默认值为on
        2.合理报错
        3.合理报错
        4.合理报错
        5.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

constant = Constant()


class HAReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '--Opengauss_Function_Guc_HA_Replication_Case0038start----')
        self.commonsh = CommonSH('PrimaryDbUser')

    def test_hot_standby(self):
        self.log.info('--步骤1:查看默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show hot_standby;')
        self.log.info(sql_cmd)
        self.assertIn(constant.BOOLEAN_VALUES[0], sql_cmd)
        self.log.info('--步骤2:修改参数值为test, "''", 1234--')
        invalid_value = ['test', "''", 10001, 125.255, -2]
        for i in invalid_value:
            result = self.commonsh.execute_gsguc("set",
                                                 constant.GSGUC_SUCCESS_MSG,
                                                 f" hot_standby"
                                                 f"={i}")
            self.assertFalse(result)

    def tearDown(self):
        self.log.info('--步骤3:恢复默认值--')
        sql_cmd = self.commonsh.execut_db_sql('show hot_standby;')
        self.log.info(sql_cmd)
        if "on" != sql_cmd.split('\n')[-2].strip():
            mod_msg = self.commonsh.execute_gsguc('set',
                                                  constant.GSGUC_SUCCESS_MSG,
                                                  'hot_standby=on')
            self.log.info(mod_msg)
            restart_msg = self.commonsh.restart_db_cluster()
            self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.commonsh.execut_db_sql('show hot_standby;')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_Guc_HA_Replication_Case0038执行完成-----')

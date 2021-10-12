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
Case Name   : 使用gs_guc set方法设置参数trace_notify为无效值,合理报错
Description :
        1.查询trace_notify默认值
        2.修改参数值为test
        3.修改参数值为123546
        4.修改参数值为null
        5.修改参数值为空串
        6.恢复参数默认值
Expect      :
        1.显示默认值为off
        2.合理报错
        3.合理报错
        4.合理报错
        5.合理报错
        6.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class DeveloperOption(unittest.TestCase):
    def setUp(self):
        LOG.info(
            '-----Opengauss_Function_DeveloperOptions_Case0035start------')
        self.constant = Constant()

    def test_trace_notify(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show trace_notify;''')
        LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd)
        LOG.info('--步骤2:修改参数值为test，123456, null,空串合理报错--')
        invalid_value = ['test', 123456, 'null', "''"]
        for i in invalid_value:
            result = commonsh.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"trace_notify={i}")
            self.assertFalse(result)

    def tearDown(self):
        LOG.info('--步骤3:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('''show trace_notify;''')
        LOG.info(sql_cmd)
        if "off" != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         '''trace_notify=off''')
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show trace_notify;''')
        LOG.info(sql_cmd)
        LOG.info(
            '------Opengauss_Function_DeveloperOptions_Case0035执行完成----')

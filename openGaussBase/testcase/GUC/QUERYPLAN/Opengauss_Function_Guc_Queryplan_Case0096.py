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
Case Name   : 使用gs_guc set方法设置参数codegen_cost_threshold为无效值,合理报错
Description :
        1.查询codegen_cost_threshold默认值
        2.1修改参数值为字符test
        2.2修改参数值为超临界值-1
        2.3修改参数值为空串
        2.4.修改参数值为小数500.985
        3.恢复参数默认值
Expect      :
        1.显示默认值为10000
        2.1-2.5：合理报错
        3.默认值恢复成功
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

LOG = Logger()
commonsh = CommonSH('dbuser')


class QueryPlan(unittest.TestCase):

    def setUp(self):
        self.constant = Constant()
        LOG.info(
            '-------Opengauss_Function_Guc_Queryplan_Case0096start------')

    def test_codegen_cost_threshold(self):
        LOG.info('--步骤1:查看默认值--')
        sql_cmd = commonsh.execut_db_sql('''show codegen_cost_threshold;''')
        LOG.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        for i in invalid_value:
            result = commonsh.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"codegen_cost_threshold={i}")
            self.assertFalse(result)

    def tearDown(self):
        LOG.info('--步骤3:恢复默认值--')
        sql_cmd = commonsh.execut_db_sql('''show codegen_cost_threshold;''')
        LOG.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[-2].strip():
            msg = commonsh.execute_gsguc('set',
                                         self.constant.GSGUC_SUCCESS_MSG,
                                         f"codegen_cost_threshold={self.res}")
            LOG.info(msg)
            msg = commonsh.restart_db_cluster()
            LOG.info(msg)
        status = commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = commonsh.execut_db_sql('''show codegen_cost_threshold;''')
        LOG.info(sql_cmd)
        LOG.info(
            '-----Opengauss_Function_Guc_Queryplan_Case0096执行完成-------')

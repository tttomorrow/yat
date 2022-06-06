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
Case Name   : 使用gs_guc set方法设置参数enable_codegen为无效值,合理报错
Description :
        1.查询enable_codegen默认值
        2.依次修改参数值为test,12345,空串
        3.恢复参数默认值
Expect      :
        1.显示默认值为on
        2.合理报错
        3.默认值恢复成功
"""
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class QueryPlan(unittest.TestCase):

    def setUp(self):
        self.LOG = Logger()
        self.pri = CommonSH('dbuser')
        self.constant = Constant()
        self.common = Common()
        self.LOG.info('-Opengauss_Function_Guc_Queryplan_Case0090 start-')

    def test_enable_codegen(self):
        text = '--step1:查看默认值;expect:默认值是on--'
        self.LOG.info(text)
        sql_cmd = self.pri.execut_db_sql("show enable_codegen;")
        self.LOG.info(sql_cmd)
        self.common.equal_sql_mdg(sql_cmd, "enable_codegen", "on",
                                  "(1 row)", flag="1")
        text = '--step2:依次修改参数值为test,12345,"''";expect:修改失败--'
        self.LOG.info(text)
        invalid_value = ['test', 12345, "''"]
        for i in invalid_value:
            result = self.pri.execute_gsguc("set",
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"enable_codegen={i}")
            self.assertFalse(result, '执行失败:' + text)

    def tearDown(self):
        text = 'step3:恢复默认值;expect:恢复默认值成功--'
        self.LOG.info(text)
        msg = self.pri.execute_gsguc("set",
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     "enable_codegen=on")
        self.LOG.info(msg)
        msg = self.pri.restart_db_cluster()
        self.LOG.info(msg)
        status = self.pri.get_db_cluster_status()
        self.LOG.info(status)
        sql_cmd = self.pri.execut_db_sql("show enable_codegen;")
        self.LOG.info(sql_cmd)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.common.equal_sql_mdg(sql_cmd, "enable_codegen", "on",
                                  "(1 row)", flag="1")
        self.LOG.info('-Opengauss_Function_Guc_Queryplan_Case0090 finish-')

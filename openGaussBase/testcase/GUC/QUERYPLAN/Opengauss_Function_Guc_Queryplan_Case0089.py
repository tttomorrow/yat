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
Case Name   : 使用gs_guc set方法设置参数enable_codegen为off,观察预期结果
Description :
        1.查询enable_codegen默认值
        2.gs_guc set设置enable_codegen为off并重启数据库
        3.查询该参数修改后的值
        4.恢复参数默认值
Expect      :
        1.默认值为on
        2.设置成功；重启成功
        3.修改为off成功
        4.参数值恢复成功
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class QueryPlan(unittest.TestCase):

    def setUp(self):
        self.LOG = Logger()
        self.commonsh = CommonSH('dbuser')
        self.constant = Constant()
        self.LOG.info(
            '------Opengauss_Function_Guc_Queryplan_Case0089 start------')

    def test_enable_codegen(self):
        text = '--step1:查看默认值;expect:默认值为on--'
        self.LOG.info(text)
        sql_cmd = self.commonsh.execut_db_sql('show enable_codegen;')
        self.LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd,
                      '执行失败:' + text)

        text = '--step2:gs_guc set设置enable_codegen为off并重启数据库;' \
               'expect:设置成功；重启成功--'
        self.LOG.info(text)
        msg = self.commonsh.execute_gsguc('set',
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          'enable_codegen =off')
        self.LOG.info(msg)
        self.assertTrue(msg)
        msg = self.commonsh.restart_db_cluster()
        self.LOG.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step3:查询该参数修改后的值;expect:修改为off成功--'
        self.LOG.info(text)
        sql_cmd = self.commonsh.execut_db_sql('show enable_codegen;')
        self.LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[1], sql_cmd,
                      '执行失败:' + text)

    def tearDown(self):
        text = '--step4:恢复默认值;expect:参数值恢复成功--'
        self.LOG.info(text)
        sql_cmd = self.commonsh.execut_db_sql('show enable_codegen;')
        self.LOG.info(sql_cmd)
        if "on" != sql_cmd.split('\n')[-2].strip():
            msg = self.commonsh.execute_gsguc('set',
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              "enable_codegen=on")
            self.LOG.info(msg)
            msg = self.commonsh.restart_db_cluster()
            self.LOG.info(msg)
        status = self.commonsh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        sql_cmd = self.commonsh.execut_db_sql('show enable_codegen;')
        self.LOG.info(sql_cmd)
        self.assertIn(self.constant.BOOLEAN_VALUES[0], sql_cmd,
                      '执行失败:' + text)
        self.LOG.info(
            '-----Opengauss_Function_Guc_Queryplan_Case0089 finish------')

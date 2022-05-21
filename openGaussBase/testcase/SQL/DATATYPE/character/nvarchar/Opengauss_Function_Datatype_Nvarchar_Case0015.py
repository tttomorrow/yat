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
Case Type   : SQL-DATETYPE-NVARCHAR
Case Name   : mot表不支持nvarchar类型
Description :
    1.修改参数并重启，允许创建mot表
    gs_guc reload -D dn1 -c "enable_incremental_checkpoint=off"
    2.创建mot表指定nvarchar类型
    3.删除表，恢复参数
Expect      :
    1.修改并重启成功
    2.创建失败 合理报错
    3.恢复成功
History     :
"""

import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Guctestcase(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info("==Opengauss_Function_Datatype_Nvarchar_Case0015 "
                      "start==")
        self.constant = Constant()
        self.primary_sh = CommonSH("PrimaryDbUser")
        self.common = Common()
        status = self.primary_sh.get_db_cluster_status("detail")
        self.log.info(status)
        self.assertTrue("Normal" in status or "Degraded" in status)

        self.param = "enable_incremental_checkpoint"
        self.value = self.common.show_param(self.param)
        self.log.info(self.value)

    def test_lock_level(self):
        text = "--step1:修改参数并重启; expect:成功"
        self.log.info(text)
        self.primary_sh.execute_gsguc('reload',
                                      self.constant.GSGUC_SUCCESS_MSG,
                                      f"{self.param}=off")
        self.primary_sh.restart_db_cluster()
        status = self.primary_sh.restart_db_cluster()
        self.log.info(status)
        result = self.primary_sh.execut_db_sql(f"show {self.param}")
        self.log.info(result)
        self.assertNotIn("on", result, "执行失败:" + text)
        self.assertIn("off", result, "执行失败:" + text)

        text = "--step2:创建mot表指定nvarchar类型; expect:失败"
        self.log.info(text)
        sql = "create foreign table t_nvarchar_0015(c_nvarchar nvarchar);"
        self.log.info(sql)
        result = self.primary_sh.execut_db_sql(sql)
        self.log.info(result)
        self.assertNotIn(self.constant.TABLE_CREATE_SUCCESS, result,
                         "执行失败:" + text)
        self.assertIn(self.constant.NOT_SUPPORTED_TYPE, result)

    def tearDown(self):
        text = "--step3:清理环境恢复参数; expect:成功"
        self.log.info(text)
        self.primary_sh.execute_gsguc('reload',
                                      self.constant.GSGUC_SUCCESS_MSG,
                                      f"{self.param}={self.value}")
        status = self.primary_sh.restart_db_cluster()
        self.log.info(status)
        result = self.common.show_param(self.param)
        self.log.info(result)
        status = self.primary_sh.get_db_cluster_status("detail")
        self.log.info(status)
        self.assertEqual(self.value, result)
        self.assertTrue("Normal" in status or "Degraded" in status)
        self.log.info("==Opengauss_Function_Datatype_Nvarchar_Case0015 "
                      "finish=")

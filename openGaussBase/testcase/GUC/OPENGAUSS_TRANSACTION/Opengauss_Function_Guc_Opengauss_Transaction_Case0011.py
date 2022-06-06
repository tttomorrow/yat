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
Case Name   : 修改参数transaction_deferrable,观察预期结果
Description :
        1.查询transaction_deferrable默认值
        2.修改transaction_deferrable为on
        3.查询修改后参数值
        4.清理环境
Expect      :
        1.显示默认值为off
        2.修改成功
        3.该参数为预留参数，该版本不生效，参数值仍是off
        4.清理环境完成
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_Opengauss_Transaction _Case0011start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')

    def test_dynamic_library_path(self):
        text = '---step1:查询默认值;expect:默认值off---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql("show transaction_deferrable;")
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()

        text = '--step2:修改transaction_deferrable为on;expect:修改成功--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"transaction_deferrable=on")
        self.assertTrue(result, '执行失败:' + text)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status
                        , '执行失败:' + text)

        text = '---step3:查询修改后的参数值;expect:参数值不变---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql("show transaction_deferrable;")
        self.log.info(sql_cmd)
        self.assertIn(self.res, sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step4:清理环境;expect:清理环境完成--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"transaction_deferrable=off")
        self.assertTrue(result, '执行失败:' + text)
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status('detail')
        self.log.info(status)
        self.assertTrue("Degraded" in status or "Normal" in status
                        , '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_Opengauss_Transaction _Case0011finish-')

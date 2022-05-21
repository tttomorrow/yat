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
Case Name   : 修改参数dynamic_library_path,观察预期结果
Description :
        1.查询dynamic_library_path默认值
        2.修改dynamic_library_path为空值
        3.恢复参数默认值
Expect      :
        1.显示默认值为$libdir
        2.修改成功
        3.恢复成功
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_ClientConnection_Case0255start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.pg_file = os.path.join(macro.DB_INSTANCE_PATH,
                                    macro.DB_PG_CONFIG_NAME)

    def test_dynamic_library_path(self):
        text = '---step1:查询默认值;expect:默认值$libdir---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql("show dynamic_library_path;")
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()
        text = '--step2:修改dynamic_library_path为空值;expect:重启失败--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"dynamic_library_path=''",
                                           single=True)
        self.assertTrue(result, '执行失败:' + text)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        self.assertFalse(msg, '执行失败:' + text)
        text = '---step3:恢复参数默认值;expect:恢复成功---'
        self.log.info(text)
        clear_cmd = f'''sed -i  "s/dynamic_library_path = ''/\
                   dynamic_library_path = \'\$libdir\'/g" {self.pg_file }'''
        self.log.info(clear_cmd)
        msg = self.user_node.sh(clear_cmd).result()
        self.log.info(msg)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        sql_cmd = self.pri_sh.execut_db_sql("show dynamic_library_path;")
        self.log.info(sql_cmd)
        self.assertIn(self.res, sql_cmd, '执行失败:' + text)

    def tearDown(self):
        self.log.info(
            '-Opengauss_Function_Guc_ClientConnection_Case0255finish-')

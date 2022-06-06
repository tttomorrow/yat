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
Case Name   : gs_guc set修改参数unix_socket_permissions为非法权限，合理报错
Description :
        1.查询unix_socket_permissions默认值
        2.修改参数值为0800
        3.清理环境
Expect      :
        1.显示默认值为0700
        2.合理报错
        3.清理环境完成
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0309start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')

    def test_unix_socket_permissions(self):
        text = '---step1:查询默认值;expect:默认值0700---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show unix_socket_permissions;')
        self.log.info(sql_cmd)
        self.res = sql_cmd.splitlines()[-2].strip()

        text = '--step2:修改参数值为0800;expect:合理报错--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"unix_socket_permissions=0800")
        self.assertFalse(result)

    def tearDown(self):
        text = '---步骤3:清理环境;expect:清理环境完成---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show unix_socket_permissions;')
        self.log.info(sql_cmd)
        if self.res != sql_cmd.split('\n')[2].strip():
            msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f'unix_socket_permissions'
                                            f'={self.res}')
            self.log.info(msg)
            msg = self.pri_sh.restart_db_cluster()
            self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(
            '-Opengauss_Function_Guc_Connectionauthentication_Case0309finish-')

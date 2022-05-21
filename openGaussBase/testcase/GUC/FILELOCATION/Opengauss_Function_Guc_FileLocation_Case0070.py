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
Case Name   : 使用gs_guc set方法设置参数config_file值为数字，合理报错
Description :
        1.查询config_file默认值
        2.修改参数值为123
        3.清理环境
Expect      :
        1.postgresql.conf(实际安装可能带有绝对目录)
        2.合理报错
        3.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0070start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.pg_file = os.path.join(macro.DB_INSTANCE_PATH,
                                    macro.DB_PG_CONFIG_NAME)

    def test_config_file(self):
        text = '---step1:查询默认值;expect:默认值是postgresql.conf---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show config_file;')
        self.log.info(sql_cmd)
        self.assertEqual(self.pg_file, sql_cmd.splitlines()[-2].strip(),
                         '执行失败:' + text)

        text = '--step2:修改参数值为123;expect:合理报错--'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"config_file=12345")
        self.assertFalse(result, '执行失败:' + text)

    def tearDown(self):
        text = '---step3:清理环境;expect:清理环境完成---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show config_file;')
        self.log.info(sql_cmd)
        if f"{self.pg_file}" != sql_cmd.split('\n')[2].strip():
            msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f"config_file='{self.pg_file}'")
            self.log.info(msg)
            msg = self.pri_sh.restart_db_cluster()
            self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0070finish-')

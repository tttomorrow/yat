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
Case Name   : ident_file参数使用gs_guc set设置为不存在目录
Description :
        1.查询ident_file默认值
        2.使用gs_guc set设置ident_file为不存在的目录并重启
        3.查询参数修改后的值
        4.清理环境
Expect      :
        1.默认值为pg_ident.conf(实际安装可能带有绝对目录)
        2.修改成功；重启成功
        3.参数值修改成功
        4.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class FilePosition(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0037start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.pg_file = os.path.join(macro.DB_INSTANCE_PATH, 'pg_ident.conf')

    def test_guc(self):
        text = '---step1:查询默认值;expect:默认值是pg_ident.conf---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show ident_file;')
        self.log.info(sql_cmd)
        self.assertEqual(self.pg_file, sql_cmd.splitlines()[-2].strip(),
                         '执行失败:' + text)

        text = '---step2:使用gs_guc set设置ident_file为不存在的' \
               '路径并重启;expect:设置成功'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"ident_file="
                                           f"'{macro.DB_INSTANCE_PATH}"
                                           f"/test/pg_ident.conf'")
        self.log.info(result)
        self.assertTrue(result, '执行失败:' + text)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '---step3:查询修改后的参数值;expect:修改成功---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show ident_file;')
        self.log.info(sql_cmd)
        self.assertIn(f'{macro.DB_INSTANCE_PATH}/test/pg_ident.conf', sql_cmd,
                      '执行失败:' + text)

    def tearDown(self):
        text = '---step4:清理环境;expect:清理环境完成---'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"ident_file='{self.pg_file}'")
        self.log.info(result)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0037finish-')

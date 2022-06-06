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
Case Name   : 使用ALTER SYSTEM SET修改数据库参数hba_file为不存在目录
Description :
        1.查询hba_file默认值
        2.在gsql中设置数据库级别hba_file为不存在路径并重启
        3.恢复参数默认值
Expect      :
        1.默认值为pg_hba.conf(实际安装可能带有绝对目录)
        2.重启失败
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


class FilePosition(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0023start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, 'cluster', 'dn1')
        self.pg_file = os.path.join(macro.DB_INSTANCE_PATH,
                                    macro.PG_HBA_FILE_NAME)

    def test_guc(self):
        text = '---step1:查询默认值;expect:默认值pg_hba.conf---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show hba_file;')
        self.log.info(sql_cmd)
        self.assertEqual(self.pg_file, sql_cmd.splitlines()[-2].strip(),
                         '执行失败:' + text)

        text = '---step2:在gsql中设置数据库级别hba_file为不存在路径并重启;' \
               'expect:重启失败---'
        sql_cmd = self.pri_sh.execut_db_sql(f"alter system  set "
                                            f"hba_file to "
                                            f"'{macro.DB_INSTANCE_PATH}"
                                            f"/test/pg_hba.conf'")
        self.log.info(sql_cmd)
        self.assertIn('ALTER SYSTEM SET', sql_cmd, '执行失败:' + text)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertFalse("Degraded" in status or "Normal" in status,
                         '执行失败:' + text)

    def tearDown(self):
        text = '---step3:恢复参数值并查询;expect:恢复成功---'
        self.log.info(text)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"hba_file='{self.pg_file}'")
        self.log.info(result)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        sql_cmd = self.pri_sh.execut_db_sql('show hba_file;')
        self.log.info(sql_cmd)
        self.assertIn(self.pg_file, sql_cmd.splitlines()[-2].strip(),
                      '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0023finish-')

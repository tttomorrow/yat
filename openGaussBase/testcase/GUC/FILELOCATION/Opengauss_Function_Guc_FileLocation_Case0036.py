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
Case Name   : 使用ALTER SYSTEM SET修改数据库参数ident_file
Description :
        1.查询ident_file默认值
        2.创建测试文件
        3.使用ALTER SYSTEM SET修改数据库参数ident_file并重启数据库
        4.查询修改后的参数值
        5.清理环境
Expect      :
        1.默认值为pg_ident.conf(实际安装可能带有绝对目录)
        2.创建成功
        3.设置成功
        4.修改成功
        5.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class FilePositionC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0036start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, 'cluster', 'dn1')
        self.pg_file = os.path.join(macro.DB_INSTANCE_PATH, 'pg_ident.conf')

    def test_guc(self):
        text = '---step1:查询默认值;expect:默认值pg_ident.conf---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show ident_file;')
        self.log.info(sql_cmd)
        self.assertEqual(self.pg_file, sql_cmd.splitlines()[-2].strip(),
                         '执行失败:' + text)

        text = '---step2:创建测试文件夹,将pg_ident.conf文件拷贝至测试目录;' \
               'expect:创建成功，复制成功---'
        self.log.info(text)
        touch_cmd = f'''mkdir -p {self.file_path};
            cp -rf {self.pg_file}  {self.file_path} '''
        self.log.info(touch_cmd)
        msg = self.user_node.sh(touch_cmd).result()
        self.log.info(msg)
        self.assertEqual(msg, '', '执行失败:' + text)

        text = '---step3:在gsql中设置数据库级别ident_file;' \
               'expect:设置成功---'
        sql_cmd = self.pri_sh.execut_db_sql(f"alter system  set "
                                            f"ident_file to "
                                            f"'{self.file_path}"
                                            f"/pg_ident.conf'")
        self.log.info(sql_cmd)
        self.assertIn('ALTER SYSTEM SET', sql_cmd, '执行失败:' + text)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '---step4:查询修改后的参数值;expect:修改成功---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql('show ident_file;')
        self.log.info(sql_cmd)
        self.assertEqual(f"{self.file_path}/pg_ident.conf",
                         sql_cmd.splitlines()[-2].strip(),
                         '执行失败:' + text)

    def tearDown(self):
        text = '---step5:清理环境;expect:清理环境完成---'
        self.log.info(text)
        rm_cmd = f'''rm -rf {macro.DB_BACKUP_PATH}/cluster;'''
        self.log.info(rm_cmd)
        msg = self.user_node.sh(rm_cmd).result()
        self.log.info(msg)
        result = self.pri_sh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"ident_file='{self.pg_file}'")
        self.log.info(result)
        msg = self.pri_sh.restart_db_cluster()
        self.log.info(msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        sql_cmd = self.pri_sh.execut_db_sql('show ident_file;')
        self.log.info(sql_cmd)
        self.assertEqual(self.pg_file, sql_cmd.splitlines()[-2].strip(),
                         '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0036finish-')

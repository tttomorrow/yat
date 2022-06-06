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
Case Name   : 修改指定数据库，用户，会话级别的参数data_directory
Description :
        1.查询data_directory默认值
        2.创建测试文件
        3.在gsql中设置数据库级别data_directory
        4.在gsql中设置用户级别data_directory
        5.在gsql中设置会话级别data_directorys
        6.清理环境
Expect      :
        1.安装时指定，如果在安装时不指定，则默认不初始化数据库
        2.创建成功
        3.合理报错
        4.合理报错
        5.合理报错(POSTMASTER型参数无法使用方式四设置)
        6.清理环境完成
             拷贝dn1目录失败
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0003 start-')
        self.constant = Constant()
        self.com = Common()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.file_path = os.path.join(macro.DB_BACKUP_PATH, 'cluster')
        self.new_dn1 = os.path.join(self.file_path, 'dn1')

    def test_data_directory(self):
        text = '---step1:查询默认值;expect:安装时指定---'
        self.log.info(text)
        sql_cmd = self.com.show_param("data_directory")
        self.assertTrue(macro.DB_INSTANCE_PATH in sql_cmd, '执行失败:' + text)

        text = '---step2:创建测试目录;expect:创建成功，复制成功---'
        self.log.info(text)
        touch_cmd = f'''mkdir -p {self.file_path};'''
        self.log.info(touch_cmd)
        msg = self.user_node.sh(touch_cmd).result()
        self.log.info(msg)
        self.assertEqual(msg, '', '执行失败:' + text)

        text = '---step3:在gsql中设置数据库级别data_directory;' \
               'expect:合理报错---'
        sql_cmd = self.pri_sh.execut_db_sql(f"alter database postgres  set "
                                            f"data_directory to "
                                            f"'{self.new_dn1}';")
        self.log.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd, '执行失败:' + text)

        text = '---step4:在gsql中设置用户级别data_directory;' \
               'expect:合理报错--'
        sql_cmd = self.pri_sh.execut_db_sql(f"alter user "
                                            f"{self.user_node.ssh_user} set "
                                            f"data_directory to "
                                            f"'{self.new_dn1}';")
        self.log.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd, '执行失败:' + text)

        text = '---step5:在gsql中设置会话级别data_directory;' \
               'expect:合理报错--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f"set data_directory to "
                                            f"'{self.new_dn1}';")
        self.log.info(sql_cmd)
        self.assertIn('ERROR', sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '---step6:清理环境;expect:清理环境完成---'
        self.log.info(text)
        rm_cmd = f'''rm -rf {self.file_path}'''
        self.log.info(rm_cmd)
        msg = self.user_node.sh(rm_cmd).result()
        self.log.info(msg)
        self.assertEqual(msg, '', '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0003 finish-')

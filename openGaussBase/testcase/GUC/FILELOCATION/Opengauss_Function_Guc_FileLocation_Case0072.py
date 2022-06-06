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
Case Name   : 修改data_directory目录权限
Description :
        1.修改data_directory目录权限为600
        2.连接数据库执行查询操作
        3.恢复data_directory目录权限700
        4.连接数据库执行查询操作
Expect      :
        1.修改成功
        2.连接失败
        3.恢复成功
        4.查询成功
History     :
"""
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
            '-Opengauss_Function_Guc_FileLocation_Case0072start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')

    def test_data_directory(self):
        text = '--step1:修改data_directory目录权限为600;expect:修改成功--'
        self.log.info(text)
        chmod_cmd = f'''chmod 600 {macro.DB_INSTANCE_PATH}'''
        self.log.info(chmod_cmd)
        msg = self.user_node.sh(chmod_cmd).result()
        self.log.info(msg)

        text = '--step2:连接数据库执行查询操作;expect:连接失败--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''show data_directory;''')
        self.log.info(sql_cmd)
        self.assertIn('failed to connect', sql_cmd, '执行失败:' + text)

        text = '--step3:恢复data_directory目录权限700;expect:恢复成功--'
        self.log.info(text)
        chmod_cmd = f'''chmod 700 {macro.DB_INSTANCE_PATH}'''
        self.log.info(chmod_cmd)
        msg = self.user_node.sh(chmod_cmd).result()
        self.log.info(msg)

        text = '--step4:连接数据库执行查询操作;expect:连接成功--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''show data_directory;''')
        self.log.info(sql_cmd)
        self.assertIn(f"{macro.DB_INSTANCE_PATH}", sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '---step5:无须清理环境---'
        self.log.info(text)
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0072finish-')

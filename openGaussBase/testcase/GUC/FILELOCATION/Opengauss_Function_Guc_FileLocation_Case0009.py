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
Case Name   : 普通用户查询data_directory参数
Description :
        1.创建普通用户
        2.普通用户查询data_directory参数
        3.清理环境
Expect      :
        1.创建成功
        2.合理报错ERROR:  must be superuser to examine "data_directory"
        3.清理环境完成
History     :
"""
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
            '-Opengauss_Function_Guc_FileLocation_Case0009 start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.user_node = Node('PrimaryDbUser')
        self.us_name = "u_guc_filelocation_case0009"

    def test_guc(self):
        text = '---step1:创建普通用户;expect:创建成功---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f"drop user if exists "
                                            f"{self.us_name};"
                                            f"create user {self.us_name} "
                                            f"password "
                                            f"'{macro.COMMON_PASSWD}';")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = '---step2:普通用户查询data_directory参数;expect:合理报错---'
        self.log.info(text)
        sql_cmd = "show data_directory;"
        sql_cmd = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                            sql_type=f'-U {self.us_name} '
                                                     f'-W '
                                                     f'{macro.COMMON_PASSWD}')
        self.log.info(sql_cmd)
        self.assertIn('ERROR:  must be superuser to examine "data_directory"',
                      sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '---step3:清理环境;expect:清理环境完成---'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f"drop user if exists "
                                            f"{self.us_name};")
        self.log.info(sql_cmd)
        self.assertIn('DROP ROLE', sql_cmd, '执行失败:' + text)
        self.log.info(
            '-Opengauss_Function_Guc_FileLocation_Case0009 finish-')

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
Case Type   : DDL_Create_Directory
Case Name   : enable_access_server_directory=off，赋予gs_role_directory_create
             权限的普通用户创建directory
Description :
    1.创建目录
    2.查询参数enable_access_server_directory=off
    3.创建普通用户并赋予gs_role_directory_create权限
    4.赋予gs_role_directory_create权限的用户创建directory
    5.通过系统表查看目录信息
    6.删除目录，删除用户
Expect      :
    1.创建目录成功
    2.参数的值为off
    3.创建用户成功，赋予权限成功
    4.创建失败，合理报错
    5.无目录信息
    6.删除成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common


class CreateDirectory(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f"-----{os.path.basename(__file__)} start-----")
        self.userNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.user_name = 'u_create_directory_0010'
        self.dir_name = 'dir_object_create_directory_0010'
        self.dir_path = os.path.join('/tmp', 'dir_create_directory_0010')

        text = '-----step1:创建目录,expect:创建目录成功-----'
        self.logger.info(text)
        mkdir_cmd = f"mkdir {self.dir_path}"
        self.userNode.sh(mkdir_cmd).result()
        check_dir_cmd = f'''if [ -d {self.dir_path} ]; 
                    then echo "exists"; 
                    else echo "not exists"; fi'''
        mkdir_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(mkdir_result)
        self.assertEquals("exists", mkdir_result, '执行失败' + text)

        text = '-----step2:查询参数enable_access_server_directory=off' \
               'expect:参数的值为off-----'
        self.logger.info(text)
        self.config_directory = 'enable_access_server_directory'
        show_msg = self.common.show_param(self.config_directory)
        self.assertEquals(show_msg, 'off', '执行失败' + text)

    def test_create_directory(self):
        text = "-----step3:创建普通用户并赋予gs_role_directory_create权限;" \
               "expect:创建成功,赋予权限成功-----"
        self.logger.info(text)
        create_cmd = f"drop user if exists {self.user_name};" \
            f"create user {self.user_name} with " \
            f"password '{macro.COMMON_PASSWD}';" \
            f"grant gs_role_directory_create to {self.user_name};"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG and
                      self.constant.CREATE_ROLE_SUCCESS_MSG and
                      self.constant.GRANT_SUCCESS_MSG,
                      create_msg, '执行失败' + text)

        text = "-----step4:赋予gs_role_directory_create权限的用户创建directory;" \
               "expect:创建失败，合理报错-----"
        self.logger.info(text)
        create_cmd = f"create or replace directory {self.dir_name} " \
            f"as '{self.dir_path}';"
        create_msg = self.sh_primary.execut_db_sql(
            create_cmd, f'-U {self.user_name} -W {macro.COMMON_PASSWD}')
        self.logger.info(create_msg)
        self.assertIn(self.constant.PERMISSION_DENIED and
                      "must be initial user to create a directory",
                      create_msg, '执行失败' + text)

        text = "-----step5:通过系统表查看目录信息，expect:无目录信息-----"
        self.logger.info(text)
        sql_cmd = f"select oid,dirname,owner,dirpath,diracl from pg_directory;"
        sql_msg = self.sh_primary.execut_db_sql(sql_cmd)
        self.logger.info(sql_msg)
        self.assertIn("(0 rows)", sql_msg, '执行失败' + text)

    def tearDown(self):
        text = "-----step6:删除用户，删除目录;expect:删除成功-----"
        self.logger.info(text)
        drop_user = f"drop user {self.user_name};"
        drop_msg = self.sh_primary.execut_db_sql(drop_user)
        self.logger.info(drop_msg)
        del_cmd = f"rm -rf {self.dir_path}"
        self.userNode.sh(del_cmd).result()
        check_dir_cmd = f'''if [ -d {self.dir_path} ]; 
                            then echo "exists"; 
                            else echo "not exists"; fi'''
        del_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(del_result)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG,
                      drop_msg, '执行失败' + text)
        self.assertEquals("not exists", del_result, '执行失败' + text)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
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
Case Type   : DDL_Alter_Directory
Case Name   : enable_access_server_directory=on时，无sysadmin权限的用户修改属主
Description :
    1.创建目录,修改guc参数enable_access_server_directory=on
    2.初始用户创建目录对象，创建用户
    3.无sysadmin权限的用户将属主修改为自己
    4.无sysadmin权限的用户将属主修改为其它sysadmin用户
    5.无sysadmin权限的用户将属主修改为其它普通用户
    6.删除目录，删除用户
    7.恢复参数
Expect      :
    1.创建目录成功,修改参数成功
    2.创建成功
    3.修改失败，合理报错
    4.修改失败，合理报错
    5.修改失败，合理报错
    6.删除成功
    7.恢复参数成功
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


class AlterDirectory(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f"-----{os.path.basename(__file__)} start-----")
        self.userNode = Node('PrimaryDbUser')
        self.sh_primary = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.user_name_1 = 'u_alter_directory_0007_01'
        self.user_name_2 = 'u_alter_directory_0007_02'
        self.user_name_3 = 'u_alter_directory_0007_03'
        self.dir_name = 'dir_alter_directory_0007'
        self.dir_path = os.path.join('/tmp', 'dir_alter_directory_0007')
        self.config_directory = 'enable_access_server_directory'
        self.check_default = self.common.show_param(self.config_directory)
        self.guc_result = ''

    def test_alter_directory(self):
        text = '-----step1:创建目录,修改guc参数enable_access_server_directory=on;' \
               'expect:创建目录成功,修改参数成功-----'
        self.logger.info(text)
        mkdir_cmd = f"mkdir {self.dir_path} && ls -ld {self.dir_path}"
        self.logger.info(mkdir_cmd)
        mkdir_msg = self.userNode.sh(mkdir_cmd).result()
        self.logger.info(mkdir_msg)
        check_dir_cmd = f'''if [ -d {self.dir_path} ]; 
                            then echo "exists"; 
                            else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        mkdir_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(mkdir_result)
        self.assertEquals("exists", mkdir_result, '执行失败' + text)

        if 'on' != self.check_default:
            result = self.sh_primary.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                f'{self.config_directory}=on')
            self.assertTrue(result, '执行失败' + text)
        show_msg = self.common.show_param(self.config_directory)
        self.assertEquals(show_msg, 'on', '执行失败' + text)

        text = "-----step2:初始用户创建目录对象，创建用户; expect:创建成功-----"
        self.logger.info(text)
        create_cmd = f"create or replace directory {self.dir_name} " \
            f"as '{self.dir_path}';" \
            f"drop user if exists {self.user_name_1},{self.user_name_2}," \
            f"{self.user_name_3};" \
            f"create user {self.user_name_1} with " \
            f"password '{macro.COMMON_PASSWD}';" \
            f"create user {self.user_name_2} sysadmin " \
            f"password '{macro.COMMON_PASSWD}';" \
            f"create user {self.user_name_3} with " \
            f"password '{macro.COMMON_PASSWD}';"
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG and
                      self.constant.DROP_ROLE_SUCCESS_MSG,
                      create_msg, '执行失败' + text)
        self.assertEquals(3, create_msg.count(
            self.constant.CREATE_ROLE_SUCCESS_MSG), '执行失败' + text)

        text = "-----step3:无sysadmin权限的用户将属主修改为自己;" \
               "expect:修改失败，合理报错-----"
        self.logger.info(text)
        alter_cmd = f"alter directory {self.dir_name} " \
            f"owner to {self.user_name_1};"
        alter_msg = self.sh_primary.execut_db_sql(
            alter_cmd,
            sql_type=f"-U {self.user_name_1} -W '{macro.COMMON_PASSWD}'")
        self.logger.info(alter_msg)
        self.assertIn("ERROR:  must be owner of directory",
                      alter_msg, '执行失败' + text)

        text = "-----step4:无sysadmin权限的用户将属主修改为其它sysadmin用户;" \
               "expect:修改失败，合理报错-----"
        self.logger.info(text)
        alter_cmd = f"alter directory {self.dir_name} " \
            f"owner to {self.user_name_2};"
        alter_msg = self.sh_primary.execut_db_sql(
            alter_cmd,
            sql_type=f"-U {self.user_name_1} -W '{macro.COMMON_PASSWD}'")
        self.logger.info(alter_msg)
        self.assertIn("ERROR:  must be owner of directory",
                      alter_msg, '执行失败' + text)

        text = "-----step5:无sysadmin权限的用户将属主修改为其它普通用户;" \
               " expect:修改失败，合理报错-----"
        self.logger.info(text)
        alter_cmd = f"alter directory {self.dir_name} " \
            f"owner to {self.user_name_3};"
        alter_msg = self.sh_primary.execut_db_sql(
            alter_cmd,
            sql_type=f"-U {self.user_name_1} -W '{macro.COMMON_PASSWD}'")
        self.logger.info(alter_msg)
        self.assertIn("ERROR:  must be owner of directory",
                      alter_msg, '执行失败' + text)

    def tearDown(self):
        text_6 = "-----step6:删除目录，删除用户;expect:删除成功-----"
        self.logger.info(text_6)
        drop_cmd = f'''drop directory {self.dir_name};
            drop user {self.user_name_1};
            drop user {self.user_name_2};
            drop user {self.user_name_3};'''
        drop_msg = self.sh_primary.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        del_cmd = f"rm -rf {self.dir_path}"
        self.logger.info(del_cmd)
        del_msg = self.userNode.sh(del_cmd).result()
        self.logger.info(del_msg)
        check_dir_cmd = f'''if [ -d {self.dir_path} ]; 
                            then echo "exists"; 
                            else echo "not exists"; fi'''
        self.logger.info(check_dir_cmd)
        del_result = self.userNode.sh(check_dir_cmd).result()
        self.logger.info(del_result)

        text_7 = "-----step7:恢复参数;expect:恢复参数成功-----"
        self.logger.info(text_7)
        current = self.common.show_param(self.config_directory)
        if self.check_default != current:
            self.guc_result = self.sh_primary.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                f'{self.config_directory}={self.check_default}')
        show_msg = self.common.show_param(self.config_directory)
        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG,
                      drop_msg, '执行失败' + text_6)
        self.assertEquals(3, drop_msg.count(
            self.constant.DROP_ROLE_SUCCESS_MSG), '执行失败' + text_6)
        self.assertEqual("not exists", del_result, '执行失败' + text_6)
        self.assertTrue(self.guc_result, '执行失败' + text_7)
        self.assertEquals(show_msg, self.check_default, '执行失败' + text_7)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
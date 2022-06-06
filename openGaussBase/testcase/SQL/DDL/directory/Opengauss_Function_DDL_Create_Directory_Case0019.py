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
Case Name   : enable_access_server_directory=off，三权分立时，系统管理员、安全管理员和审计管理员用户创建目录对象
Description :
    1.创建目录
    2.修改guc参数enableSeparationOfDuty=on
    3.初始用户创建系统管理员、安全管理员和审计管理员用户
    4.系统管理员、安全管理员和审计管理员用户创建目录对象
    5.删除目录，删除用户
    6.恢复参数
Expect      :
    1.创建目录成功
    2.修改参数成功
    3.创建用户成功
    4.创建失败，合理报错
    5.删除成功
    6.恢复参数成功
History     :
"""
import os
import re
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
        self.user_name_1 = 'u_create_directory_0019_01'
        self.user_name_2 = 'u_create_directory_0019_02'
        self.user_name_3 = 'u_create_directory_0019_03'
        self.dir_name = 'dir_object_create_directory_0019'
        self.dir_path = os.path.join('/tmp', 'dir_create_directory_0019')
        self.guc_duty_result = ''
        self.restart_res = ''

        text = "-----step1:创建目录;expect:创建目录成功-----"
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
        self.assertEqual("exists", mkdir_result, '执行失败' + text)

        text = "-----step2:修改guc参数enableSeparationOfDuty=on;" \
               "expect:修改参数成功-----"
        self.config_duty = 'enableSeparationOfDuty'
        self.duty_default = self.common.show_param(self.config_duty)
        if 'on' != self.duty_default:
            result = self.sh_primary.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'{self.config_duty}=on')
            self.assertTrue(result, '执行失败' + text)
            restart_res = self.sh_primary.restart_db_cluster()
            self.assertTrue(restart_res, '执行失败' + text)
        show_msg = self.common.show_param(self.config_duty)
        self.logger.info(show_msg)
        self.assertEquals(show_msg, 'on', '执行失败' + text)

    def test_create_directory(self):
        text = "-----step3:初始用户创建系统管理员、安全管理员和审计管理员用户，" \
               "创建目录对象; expect:创建用户成功-----"
        self.logger.info(text)
        create_cmd = f'''drop user if exists {self.user_name_1},
            {self.user_name_2},{self.user_name_3};
            create user {self.user_name_1} sysadmin 
            password '{macro.COMMON_PASSWD}';
            create user {self.user_name_2} with createrole 
            password '{macro.COMMON_PASSWD}';
            create user {self.user_name_3} with auditadmin 
            password '{macro.COMMON_PASSWD}';'''
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG,
                      create_msg, '执行失败' + text)
        self.assertEquals(3, create_msg.count(
            self.constant.CREATE_ROLE_SUCCESS_MSG), '执行失败' + text)

        text = "-----step4:系统管理员、安全管理员和审计管理员用户创建目录对象; " \
               "expect:创建失败，合理报错-----"
        self.logger.info(text)
        names = [self.user_name_1, self.user_name_2, self.user_name_3]
        for name in names:
            create_cmd = f"create or replace directory {self.dir_name} " \
                f"as '{self.dir_path}';"
            create_msg = self.sh_primary.execut_db_sql(
                create_cmd, f'-U {name} -W {macro.COMMON_PASSWD}')
            self.logger.info(create_msg)
            self.assertIn(self.constant.PERMISSION_DENIED,
                          create_msg, '执行失败' + text)

    def tearDown(self):
        text_5 = "-----step5:删除目录，删除用户;expect:删除成功-----"
        self.logger.info(text_5)
        drop_cmd = f'''drop user {self.user_name_1};
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
        text_6 = "-----step6:恢复参数;expect:恢复参数成功-----"
        self.logger.info(text_6)
        current_duty = self.common.show_param(self.config_duty)
        if self.duty_default != current_duty:
            self.guc_duty_result = self.sh_primary.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'{self.config_duty}={self.duty_default}')
            self.restart_res = self.sh_primary.restart_db_cluster()
        show_duty_msg = self.common.show_param(self.config_duty)
        self.logger.info(show_duty_msg)
        self.assertEquals(3, drop_msg.count(
            self.constant.DROP_ROLE_SUCCESS_MSG), '执行失败' + text_5)
        self.assertEqual("not exists", del_result, '执行失败' + text_5)
        self.assertTrue(self.restart_res, '执行失败' + text_6)
        self.assertTrue(self.guc_duty_result, '执行失败' + text_6)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
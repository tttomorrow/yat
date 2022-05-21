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
Case Name   : enable_access_server_directory=off，三权分立时，
              系统管理员、安全管理员和审计管理员用户修改目录对象
Description :
    1.创建目录
    2.修改guc参数enableSeparationOfDuty=on
    3..初始用户创建系统管理员、安全管理员和审计管理员用户，创建目录对象
    4.系统管理员、安全管理员和审计管理员用户修改目录对象
    5.删除目录，删除用户
    6.恢复参数
Expect      :
    1.创建目录成功
    2.修改参数成功
    3.创建用户成功，创建目录对象成功
    4.修改失败，合理报错
    5.删除成功
    6.恢复参数成功
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
        self.user_name_1 = 'u_alter_directory_0011_01'
        self.user_name_2 = 'u_alter_directory_0011_02'
        self.user_name_3 = 'u_alter_directory_0011_03'
        self.dir_name = 'dir_alter_directory_0011'
        self.dir_path = os.path.join('/tmp', 'dir_alter_directory_0011')
        self.config_duty = 'enableSeparationOfDuty'
        self.duty_default = self.common.show_param(self.config_duty)

    def test_alter_directory(self):
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
        self.assertEquals("exists", mkdir_result, '执行失败' + text)

        text = "-----step2:修改guc参数;enableSeparationOfDuty=on;" \
               "expect:修改参数成功-----"
        if 'on' != self.duty_default:
            result = self.sh_primary.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'{self.config_duty}=on')
            self.assertTrue(result, '执行失败' + text)
            restart_res = self.sh_primary.restart_db_cluster()
            self.assertTrue(restart_res, '执行失败' + text)
        show_msg = self.common.show_param(self.config_duty)
        self.assertEquals(show_msg, 'on', '执行失败' + text)

        text = "-----step3:初始用户创建系统管理员、安全管理员和审计管理员用户，" \
               "创建目录对象; expect:创建用户成功，创建目录对象成功-----"
        self.logger.info(text)
        create_cmd = f'''create user {self.user_name_1} sysadmin 
            password '{macro.COMMON_PASSWD}';
            create user {self.user_name_2} with createrole 
            password '{macro.COMMON_PASSWD}';
            create user {self.user_name_3} with auditadmin 
            password '{macro.COMMON_PASSWD}';
            create or replace directory {self.dir_name} as '{self.dir_path}';
            select oid,dirname,owner,dirpath,diracl from pg_directory;'''
        create_msg = self.sh_primary.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_DIRECTORY_SUCCESS_MSG and
                      self.dir_name, create_msg, '执行失败' + text)
        self.assertEquals(3, create_msg.count(
            self.constant.CREATE_ROLE_SUCCESS_MSG), '执行失败' + text)

        text = "-----step4:系统管理员、安全管理员和审计管理员用户修改目录对象; " \
               "expect:修改失败，合理报错-----"
        self.logger.info(text)
        names = [self.user_name_1, self.user_name_2, self.user_name_3]
        for name in names:
            alter_cmd = f"alter directory {self.dir_name} " \
                f"owner to {name};"
            alter_msg = self.sh_primary.execut_db_sql(
                alter_cmd, sql_type=f"-U {name} -W '{macro.COMMON_PASSWD}'")
            self.logger.info(alter_msg)
            self.assertIn(self.constant.PERMISSION_DENIED,
                          alter_msg, '执行失败' + text)

    def tearDown(self):
        text_5 = "-----step5:删除目录，删除用户;expect:删除成功-----"
        self.logger.info(text_5)
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

        text_6 = "-----step6:恢复参数;expect:恢复参数成功-----"
        self.logger.info(text_6)
        current_duty = self.common.show_param(self.config_duty)
        if self.duty_default != current_duty:
            self.guc_duty_result = self.sh_primary.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'{self.config_duty}={self.duty_default}')
            self.restart_res = self.sh_primary.restart_db_cluster()
        show_duty_msg = self.common.show_param(self.config_duty)

        self.assertIn(self.constant.DROP_DIRECTORY_SUCCESS_MSG,
                      drop_msg, '执行失败' + text_5)
        self.assertEquals(3, drop_msg.count(
            self.constant.DROP_ROLE_SUCCESS_MSG), '执行失败' + text_5)
        self.assertEqual("not exists", del_result, '执行失败' + text_5)
        self.assertTrue(self.guc_duty_result, '执行失败' + text_6)
        self.assertTrue(self.restart_res, '执行失败' + text_6)
        self.assertEquals(show_duty_msg, self.duty_default, '执行失败' + text_6)
        self.logger.info(f"-----{os.path.basename(__file__)} end-----")
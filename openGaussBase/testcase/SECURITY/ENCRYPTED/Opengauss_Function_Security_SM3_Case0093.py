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
Case Type   : security_sm3
Case Name   : 设置password_encryption_type=3，认证方式sm3，copy文件内容至表中
Description :
    1.修改password_encryption_type=3，pg_haba.conf文件修改认证方式为sm3
    2.创建用户1,查看加密方式；
    3.创建表
    4.创建文件wflog，写入数据9，copy文件内容至表中，查看表中数据
Expect      :
    1.参数设置成功
    2.加密方式为sm3;
    3.创建表成功，数据插入完成
    4.文件中数据成功拷贝到表中，查看表中数据新增数据9
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Security_sm3_Case0093 start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.user = 'u_security_sm3_0093'
        self.table = 't_security_sm3_0093'
        self.copy_path = os.path.join(macro.DB_INSTANCE_PATH, 'wflog')
        self.default_msg_list1 = ''
        check_default1 = 'show enable_copy_server_files;'
        default_msg1 = self.sh_primy.execut_db_sql(check_default1)
        self.logger.info(default_msg1)
        self.default_msg_list1 = default_msg1.splitlines()[2].strip()
        self.logger.info(self.default_msg_list1)
        self.default_msg_list2 = ''
        check_default2 = 'show password_encryption_type;'
        default_msg2 = self.sh_primy.execut_db_sql(check_default2)
        self.logger.info(default_msg2)
        self.default_msg_list2 = default_msg2.splitlines()[2].strip()
        self.logger.info(self.default_msg_list2)
    
    def test_encrypted(self):
        text = '---step1:修改password_encryption_type=3，pg_haba.conf文件修改' \
               '认证方式为sm3---'
        self.logger.info(text)
        pre_cmd = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            '"enable_copy_server_files=on"'
        pre_msg = self.userNode.sh(pre_cmd).result()
        self.logger.info(pre_msg)
        check_pre_cmd = 'show enable_copy_server_files;'
        check_pre_msg = self.sh_primy.execut_db_sql(check_pre_cmd)
        self.logger.info(check_pre_msg)
        self.common.equal_sql_mdg(check_pre_msg, 'enable_copy_server_files',
                                  'on', '(1 row)', flag='1')
        text = '----step1.1：修改password_encryption_type=3----'
        self.logger.info(text)
        sql_cmd1 = f'ALTER SYSTEM SET password_encryption_type TO 3;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        check_cmd = 'show password_encryption_type;'
        check_msg = self.sh_primy.execut_db_sql(check_cmd)
        self.logger.info(check_msg)
        self.common.equal_sql_mdg(check_msg, 'password_encryption_type', '3',
                                  '(1 row)', flag='1')
        text = '------step2：创建用户1,查看用户1的加密方式-----'
        self.logger.info(text)
        sql_cmd1 = f'create user {self.user} with password ' \
            f'\'{macro.COMMON_PASSWD}\';' \
            f'grant all privileges to {self.user};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        self.logger.info(msg1)
        sql_cmd2 = f'select rolpassword from pg_authid ' \
            f'where rolname=\'{self.user}\';'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        msg2_list = msg2.splitlines()
        self.assertTrue(msg2_list[-2].strip()[:3] == 'sm3', '执行失败' + text)
        text = '------step3：创建表-----'
        self.logger.info(text)
        sql_cmd3 = f'create table {self.table}(id int);'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        self.logger.info(msg3)
        text = '--step4：创建文件wflog，写入数据9，copy文件内容至表中查看表中数据--'
        self.logger.info(text)
        exe_cmd4 = f'echo \'9\' >> {self.copy_path};'
        self.userNode.sh(exe_cmd4).result()
        sql_cmd5 = f'copy {self.table} from \'{self.copy_path}\';'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        self.logger.info(msg5)
        sql_cmd6 = f'select * from {self.table};'
        msg6 = self.sh_primy.execut_db_sql(sql_cmd6)
        self.logger.info(msg6)
        self.common.equal_sql_mdg(msg6, 'id', '9', '(1 row)', flag='1')
    
    def tearDown(self):
        self.logger.info('-------恢复参数配置------')
        exe_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            f'"enable_copy_server_files={self.default_msg_list1}"'
        msg1 = self.userNode.sh(exe_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = 'show enable_copy_server_files;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        exe_cmd3 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            f'"password_encryption_type={self.default_msg_list2}"'
        msg3 = self.userNode.sh(exe_cmd3).result()
        self.logger.info(msg3)
        sql_cmd4 = 'show password_encryption_type;'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        self.logger.info(msg4)
        self.logger.info('-------删除表、用户------')
        sql_cmd5 = f'drop table {self.table};' \
            f'drop user {self.user};'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        self.logger.info(msg5)
        self.logger.info('-------删除生成的文件------')
        exe_cmd6 = f'rm -rf {self.copy_path}'
        msg6 = self.userNode.sh(exe_cmd6).result()
        self.logger.info(msg6)
        self.logger.info('--Opengauss_Function_Security_sm3_Case0093 finish--')

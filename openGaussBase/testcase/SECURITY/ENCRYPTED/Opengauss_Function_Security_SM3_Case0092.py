"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

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
Case Name   : 设置password_encryption_type=3，认证方式sm3，gs_dump导出数据带参数-W3
Description :
    1.修改password_encryption_type=3，pg_haba.conf文件修改认证方式为sm3
    2.创建用户user001,查看user001的加密方式；
    3.创建表后插入数据，copy表中内容至文件中，查看文件wflog
Expect      :
    1.参数设置成功
    2.user001的加密方式为sm3;
    3.表中内容copy到文件中
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger

logger = Logger()


class Security(unittest.TestCase):
    def setUp(self):
        logger.info('----Opengauss_Function_Security_sm3_Case0092 start----')
        self.userNode = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.copy_path = os.path.join(macro.DB_INSTANCE_PATH, 'wflog')
        self.default_msg_list1 = ''
        check_default1 = 'show enable_copy_server_files;'
        default_msg1 = self.sh_primy.execut_db_sql(check_default1)
        logger.info(default_msg1)
        self.default_msg_list1 = default_msg1.splitlines()[2].strip()
        logger.info(self.default_msg_list1)
        self.default_msg_list2 = ''
        check_default2 = 'show password_encryption_type;'
        default_msg2 = self.sh_primy.execut_db_sql(check_default2)
        logger.info(default_msg2)
        self.default_msg_list2 = default_msg2.splitlines()[2].strip()
        logger.info(self.default_msg_list2)
    
    def test_encrypted(self):
        logger.info('--------预置条件：修改enable_copy_server_files=on--------')
        pre_cmd = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            '"enable_copy_server_files=on"'
        pre_msg = self.userNode.sh(pre_cmd).result()
        logger.info(pre_msg)
        check_pre_cmd = 'show enable_copy_server_files;'
        check_pre_msg = self.sh_primy.execut_db_sql(check_pre_cmd)
        logger.info(check_pre_msg)
        self.common.equal_sql_mdg(check_pre_msg, 'enable_copy_server_files',
                                  'on', '(1 row)', flag='1')
        logger.info('--------1.修改password_encryption_type=3--------')
        sql_cmd1 = f'ALTER SYSTEM SET password_encryption_type TO 3;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        check_cmd = 'show password_encryption_type;'
        check_msg = self.sh_primy.execut_db_sql(check_cmd)
        logger.info(check_msg)
        self.common.equal_sql_mdg(check_msg, 'password_encryption_type', '3',
                                  '(1 row)', flag='1')
        logger.info('--------2.创建用户user001,查看user001的加密方式-------')
        sql_cmd1 = f'create user user001 with password ' \
            f'\'{macro.COMMON_PASSWD}\';grant all privileges to user001;'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1)
        logger.info(msg1)
        sql_cmd2 = f'select rolpassword from pg_authid ' \
            f'where rolname=\'user001\';'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        msg2_list = msg2.splitlines()
        self.assertTrue(msg2_list[-2].strip()[:3] == 'sm3')
        logger.info('---3.创建表插入数据，copy表中内容至文件wflog，查看文件wflog---')
        sql_cmd3 = f'create table table001(id int);' \
                   f'insert into table001 values(3);' \
                   f'copy table001 to \'{self.copy_path}\';'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        logger.info('---4.查看生成的dump091.sql---')
        exe_cmd5 = f'cat {self.copy_path};rm -rf {self.copy_path}'
        msg5 = self.userNode.sh(exe_cmd5).result()
        logger.info(msg5)
        self.assertIn('3', msg5)
    
    def tearDown(self):
        logger.info('-------1.恢复参数配置------')
        exe_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            f'"enable_copy_server_files={self.default_msg_list1}"'
        msg1 = self.userNode.sh(exe_cmd1).result()
        logger.info(msg1)
        sql_cmd2 = 'show enable_copy_server_files;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        logger.info(msg2)
        self.common.equal_sql_mdg(msg2, 'enable_copy_server_files',
                                  f'{self.default_msg_list1}', '(1 row)',
                                  flag='1')
        exe_cmd3 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            f'"password_encryption_type={self.default_msg_list2}"'
        msg3 = self.userNode.sh(exe_cmd3).result()
        logger.info(msg3)
        sql_cmd4 = 'show password_encryption_type;'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        self.common.equal_sql_mdg(msg4, 'password_encryption_type',
                                  f'{self.default_msg_list2}', '(1 row)',
                                  flag='1')
        logger.info('-------2.删除表、用户------')
        sql_cmd5 = f'drop table table001;' \
            f'drop user user001;'
        msg5 = self.sh_primy.execut_db_sql(sql_cmd5)
        logger.info(msg5)
        self.assertTrue('DROP ROLE' in msg5 and 'DROP TABLE' in msg5)
        logger.info('-------3.删除生成的文件------')
        exe_cmd6 = f'rm -rf {self.copy_path}'
        msg6 = self.userNode.sh(exe_cmd6).result()
        logger.info(msg6)
        logger.info('----Opengauss_Function_Security_sm3_Case0092 finish----')

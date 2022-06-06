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
Case Name   : 使用gs_guc set方式设置加密方式为sm3，初始化数据库带参数--auth-host=sm3
Description :
    1.修改password_encryption_type=3
    2.初始化数据库
    3.查看$data/pg_hba.conf文件中认证方式
    4.gaussdb方法启动数据库，默认端口
    5.使用默认端口连接数据库
Expect      :
    1.参数设置成功
    2.初始化成功，生成data目录
    3.host所在行认证方式为sm3
    4.数据库启动成功
    5.数据库连接成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.ComThread import ComThread




class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info('--Opengauss_Function_Security_sm3_Case0088 start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.userNode2 = Node(node='PrimaryDbUser')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.port = '5432'
        self.dbname = 'postgres'
        self.dir_path = os.path.join(macro.DB_INSTANCE_PATH, 'datadir')
        self.default_msg_list = ''
        check_default = 'show password_encryption_type;'
        default_msg = self.sh_primy.execut_db_sql(check_default)
        self.logger.info(default_msg)
        self.default_msg_list = default_msg.splitlines()[2].strip()
        self.logger.info(self.default_msg_list)
    
    def test_encrypted(self):
        text = '---step1.修改password_encryption_type=3;expect:成功---'
        self.logger.info(text)
        exe_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            '"password_encryption_type=3"'
        msg1 = self.userNode.sh(exe_cmd1).result()
        self.logger.info(msg1)
        check_cmd = 'show password_encryption_type;'
        check_msg = self.sh_primy.execut_db_sql(check_cmd)
        self.logger.info(check_msg)
        self.common.equal_sql_mdg(check_msg, 'password_encryption_type', '3',
                                  '(1 row)', flag='1')
        text = '--------step2.初始化数据库;expect:成功--------'
        self.logger.info(text)
        exe_cmd2 = f'source {self.DB_ENV_PATH};gs_initdb -D ' \
            f'{self.dir_path} --nodename=dn_new --auth-host=sm3'
        self.logger.info(exe_cmd2)
        msg2 = self.userNode.sh(exe_cmd2).result()
        self.logger.info(msg2)
        text = '---step3.查看$data/pg_hba.conf文件中认证方式;expect:成功---'
        self.logger.info(text)
        file_path = os.path.join(self.dir_path, 'pg_hba.conf')
        exe_cmd3 = f'grep "host.*sm3" {file_path}'
        msg3 = self.userNode.sh(exe_cmd3).result()
        self.logger.info(msg3)
        self.assertTrue(msg3.count('sm3') >= 2, '执行失败' + text)
        text = '---step4.gaussdb方法启动数据库，默认端口;expect:成功---'
        self.logger.info(text)
        exe_cmd4 = f'source {self.DB_ENV_PATH};' \
            f'gaussdb -D {self.dir_path} -M primary'
        self.logger.info(exe_cmd4)
        thread_2 = ComThread(self.userNode2.sh, args=(exe_cmd4,))
        thread_2.setDaemon(True)
        thread_2.start()
        thread_2.join(10)
        msg_result_2 = thread_2.get_result()
        self.logger.info(msg_result_2)
        text = '---step5.使用默认端口连接数据库;expect:成功---'
        self.logger.info(text)
        exe_cmd5 = f'source {self.DB_ENV_PATH};' \
            f'gsql -d {self.dbname} -p {self.port} -c "\\q"'
        self.logger.info(exe_cmd5)
        msg5 = self.userNode2.sh(exe_cmd5).result()
        self.logger.info(msg5)
        self.assertEqual('', msg5, '执行失败' + text)
    
    def tearDown(self):
        self.logger.info('-------1.恢复加密方式配置------')
        exe_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            f'"password_encryption_type={self.default_msg_list}"'
        msg1 = self.userNode.sh(exe_cmd1).result()
        self.logger.info(msg1)
        sql_cmd2 = 'show password_encryption_type;'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.logger.info('-------2.清理目录-------')
        exe_cmd3 = f'rm -rf {self.dir_path};ls {self.dir_path}'
        msg3 = self.userNode.sh(exe_cmd3).result()
        self.logger.info(msg3)
        self.logger.info('-------3.清理进程-------')
        exe_cmd4 = f'ps -ef | grep "gaussdb -D {self.dir_path}" |grep -v ' \
            '\'grep\' | awk \'{{print $2}}\' | ' \
            'xargs kill -9'
        self.logger.info(exe_cmd4)
        msg4 = self.userNode.sh(exe_cmd4).result()
        self.logger.info(msg4)
        self.logger.info('--Opengauss_Function_Security_sm3_Case0088 finish--')

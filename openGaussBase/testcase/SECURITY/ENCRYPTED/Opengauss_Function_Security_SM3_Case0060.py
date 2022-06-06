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
Case Type   : Interface
Case Name   : 加密算法与认证过程中的加密算法均为sm3,非初始用户正确的密码通过ODBC连接数据库
Description :
    1.安装unixODBC
    2.创建用户，配置加密方式和认证方式为sm3
    3.配置数据源
    4.检查依赖库
    5.连接数据库
    6.编译脚本
    7.执行脚本
Expect      :
    1.安装成功
    2.用户创建成功，配置完成
    3.配置完成
    4.依赖库配置完成
    5.连接成功
    6.编译成功
    7.执行成功
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class Security(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.userNode = Node(node='PrimaryDbUser')
        self.primary_root = Node(node='PrimaryRoot')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.targetpath = '/etc'
        self.local_path = '/usr/local/odbclib'
        self.odbc_lib_path = os.path.join(self.local_path, 'odbc', 'lib')
        self.sourcefile = os.path.join(self.local_path, "odbcsrc")
        self.compile = 'ODBCInterFace'
        self.user = 'user_security_sm3_0060'
        self.default_param = self.common.show_param('password_encryption_type')
    
    def test_encrypted(self):
        text = '-----step1：安装unixODBC;expect:成功-----'
        self.logger.info(text)
        self.common.install_odbc(self.primary_root, self.local_path,
                                 'Complete!')
        
        text = '---step2.1:设置加密方式为sm3;expect:成功---'
        self.logger.info(text)
        cp_cmd = f"cp {os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba_bak.conf')};"
        self.userNode.sh(cp_cmd).result()
        self.sh_primy.execute_gsguc('reload', self.constant.GSGUC_SUCCESS_MSG,
                                    f'password_encryption_type=3')
        text = '---step2.2:创建用户;expect:成功---'
        self.logger.info(text)
        create_cmd = f'drop user if exists {self.user} cascade;' \
            f'create user {self.user} password \'{macro.COMMON_PASSWD}\';'
        create_msg = self.sh_primy.execut_db_sql(create_cmd)
        self.logger.info(create_msg)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, create_msg, text)
        text = '---step2.3:pg_hba.conf文件中增加认证方式为sm3;expect:成功---'
        self.logger.info(text)
        exe_cmd2 = f'source {macro.DB_ENV_PATH};' \
            f'gs_guc reload -D {macro.DB_INSTANCE_PATH} -h ' \
            f'"host {self.userNode.db_name} {self.user} ' \
            f'{self.userNode.db_host}/32 sm3"'
        self.logger.info(exe_cmd2)
        msg2 = self.userNode.sh(exe_cmd2).result()
        self.logger.info(msg2)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, msg2, text)
        
        text = '---step3:配置数据源;expect:成功---'
        self.logger.info(text)
        ini_content = [self.userNode.db_host, self.userNode.db_name,
                       self.user, macro.COMMON_PASSWD,
                       self.userNode.db_port]
        odbc_ini = self.common.set_odbc_ini(self.primary_root, ini_content,
                                            self.local_path)
        self.assertTrue(odbc_ini, text)
        odbcinst_ini = self.common.set_odbcinst_ini(self.primary_root,
                                                    self.local_path,
                                                    self.odbc_lib_path)
        self.assertTrue(odbcinst_ini, text)
        odbc_src = self.common.set_odbc_src(self.primary_root, self.local_path,
                                            self.odbc_lib_path,
                                            self.sourcefile)
        self.assertTrue(odbc_src, text)
        
        text = '---step4:检查依赖库;expect:成功---'
        self.logger.info(text)
        lib_file = os.path.join(self.odbc_lib_path, 'psqlodbcw.so')
        self.common.check_libfile(self.primary_root, lib_file,
                                  os.path.join(self.local_path, 'lib'))
        
        text = '---step5:连接数据库;expect:成功---'
        self.logger.info(text)
        exe_cmd8 = f'source {self.sourcefile};' \
            f'isql -v gaussodbc &'
        self.logger.info(exe_cmd8)
        msg8 = self.primary_root.sh(exe_cmd8).result()
        self.logger.info(msg8)
        self.assertIn('Connected!', msg8, '执行失败' + text)
        
        text = '---step6:编译文件;expect:成功---'
        self.logger.info(text)
        self.primary_root.scp_put(
            os.path.join(macro.SCRIPTS_PATH, self.compile + '.c'),
            os.path.join(self.local_path, self.compile + '.c'))
        exe_compile = f"source {self.sourcefile};gcc -c " \
            f"'{os.path.join(self.local_path, self.compile + '.c')}' -o " \
            f"'{os.path.join(self.local_path, self.compile + '.o')}';" \
            f"gcc -o " \
            f"{os.path.join(self.local_path, self.compile)} " \
            f"{os.path.join(self.local_path, self.compile + '.o')} " \
            f"{lib_file};"
        self.logger.info(exe_compile)
        msg_compile = self.primary_root.sh(exe_compile).result()
        self.logger.info(msg_compile)
        check_file_cmd = f'ls {os.path.join(self.local_path, self.compile)}'
        check_file_msg = self.primary_root.sh(check_file_cmd).result()
        self.logger.info(check_file_msg)
        self.assertNotIn('No such file or directory', check_file_msg,
                         '执行失败' + text)
        
        text = '---step7:执行脚本;expect:成功---'
        self.logger.info(text)
        exe_cmd9 = f'source {self.sourcefile};' \
            f'/./{os.path.join(self.local_path, self.compile)}'
        msg9 = self.primary_root.sh(exe_cmd9).result()
        self.logger.info(msg9)
        self.assertEqual(msg9.count('Success!'), 23, '执行失败' + text)
    
    def tearDown(self):
        text = '---step1.恢复配置文件中的信息;expect:成功---'
        self.logger.info(text)
        check_cmd = f'mv ' \
            f'{os.path.join(macro.DB_INSTANCE_PATH, "pg_hba_bak.conf")} ' \
            f'{os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")};' \
            f'rm -rf {os.path.join(self.local_path, "odbc.ini")} ' \
            f'{os.path.join(self.local_path, "odbcinst.ini")} ' \
            f'{self.sourcefile} ' \
            f'{os.path.join(self.local_path, self.compile + "*")}'
        self.logger.info(check_cmd)
        self.primary_root.sh(check_cmd).result()

        text = '-----step2:重启数据库;expect:成功-----'
        self.logger.info(text)
        node_num = self.common.get_node_num(self.primary_root)
        self.logger.info(node_num)
        if node_num == 1:
            self.sh_primy.execute_gsctl('restart',
                                        self.constant.REBUILD_SUCCESS_MSG)
        else:
            self.sh_primy.execute_gsctl('restart',
                                        self.constant.REBUILD_SUCCESS_MSG,
                                        param="-M primary")

        text = '---step4:恢复加密方式;expect:成功---'
        self.logger.info(text)
        self.sh_primy.execute_gsguc('reload', self.constant.GSGUC_SUCCESS_MSG,
                            f'password_encryption_type={self.default_param}')

        text = '---step5:清理用户;expect:成功---'
        self.logger.info(text)
        drop_cmd = f'drop user {self.user} cascade;'
        drop_msg = self.sh_primy.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, drop_msg, text)
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

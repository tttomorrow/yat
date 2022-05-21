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
Case Name   : 加密算法md5+sha256，认证方式sm3，非初始用户错误的密码通过ODBC连接数据库
Description :
    1.安装unixODBC
    2.创建用户，配置加密方式md5+sha256,认证方式为sm3
    3.配置数据源
    4.检查依赖库
    5.在客户端配置环境变量,导入环境变量
    6.连接数据库
Expect      :
    1.安装成功
    2.用户创建成功，配置完成
    3.配置完成
    4.依赖库配置完成
    5.环境变量导入
    6.数据库连接失败
History     :
"""
import os
import re
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
        self.logger.info('--Opengauss_Function_Security_SM3_Case0081 start--')
        self.userNode = Node(node='PrimaryDbUser')
        self.primary_root = Node(node='PrimaryRoot')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.user = 'u_security_sm3_0081'
        self.default_param = self.common.show_param('password_encryption_type')
        self.targetpath = '/etc'
        self.local_path = '/usr/local'
        self.compile = 'ODBCInterFace'
    
    def test_encrypted(self):
        text = '------step1：安装unixODBC包;expect:成功------'
        self.logger.info(text)
        self.common.install_odbc(self.primary_root, self.local_path,
                                 'Complete!')
        
        text = '---step2.1:设置加密方式为md5+sha256;expect:成功---'
        self.logger.info(text)
        cp_cmd = f"cp {os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba_bak.conf')};"
        self.userNode.sh(cp_cmd).result()
        self.sh_primy.execute_gsguc('reload', self.constant.GSGUC_SUCCESS_MSG,
                                    f'password_encryption_type=1')
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
        odbc_content = f'[gaussodbc]\n' \
            f'Driver=PostgreSQL\n' \
            f'Servername={self.userNode.db_host}\n' \
            f'Database={self.userNode.db_name}\n' \
            f'Username={self.user}\n' \
            f'Password={macro.COMMON_PASSWD}_error\n' \
            f'Port={self.userNode.db_port}\n' \
            f'ReadOnly=No\n'
        write_cmd1 = f"echo '{odbc_content}' > " \
            f"{os.path.join(self.targetpath, 'odbc.ini')}"
        self.logger.info(write_cmd1)
        write_msg1 = self.primary_root.sh(write_cmd1).result()
        self.logger.info(write_msg1)
        check_cmd = f'cat {os.path.join(self.targetpath, "odbc.ini")}'
        self.logger.info(check_cmd)
        result = self.primary_root.sh(check_cmd).result()
        self.logger.info(result)
        assert1 = re.search(
            r".*Driver.*Servername.*Database.*Username.*Password.*Port",
            result, re.S)
        self.assertTrue(assert1, '执行失败:' + text)
        
        text = '---step3.2:写配置文件odbcinst.ini;expect:成功---'
        self.logger.info(text)
        lib_file = os.path.join(self.local_path, 'lib', 'psqlodbcw.so')
        odbcinst_content = f'[PostgreSQL]\n' \
            f'Driver64={lib_file}\n' \
            f'Setup={lib_file}\n'
        write_cmd2 = f"echo '{odbcinst_content}' > " \
            f"{os.path.join(self.targetpath, 'odbcinst.ini')}"
        self.logger.info(write_cmd2)
        write_msg2 = self.primary_root.sh(write_cmd2).result()
        self.logger.info(write_msg2)
        check_cmd = f'cat {os.path.join(self.targetpath, "odbcinst.ini")}'
        self.logger.info(check_cmd)
        result = self.primary_root.sh(check_cmd).result()
        self.logger.info(result)
        assert2 = re.search(r".*Driver64.*Setup.*", result, re.S)
        self.assertTrue(assert2, '执行失败:' + text)

        text = '---step4:检查依赖库;expect:成功---'
        self.logger.info(text)
        self.common.check_libfile(self.primary_root, lib_file,
                                  os.path.join(self.local_path, 'lib'))
        cp_ld_cmd = f"cp {os.path.join(self.targetpath, 'ld.so.conf')} " \
            f"{os.path.join(self.targetpath, 'ld.so_bak.conf')}"
        self.primary_root.sh(cp_ld_cmd).result()
        self.common.odbc_symbolic_link(self.primary_root,
                                       os.path.join(self.local_path, 'lib'),
                                       os.path.join(self.targetpath,
                                                    'ld.so.conf'))
        text = '---step5:在客户端配置环境变量,导入环境变量;expect:成功---'
        self.logger.info(text)
        lib_path = os.path.join(self.local_path, 'lib')
        import_content = f'export ' \
            f'LD_LIBRARY_PATH={lib_path}:$LD_LIBRARY_PATH;' \
            f'export ODBCSYSINI={self.targetpath};' \
            f'export ODBCINI={os.path.join(self.targetpath, "odbc.ini")}'
        write_cmd3 = f"echo '{import_content}' > " \
            f"{os.path.join(self.local_path, 'sourcefile')}"
        self.logger.info(write_cmd3)
        write_msg3 = self.primary_root.sh(write_cmd3).result()
        self.assertEqual(write_msg3, '', '执行失败' + text)
        
        text = '---step6:连接数据库;expect:成功---'
        self.logger.info(text)
        exe_cmd8 = f'source {os.path.join(self.local_path, "sourcefile")};' \
            f'isql -v gaussodbc &'
        self.logger.info(exe_cmd8)
        msg8 = self.primary_root.sh(exe_cmd8).result()
        self.logger.info(msg8)
        self.assertNotIn('Connected!', msg8, '执行失败' + text)
    
    def tearDown(self):
        text = '---step1.恢复配置文件中的信息;expect:成功---'
        self.logger.info(text)
        check_cmd = f'mv ' \
            f'{os.path.join(macro.DB_INSTANCE_PATH, "pg_hba_bak.conf")} ' \
            f'{os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")};' \
            f'mv -f {os.path.join(self.targetpath, "ld.so_bak.conf")} ' \
            f'{os.path.join(self.targetpath, "ld.so.conf")};' \
            f'rm -rf {os.path.join(self.targetpath, "odbc.ini")} ' \
            f'{os.path.join(self.targetpath, "odbcinst.ini")} ' \
            f'{os.path.join(self.local_path, "sourcefile")} ' \
            f'{os.path.join(self.local_path, self.compile + "*")}'
        self.logger.info(check_cmd)
        self.primary_root.sh(check_cmd).result()
        text = '---step2:重启数据库;expect:成功---'
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
        text = '---step3:恢复加密方式;expect:成功---'
        self.logger.info(text)
        self.sh_primy.execute_gsguc('reload', self.constant.GSGUC_SUCCESS_MSG,
                            f'password_encryption_type={self.default_param}')
        text = '---step4:清理用户;expect:成功---'
        self.logger.info(text)
        drop_cmd = f'drop user {self.user} cascade;'
        drop_msg = self.sh_primy.execut_db_sql(drop_cmd)
        self.logger.info(drop_msg)
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, drop_msg, text)
        self.logger.info('--Opengauss_Function_Security_SM3_Case0081 finish--')

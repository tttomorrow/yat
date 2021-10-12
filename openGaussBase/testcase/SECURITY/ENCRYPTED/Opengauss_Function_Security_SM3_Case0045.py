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
Case Name   : 创建用户时的加密算法sm3，认证方式MD5，非初始用户错误的密码通过JDBC连接数据库
Description :
    1.修改password_encryption_type=3
    2.pg_hba.conf文件中修改认证方式为MD5
    3.非初始用户错误的密码通过JDBC登录数据库
Expect      :
    1-2.参数设置成功
    3.数据库连接失败
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
        logger.info('---Opengauss_Function_Security_sm3_Case0044 start---')
        self.userNode = Node('PrimaryDbUser')
        self.primary_root = Node('PrimaryRoot')
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.DB_INSTANCE_PATH = macro.DB_INSTANCE_PATH
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.targetpath = "/home/jdbc_test"
        self.properties = os.path.join(self.targetpath, "jdbc_connect.conf")
        self.java_name = "jdbc_drop_schema_case0001"
        self.config = os.path.join(self.DB_INSTANCE_PATH, 'pg_hba.conf')
        self.confignew = os.path.join(self.DB_INSTANCE_PATH, 'pg_hba_bak.conf')
        logger.info('--------获取参数默认值--------')
        self.default_msg_list = ''
        check_default = 'show password_encryption_type;'
        default_msg = self.sh_primy.execut_db_sql(check_default)
        logger.info(default_msg)
        self.default_msg_list = default_msg.splitlines()[2].strip()
        logger.info(self.default_msg_list)
        logger.info('--------备份白名单文件---------')
        cp_cmd = f"cp {self.config} {self.confignew}"
        self.userNode.sh(cp_cmd).result()
    
    def test_encrypted(self):
        logger.info('--------1.修改password_encryption_type=3--------')
        exe_cmd1 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            '"password_encryption_type=3"'
        msg1 = self.userNode.sh(exe_cmd1).result()
        logger.info(msg1)
        check_cmd = 'show password_encryption_type;'
        check_msg = self.sh_primy.execut_db_sql(check_cmd)
        logger.info(check_msg)
        self.common.equal_sql_mdg(check_msg, 'password_encryption_type', '3',
                                  '(1 row)', flag='1')
        logger.info('--------2.pg_hba.conf文件中增加认证方式为md5--------')
        exe_cmd2 = f'grep  "IPv4 local connections:" {self.config}'
        msg2 = self.userNode.sh(exe_cmd2).result()
        logger.info(msg2)
        insert_messages = f"host {self.userNode.db_name} user001 " \
            f"{self.userNode.db_host}/32 md5"
        exe_cmd3 = f'sed -i "/{msg2}/a\{insert_messages}" {self.config}'
        logger.info(exe_cmd3)
        msg3 = self.userNode.sh(exe_cmd3).result()
        logger.info(msg3)
        logger.info('--------3.创建用户user001--------')
        sql_cmd4 = f'create user user001 with password \'' \
            f'{macro.COMMON_PASSWD}\';'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        self.assertTrue('CREATE ROLE' in msg4)
        logger.info('--------4.1 写入配置文件，用户user001设置错误的密码-------')
        self.common.scp_file(self.primary_root,
                             f"{self.java_name}.java", self.targetpath)
        result = self.primary_root.sh(
            f"touch {self.properties}").result()
        logger.info(result)
        config = f'echo "password=1qaz2WSX"> {self.properties}'
        self.primary_root.sh(config)
        config = f'echo "port={self.userNode.db_port}">> ' \
            f'{self.properties}'
        self.primary_root.sh(config)
        config = f'echo "hostname={self.userNode.db_host}">> ' \
            f'{self.properties}'
        self.primary_root.sh(config)
        config = f'echo "user=user001">> {self.properties}'
        self.primary_root.sh(config)
        config = f'echo "dbname={self.userNode.db_name}">> ' \
            f'{self.properties}'
        self.primary_root.sh(config)
        config = f'cat {self.properties}'
        result = self.primary_root.sh(config).result()
        self.assertTrue("password=" in result and "port=" in result and
                        "hostname=" in result and "user=" in result
                        and "dbname=" in result)
        logger.info('---------4.2 编译java脚本----------')
        scp_cmd = self.primary_root.scp_put(macro.JDBC_PATH,
                                        f"{self.targetpath}/postgresql.jar")
        logger.info(scp_cmd)
        cmd = f"javac -encoding utf-8 -cp " \
            f"{os.path.join(self.targetpath, 'postgresql.jar')} " \
            f"{os.path.join(self.targetpath, f'{self.java_name}.java')}"
        logger.info(cmd)
        result = self.primary_root.sh(cmd).result()
        logger.info(result)
        logger.info("--------4.3 运行java脚本，数据库连接成功---------")
        cmd = f" java -cp {os.path.join(self.targetpath, 'postgresql.jar')}" \
            f":{self.targetpath} " \
            f"{self.java_name} -F {self.properties}"
        logger.info(cmd)
        result = self.primary_root.sh(cmd).result()
        logger.info(result)
        self.assertIn('连接失败', result)
    
    def tearDown(self):
        logger.info('-------1.恢复配置文件中的信息------')
        rec_cmd = f"rm -rf {self.config};" \
            f"mv {self.confignew} {self.config};" \
            f"rm -rf {self.targetpath};" \
            f"ls {self.targetpath}"
        rec_msg = self.primary_root.sh(rec_cmd).result()
        self.assertIn('No such file or directory', rec_msg)
        logger.info('-------2.恢复加密方式配置------')
        exe_cmd2 = f'source {self.DB_ENV_PATH};' \
            f'gs_guc reload -D {self.DB_INSTANCE_PATH} -c ' \
            f'"password_encryption_type={self.default_msg_list}"'
        msg2 = self.userNode.sh(exe_cmd2).result()
        logger.info(msg2)
        sql_cmd3 = 'show password_encryption_type;'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3)
        logger.info(msg3)
        logger.info('-------3.删除用户-------')
        sql_cmd4 = 'drop user user001'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4)
        logger.info(msg4)
        logger.info('----Opengauss_Function_Security_sm3_Case0044 finish----')

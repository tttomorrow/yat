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
Case Type   : security-auditing
Case Name   : 关闭数据库对象CMK、CEK的CREATE、DROP操作审计功能
Description :
    1.设置audit_system_object=1048575
    2.gsql客户端-C连接数据库，创建cmk
    3.gsql客户端-C连接数据库，创建cek
    4.gsql客户端-C连接数据库,删除cmk,cek
    5.登录数据库，查看审计日志,时间设在最接近登录数据库的时间
Expect      :
    1.设置成功
    2.创建成功
    3.创建成功
    4.删除成功
    4.未查询到创建、删除CMK、CEK信息
History     :
"""
import re
import os
import unittest
from time import sleep
from yat.test import Node
from yat.test import macro
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            '------Opengauss_Function_Security_Auditing_Case0152 start-----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.userNode = Node('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.cmk = 'cmk_security_audit_0152'
        self.cek = 'cek_security_audit_0152'
        self.key_path = 'keypath_security_audit_0152'
        self.default_param = self.common.show_param('audit_system_object')
        self.localkms = os.path.join(macro.DB_INSTANCE_PATH, '..', 'app',
                                     'etc', 'localkms')
    
    def test_security(self):
        text = '----pre1:配置$GAUSSHOME/etc/localkms路径;expect:成功---'
        self.logger.info(text)
        mkdir_cmd = f'if [ ! -d "{self.localkms}" ];' \
            f'then mkdir {self.localkms};fi'
        self.logger.info(mkdir_cmd)
        self.userNode.sh(mkdir_cmd).result()
        text = 'step1:设置参数audit_system_object=1048575;expect:成功'
        self.logger.info(text)
        self.sh_primy.execute_gsguc('reload', self.constant.GSGUC_SUCCESS_MSG,
                                    f'audit_system_object=1048575')
        self.logger.info('------获取起始时间点-----')
        start_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        start_time = start_time_msg.splitlines()[2].strip()
        self.logger.info(start_time)
        sleep(5)
        text = '--step2-4:gsql客户端-C连接数据库，创建、删除cmk、cek;expect:成功--'
        self.logger.info(text)
        sql_cmd1 = f'drop column encryption key if exists {self.cek};' \
            f'drop client master key if exists {self.cmk};' \
            f'create client master key {self.cmk} with ' \
            f'(key_store = localkms, key_path = "{self.key_path}", ' \
            f'algorithm = rsa_2048);' \
            f'create column encryption key {self.cek} with values ' \
            f'(client_master_key = {self.cmk}, algorithm  = ' \
            f'aead_aes_256_cbc_hmac_sha256);' \
            f'drop column encryption key {self.cek};' \
            f'drop client master key {self.cmk};'
        excute_cmd1 = f'source {macro.DB_ENV_PATH};' \
            f'gsql -d {self.userNode.db_name} -p {self.userNode.db_port} ' \
            f'-C -c "{sql_cmd1}"'
        msg1 = self.userNode.sh(excute_cmd1).result()
        self.logger.info(msg1)
        assert1 = re.search(
            r".*CREATE CLIENT MASTER KEY.*CREATE COLUMN ENCRYPTION KEY.*"
            r"DROP COLUMN ENCRYPTION KEY.*DROP CLIENT MASTER KEY.*",
            msg1, re.S)
        self.assertTrue(assert1, '执行失败:' + text)
        sleep(5)
        end_time_msg = self.sh_primy.execut_db_sql('SELECT sysdate;')
        end_time = end_time_msg.splitlines()[2].strip()
        sql_cmd2 = f'select result,detail_info from ' \
            f'pg_query_audit(\'{start_time}\', \'{end_time}\');'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        assert2 = re.search(
            r".*ok.*create client master key.*ok.*create column encryption.*"
            r".*ok.*drop column encryption key.*ok.*drop client master key.*",
            msg2, re.S)
        self.assertFalse(assert2, '执行失败:' + text)
    
    def tearDown(self):
        text1 = '----恢复配置----'
        self.logger.info(text1)
        rev_msg = self.sh_primy.execute_gsguc('reload',
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f'audit_system_object={self.default_param}')
        self.logger.info(rev_msg)
        check_msg = self.sh_primy.execut_db_sql('show audit_system_object;')
        self.logger.info(check_msg)
        text2 = '----删除文件----'
        self.logger.info(text2)
        clean_cmd = f"rm -rf {self.localkms}"
        self.logger.info(clean_cmd)
        clean_msg = self.userNode.sh(clean_cmd).result()
        self.assertEqual('', clean_msg, text2 + '执行失败')
        self.common.equal_sql_mdg(check_msg, 'audit_system_object',
                                  f'{self.default_param}', '(1 row)', flag='1')
        self.logger.info(
            '----Opengauss_Function_Security_Auditing_Case0152 end-----')

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
Case Type   : security-EqualityQuery
Case Name   : 关闭全密态开关，无法创建cek
Description :
    1.gsql客户端-C连接数据库，创建cmk
    2.gsql客户端不加-C连接数据库，创建cek
Expect      :
    1.创建成功
    2.报错： disable client-encryption feature, please use -C to enable it
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.userNode = Node('PrimaryDbUser')
        self.cmk = 'cmk_security_qualityquery_0043'
        self.cek = 'cek_security_qualityquery_0043'
        self.key_path = 'keypath_security_qualityquery_0043'
        self.localkms = os.path.join(macro.DB_INSTANCE_PATH, '..', 'app',
                                     'etc', 'localkms')
    
    def test_security(self):
        text = '----pre1:配置$GAUSSHOME/etc/localkms路径;expect:成功---'
        self.logger.info(text)
        mkdir_cmd = f'if [ ! -d "{self.localkms}" ];' \
            f'then mkdir {self.localkms};fi'
        self.logger.info(mkdir_cmd)
        self.userNode.sh(mkdir_cmd).result()
        text = '---step1:gsql客户端-C连接数据库，创建cmk;expect:成功---'
        self.logger.info(text)
        sql_cmd1 = f'drop client master key if exists {self.cmk};' \
            f'create client master key {self.cmk} with ' \
            f'(key_store = localkms, key_path = "{self.key_path}", ' \
            f'algorithm = rsa_3072);'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type='-C')
        self.logger.info(msg1)
        self.assertIn(self.constant.create_cmk_success, msg1, text + '执行失败')

        text = '---step1:gsql客户端不加-C连接数据库，创建cek;expect:失败---'
        self.logger.info(text)
        sql_cmd2 = f'create column encryption key {self.cek} with values ' \
            f'(client_master_key = {self.cmk}, ' \
            f'algorithm = aead_aes_256_cbc_hmac_sha256);'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2)
        self.logger.info(msg2)
        self.assertIn('disable client-encryption feature, please use -C '
                      'to enable it', msg2, text + '执行失败')
    
    def tearDown(self):
        text1 = '----清理数据库创建的资源----'
        self.logger.info(text1)
        sql_cmd1 = f'drop client master key {self.cmk};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type='-C')
        self.logger.info(msg1)
        text2 = '----删除文件----'
        self.logger.info(text2)
        clean_cmd = f"rm -rf {self.localkms}"
        self.logger.info(clean_cmd)
        clean_msg = self.userNode.sh(clean_cmd).result()
        self.assertIn(self.constant.drop_cmk_success, msg1, '执行失败:' + text1)
        self.assertEqual('', clean_msg, text2 + '执行失败')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

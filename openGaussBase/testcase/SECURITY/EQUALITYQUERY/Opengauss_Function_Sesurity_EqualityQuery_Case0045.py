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
Case Name   : 创建cek的加密算法SM4_SM3，cmk的加密算法仅支持SM2
Description :
    1.gsql客户端-C连接数据库，创建cmk,加密算法SM2
    2.gsql客户端-C连接数据库，创建cmk,加密算法RSA_3072
    3.gsql客户端-C连接数据库，创建cek，加密算法SM4_SM3，cmk选择第1步创建的
    4.gsql客户端-C连接数据库，创建cek，加密算法SM4_SM3，cmk选择第2步创建的
Expect      :
    1.创建成功
    2.创建成功
    3.创建成功
    4.报错：ERROR(CLIENT): National secret algorithm must be used together.
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
        self.cmk1 = 'cmk01_security_qualityquery_0045'
        self.cmk2 = 'cmk02_security_qualityquery_0045'
        self.cek1 = 'cek01_security_qualityquery_0045'
        self.cek2 = 'cek02_security_qualityquery_0045'
        self.key_path1 = 'keypath01_security_qualityquery_0045'
        self.key_path2 = 'keypath02_security_qualityquery_0045'
        self.localkms = os.path.join(macro.DB_INSTANCE_PATH, '..', 'app',
                                     'etc', 'localkms')
    
    def test_security(self):
        text = '----pre1:配置$GAUSSHOME/etc/localkms路径;expect:成功---'
        self.logger.info(text)
        mkdir_cmd = f'if [ ! -d "{self.localkms}" ];' \
            f'then mkdir {self.localkms};fi'
        self.logger.info(mkdir_cmd)
        self.userNode.sh(mkdir_cmd).result()
        text = '---step1:gsql客户端-C连接数据库，创建cmk,加密算法SM2;expect:成功---'
        self.logger.info(text)
        sql_cmd1 = f'drop client master key if exists {self.cmk1};' \
            f'create client master key {self.cmk1} with ' \
            f'(key_store = localkms, key_path = "{self.key_path1}", ' \
            f'algorithm = sm2);'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type='-C')
        self.logger.info(msg1)
        self.assertIn(self.constant.create_cmk_success, msg1, text + '执行失败')
        
        text = '--step2:gsql客户端-C创建cmk,加密算法RSA_3072;expect:成功--'
        self.logger.info(text)
        sql_cmd2 = f'drop client master key if exists {self.cmk2};' \
            f'create client master key {self.cmk2} with ' \
            f'(key_store = localkms, key_path = "{self.key_path2}", ' \
            f'algorithm = rsa_3072);'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2, sql_type='-C')
        self.logger.info(msg2)
        self.assertIn(self.constant.create_cmk_success, msg2, text + '执行失败')
        
        text = '--step3-4:gsql客户端-C连接创建cek，加密算法SM4_SM3;expect:成功--'
        self.logger.info(text)
        sql_cmd3 = f'create column encryption key {self.cek1} with values ' \
            f'(client_master_key = {self.cmk1}, ' \
            f'algorithm = sm4_sm3);' \
            f'create column encryption key {self.cek2} with values ' \
            f'(client_master_key = {self.cmk2}, algorithm = sm4_sm3);'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3, sql_type='-C')
        self.logger.info(msg3)
        self.assertIn(self.constant.create_cek_success, msg3, text + '执行失败')
        self.assertIn('National secret algorithm must be used together',
                      msg3, text + '执行失败')
    
    def tearDown(self):
        text1 = '----清理数据库创建的资源----'
        self.logger.info(text1)
        sql_cmd1 = f'drop column encryption key {self.cek1};' \
            f'drop client master key {self.cmk1};' \
            f'drop client master key {self.cmk2};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type='-C')
        self.logger.info(msg1)
        text = '----删除文件----'
        self.logger.info(text)
        clean_cmd = f"rm -rf {self.localkms}"
        clean_msg = self.userNode.sh(clean_cmd).result()
        self.assertTrue(msg1.count(self.constant.drop_cmk_success) == 2,
                        text + '执行失败')
        self.assertIn(self.constant.drop_cek_success, msg1, text + '执行失败')
        self.assertEqual('', clean_msg, text + '执行失败')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

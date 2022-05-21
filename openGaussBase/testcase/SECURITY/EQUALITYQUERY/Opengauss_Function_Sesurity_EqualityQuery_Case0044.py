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
Case Name   : cek未删除不能直接删除cmk
Description :
    1.gsql客户端-C连接数据库，创建cmk
    2.gsql客户端-C连接数据库，创建cek
    3.删除cmk
    4.删除cek，再删除cmk
Expect      :
    1.创建成功
    2.创建成功
    3.报错：cannot drop client master key
    4.删除成功
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
        self.cmk = 'cmk_security_qualityquery_0044'
        self.cek = 'cek_security_qualityquery_0044'
        self.key_path = 'keypath_security_qualityquery_0044'
        self.localkms = os.path.join(macro.DB_INSTANCE_PATH, '..', 'app',
                                     'etc', 'localkms')
    
    def test_security(self):
        text = '----pre1:配置$GAUSSHOME/etc/localkms路径;expect:成功---'
        self.logger.info(text)
        mkdir_cmd = f'if [ ! -d "{self.localkms}" ];' \
            f'then mkdir {self.localkms};fi'
        self.logger.info(mkdir_cmd)
        self.userNode.sh(mkdir_cmd).result()
        text = '---step1-2:gsql客户端-C连接数据库，创建cmk,cek;expect:成功---'
        self.logger.info(text)
        sql_cmd1 = f'drop client master key if exists {self.cmk} cascade;' \
            f'create client master key {self.cmk} with ' \
            f'(key_store = localkms, key_path = "{self.key_path}", ' \
            f'algorithm = rsa_3072);' \
            f'create column encryption key {self.cek} with values ' \
            f'(client_master_key = {self.cmk}, ' \
            f'algorithm = aead_aes_256_cbc_hmac_sha256);'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type='-C')
        self.logger.info(msg1)
        self.assertIn(self.constant.create_cek_success, msg1, text + '执行失败')

        text = '---step3:删除cmk;expect:失败---'
        self.logger.info(text)
        sql_cmd2 = f'drop client master key {self.cmk};'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2, sql_type='-C')
        self.logger.info(msg2)
        self.assertIn(f'cannot drop client master key', msg2, text + '执行失败')

        text = '---step4:删除cek，再删除cmk;expect:失败---'
        self.logger.info(text)
        sql_cmd2 = f'drop column encryption key {self.cek};' \
            f'drop client master key if exists {self.cmk};'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2, sql_type='-C')
        self.logger.info(msg2)
        self.assertIn(self.constant.drop_cmk_success, msg2, text + '执行失败')
    
    def tearDown(self):
        text = '----删除文件----'
        self.logger.info(text)
        clean_cmd = f"rm -rf {self.localkms}"
        clean_msg = self.userNode.sh(clean_cmd).result()
        self.assertEqual('', clean_msg, text + '执行失败')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

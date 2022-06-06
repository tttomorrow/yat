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
Case Name   : 删除$GAUSSHOME/etc/localkms路径下密钥，再删除cmk
Description :
    1.gsql客户端-C连接数据库，创建cmk，
    2.删除$GAUSSHOME/etc/localkms路径下生成密钥文件，再删除cmk
Expect      :
    1.创建成功
    2.删除成功，提示密钥文件已经不存在得相关信息
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
        self.cmk = 'cmk_security_qualityquery_0038'
        self.key_path = 'keypath_security_qualityquery_0038'
        self.localkms = os.path.join(macro.DB_INSTANCE_PATH, '..', 'app',
                                     'etc', 'localkms')
    
    def test_security(self):
        text = '----pre1:配置$GAUSSHOME/etc/localkms路径;expect:成功---'
        self.logger.info(text)
        mkdir_cmd = f'if [ ! -d "{self.localkms}" ];' \
            f'then mkdir {self.localkms};fi'
        self.logger.info(mkdir_cmd)
        self.userNode.sh(mkdir_cmd).result()
        text = '---step1:gsql客户端连接数据库加-C参数，创建cmk;expect:成功---'
        self.logger.info(text)
        sql_cmd1 = f'drop client master key if exists {self.cmk};' \
            f'create client master key {self.cmk} with ' \
            f'(key_store = localkms, key_path = "{self.key_path}", ' \
            f'algorithm = sm2);'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type='-C')
        self.logger.info(msg1)
        self.assertIn(self.constant.create_cmk_success, msg1, text + '执行失败')
        exe_cmd2 = f'ls {self.localkms}'
        self.logger.info(exe_cmd2)
        msg2 = self.userNode.sh(exe_cmd2).result()
        self.logger.info(msg2)
        self.assertIn(f'{self.key_path}.priv', msg2, text + '执行失败')
        
        text = '---step2:删除$GAUSSHOME/etc/localkms路径下生成密钥文件，' \
               '再删除cmk;expect:成功---'
        self.logger.info(text)
        clean_cmd = f"rm -rf {os.path.join(self.localkms, '*')};"
        self.logger.info(clean_cmd)
        self.userNode.sh(clean_cmd).result()
        sql_cmd3 = f'drop client master key {self.cmk};'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3, sql_type='-C')
        self.logger.info(msg3)
        self.assertIn('failed to remove file', msg3, text + '执行失败')
        self.assertIn(self.constant.drop_cmk_success, msg3, text + '执行失败')
    
    def tearDown(self):
        text = '----删除文件----'
        self.logger.info(text)
        clean_cmd = f"rm -rf {self.localkms}"
        clean_msg = self.userNode.sh(clean_cmd).result()
        self.assertEqual('', clean_msg, text + '执行失败')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

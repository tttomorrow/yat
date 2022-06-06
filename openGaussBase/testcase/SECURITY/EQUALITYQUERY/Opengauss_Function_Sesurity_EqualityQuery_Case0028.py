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
Case Name   : cmk命名不符合标识符规范得无法创建
Description :
    1.gsql客户端-C连接数据库，创建cmk，名称以数字开头
    2.gsql客户端-C连接数据库，创建cmk，名称以特殊符号开头
Expect      :
    1.报错：ERROR:  syntax error at or near "123"
    2.报错：ERROR:  syntax error at or near "*#"
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
        self.cmk1 = '123cmk_security_qualityquery_0028'
        self.cmk2 = '*#$cmk_security_qualityquery_0028'
        self.key_path1 = 'keypath_security_qualityquery_0028'
        self.key_path2 = 'keypath02_security_qualityquery_0028'
        self.localkms = os.path.join(macro.DB_INSTANCE_PATH, '..', 'app',
                                     'etc', 'localkms')
    
    def test_security(self):
        text = '-----pre1:配置$GAUSSHOME/etc/localkms路径;expect:成功-----'
        self.logger.info(text)
        mkdir_cmd = f'if [ ! -d "{self.localkms}" ];' \
            f'then mkdir {self.localkms};fi'
        self.logger.info(mkdir_cmd)
        self.userNode.sh(mkdir_cmd).result()
        text = '--step1:gsql客户端-C连接数据库创建cmk，名称以数字开头;expect:失败--'
        self.logger.info(text)
        sql_cmd1 = f'create client master key {self.cmk1} with ' \
            f'(key_store = localkms, key_path = "{self.key_path1}", ' \
            f'algorithm = rsa_2048);'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type='-C')
        self.logger.info(msg1)
        self.assertIn('syntax error at or near', msg1, text + '执行失败')
        text = '-step2:gsql客户端-C连接数据库创建cmk，名称以特殊符号开头;expect:失败-'
        self.logger.info(text)
        sql_cmd2 = f'create client master key {self.cmk2} with ' \
            f'(key_store = localkms, key_path = "{self.key_path2}", ' \
            f'algorithm = rsa_2048);'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2, sql_type='-C')
        self.logger.info(msg2)
        self.assertIn('syntax error at or near', msg2, text + '执行失败')
    
    def tearDown(self):
        text1 = '----删除文件----'
        self.logger.info(text1)
        clean_cmd = f"rm -rf {self.localkms}"
        self.logger.info(clean_cmd)
        clean_msg = self.userNode.sh(clean_cmd).result()
        self.assertEqual('', clean_msg, text1 + '执行失败')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

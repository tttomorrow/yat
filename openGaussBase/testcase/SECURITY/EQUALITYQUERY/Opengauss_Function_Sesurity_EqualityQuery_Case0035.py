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
Case Name   : 手动配置该环境变量$LOCALKMS_FILE_PATH，删除cmk，密钥文件自动删除
Description :
    1.手动配置该环境变量$LOCALKMS_FILE_PATH（路径自行配置）
    2.gsql客户端连接数据库加-C参数，创建cmk，$LOCALKMS_FILE_PATH路径下生成密钥文件
    3.删除cmk,密钥文件自动删除
Expect      :
    1.配置成功
    2.创建成功
    3.删除成功
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
        self.cmk = 'cmk_security_qualityquery_0035'
        self.key_path = 'keypath_security_qualityquery_0035'
        self.env_new = os.path.join(macro.DB_INSTANCE_PATH, 'newenv')
    
    def test_security(self):
        text = '---step1:手动配置该环境变量$LOCALKMS_FILE_PATH;expect:成功---'
        self.logger.info(text)
        conf_cmd = f'cp {macro.DB_ENV_PATH} {self.env_new};' \
            f'sed -i \'$aexport LOCALKMS_FILE_PATH=' \
            f'{macro.DB_INSTANCE_PATH}\' {macro.DB_ENV_PATH};'
        self.logger.info(conf_cmd)
        conf_msg = self.userNode.sh(conf_cmd).result()
        self.logger.info(conf_msg)
        
        text = '---step2.1:gsql客户端连接数据库加-C参数，创建cmk，' \
               '$LOCALKMS_FILE_PATH路径下生成密钥文件;expect:成功---'
        self.logger.info(text)
        sql_cmd1 = f'drop client master key if exists {self.cmk};' \
            f'create client master key {self.cmk} with ' \
            f'(key_store = localkms, key_path = "{self.key_path}", ' \
            f'algorithm = rsa_3072);'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type='-C')
        self.logger.info(msg1)
        text = '---step2.2:检查生成密钥文件;expect:成功---'
        self.logger.info(text)
        exe_cmd2 = f'ls {macro.DB_INSTANCE_PATH}'
        msg2 = self.userNode.sh(exe_cmd2).result()
        self.logger.info(msg2)
        self.assertIn(f'{self.key_path}', msg2, text + '执行失败')

        text = '---step3:删除cmk,密钥文件自动删除;expect:成功---'
        self.logger.info(text)
        sql_cmd3 = f'drop client master key {self.cmk};'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3, sql_type='-C')
        self.logger.info(msg3)
        self.assertIn(self.constant.drop_cmk_success, msg3, text + '执行失败')
        exe_cmd4 = f'ls {macro.DB_INSTANCE_PATH}'
        msg4 = self.userNode.sh(exe_cmd4).result()
        self.logger.info(msg4)
        self.assertNotIn(f'{self.key_path}', msg4, text + '执行失败')

    def tearDown(self):
        text = '----恢复环境----'
        self.logger.info(text)
        clean_cmd = f"mv {self.env_new} {macro.DB_ENV_PATH}"
        self.logger.info(clean_cmd)
        clean_msg = self.userNode.sh(clean_cmd).result()
        self.assertEqual('', clean_msg, text + '执行失败')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

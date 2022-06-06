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
Case Name   : 加密表中插入数据进行等值查询，加密列作为查询条件
Description :
    1.gsql客户端-C连接数据库，创建cmk
    2.gsql客户端-C连接数据库，创建cek
    3.gsql客户端-C连接数据库，创建加密表
    4.gsql客户端-C连接数据库，加密列作为查询条件进行等值查询
Expect      :
    1.创建成功
    2.创建成功
    3.创建成功，数据插入完成
    4.查询到值为1
History     :
"""
import os
import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.Logger import Logger


class Auditing(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.logger.info(f'-----{os.path.basename(__file__)} start-----')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.userNode = Node('PrimaryDbUser')
        self.cmk = 'cmk_security_qualityquery_0046'
        self.cek = 'cek_security_qualityquery_0046'
        self.key_path = 'keypath_security_qualityquery_0046'
        self.table = 'table_security_qualityquery_0046'
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
            f'algorithm = sm2);'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type='-C')
        self.logger.info(msg1)
        self.assertIn(self.constant.create_cmk_success, msg1, text + '执行失败')
        
        text = '--step2:gsql客户端-C连接数据库，创建cek;expect:成功--'
        self.logger.info(text)
        sql_cmd2 = f'create column encryption key {self.cek} with values ' \
            f'(client_master_key = {self.cmk}, ' \
            f'algorithm = sm4_sm3);'
        msg2 = self.sh_primy.execut_db_sql(sql_cmd2, sql_type='-C')
        self.logger.info(msg2)
        self.assertIn(self.constant.create_cek_success, msg2, text + '执行失败')
        
        text = '--step3:gsql客户端-C连接数据库，创建加密表;expect:成功--'
        self.logger.info(text)
        sql_cmd3 = f'create table {self.table} (id_number int, name text' \
            f' encrypted with (column_encryption_key = {self.cek}, ' \
            f'encryption_type = deterministic),credit_card varchar(19)' \
            f' encrypted with (column_encryption_key = {self.cek}, ' \
            f'encryption_type = deterministic));' \
            f'insert into {self.table} values ' \
            f'insert into creditcard_info values ' \
            f'(2, \'joy\',\'6219985678349800033\');'
        msg3 = self.sh_primy.execut_db_sql(sql_cmd3, sql_type='-C')
        self.logger.info(msg3)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, msg3, text + '执行失败')
        
        text = '--step4:gsql客户端-C连接数据库，加密列作为查询条件进行等值查询;' \
               'expect:成功--'
        self.logger.info(text)
        sql_cmd4 = f'select id_number from {self.table} where name = \'joe\';'
        msg4 = self.sh_primy.execut_db_sql(sql_cmd4, sql_type='-C')
        self.logger.info(msg4)
        self.common.equal_sql_mdg(msg4, 'id_number', '1', '(1 row)', flag='1')
    
    def tearDown(self):
        text1 = '----清理数据库创建的资源----'
        self.logger.info(text1)
        sql_cmd1 = f'drop table {self.table};' \
            f'drop column encryption key {self.cek};' \
            f'drop client master key {self.cmk};'
        msg1 = self.sh_primy.execut_db_sql(sql_cmd1, sql_type='-C')
        self.logger.info(msg1)
        text = '----删除文件----'
        self.logger.info(text)
        clean_cmd = f"rm -rf {self.localkms}"
        clean_msg = self.userNode.sh(clean_cmd).result()
        self.assertIn(self.constant.DROP_TABLE_SUCCESS, msg1, text + '执行失败')
        self.assertIn(self.constant.drop_cmk_success, msg1, text + '执行失败')
        self.assertEqual('', clean_msg, text + '执行失败')
        self.logger.info(f'-----{os.path.basename(__file__)} end-----')

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
Case Type   : 全密态
Case Name   :加密表支持explain打印加密列的等值过滤查询
Description :
    1、配置全密态环境变量
    2、连接全密态数据库，分别创建cmk，cek
    3、创建两张加密表
    4、两张表分别插入数据
    5、explain打印加密列的等值过滤查询
    6、清理环境
Expect      :
    1、配置成功
    2、成功
    3、成功
    4、成功
    5、成功
    6、成功
History     :
"""
import unittest
import os
from yat.test import Node
from yat.test import macro
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class FullDensityState(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        self.Constant = Constant()
        self.userNode = Node('PrimaryDbUser')
        self.sh_primy = CommonSH('PrimaryDbUser')
        self.cmk = 'cmk_security_qualityquery_0021'
        self.cek = 'cek_security_qualityquery_0021'
        self.tab1 = 't_security_qualityquery_0021_01'
        self.tab2 = 't_security_qualityquery_0021_02'
        self.key_path = 'keypath_security_qualityquery_0021'
        self.localkms = os.path.join(macro.DB_INSTANCE_PATH, '..', 'app',
                                     'etc', 'localkms')

    def test_create_cmk_cek(self):
        self.logger.info(f'-----{os.path.basename(__file__)}' + ' start-----')
        text = '---step1:配置$GAUSSHOME/etc/localkms路径;expect:成功---'
        self.logger.info(text)
        mkdir_cmd = f'if [ ! -d "{self.localkms}" ];' \
                    f'then mkdir {self.localkms};fi'
        self.logger.info(mkdir_cmd)
        self.userNode.sh(mkdir_cmd).result()

        text = '--step2:连接全密态数据库，分别创建cmk，cek;expect:成功---'
        self.logger.info(text)
        sql_cmd = f'''drop client master key if exists {self.cmk} cascade;
            create client master key {self.cmk} with
            (key_store=localkms,key_path="{self.key_path}",
            algorithm=rsa_2048);
            drop column encryption key if exists {self.cek} cascade;
            create column encryption key {self.cek} with values
            (client_master_key = {self.cmk},algorithm = 
            aead_aes_256_cbc_hmac_sha256);'''
        self.logger.info(sql_cmd)
        msg = self.sh_primy.execut_db_sql(sql_cmd, sql_type='-C')
        self.logger.info(msg)
        self.assertIn(self.Constant.create_cmk_success, msg, text + '执行失败')
        self.assertIn(self.Constant.create_cek_success, msg, text + '执行失败')
        text = '--step3:创建两张加密表;expect:成功---'
        self.logger.info(text)
        sql_cmd = f'''drop table if exists {self.tab1};
            create table {self.tab1} (id_number int,name1 text encrypted 
            with (column_encryption_key = {self.cek}, encryption_type = 
            deterministic),name2 text encrypted with 
            (column_encryption_key = {self.cek}, encryption_type = 
            deterministic),credit_card varchar(19) encrypted with 
            (column_encryption_key={self.cek}, encryption_type = 
            deterministic))with (orientation=row);
            create table {self.tab2} (id_number int,name1 text encrypted 
            with (column_encryption_key = {self.cek}, encryption_type = 
            deterministic),name2 text encrypted with 
            (column_encryption_key = {self.cek}, encryption_type = 
            deterministic),credit_card varchar(19) encrypted with 
            (column_encryption_key={self.cek}, encryption_type = 
            deterministic))with (orientation=row);'''
        self.logger.info(sql_cmd)
        msg1 = self.sh_primy.execut_db_sql(sql_cmd, sql_type='-C')
        self.logger.info(msg1)
        self.assertTrue(msg1.count(self.Constant.CREATE_TABLE_SUCCESS) == 2,
                        '执行失败' + text)
        text = '---step4:两张表分别插入数据;expect:成功---'
        self.logger.info(text)
        sql_cmd = f'''insert into {self.tab1} values
        insert into {self.tab1} values(2,'joy','joy',6219985678349800033);
        insert into {self.tab1} values
        insert into {self.tab2} values(1,'joe','joe',62176500);
        insert into {self.tab2} values(2,'joy','joy',62199856);
        insert into {self.tab2} values(3,'li','li',62117780);'''
        self.logger.info(sql_cmd)
        msg1 = self.sh_primy.execut_db_sql(sql_cmd, sql_type='-C')
        self.logger.info(msg1)
        self.assertTrue(msg1.count(self.Constant.INSERT_SUCCESS_MSG) == 6,
                        text + '执行失败')
        text = '---step5:explain打印加密列的等值过滤查询;expect:成功---'
        self.logger.info(text)
        sql_cmd = f'''explain select * from (select * from {self.tab2}) 
        as a,(select * from {self.tab1}) as b where 
        a.credit_card = 62176500 and a.name1='joe' and b.name1 = 'joe';'''
        self.logger.info(sql_cmd)
        msg1 = self.sh_primy.execut_db_sql(sql_cmd, sql_type='-C')
        self.logger.info(msg1)
        self.assertTrue(msg1.count('Seq Scan on') == 2, '执行失败' + text)

    def tearDown(self):
        text = '---step6:清理环境 expect:成功---'
        self.logger.info(text)
        sql_cmd = f'''drop table {self.tab1};
        drop table {self.tab2};
        drop column encryption key {self.cek} cascade; 
        drop client master key {self.cmk} cascade;'''
        self.logger.info(sql_cmd)
        msg1 = self.sh_primy.execut_db_sql(sql_cmd, sql_type='-C')
        self.logger.info(msg1)
        del_cmd = f'rm -rf {self.localkms}'
        self.logger.info(del_cmd)
        del_res = self.userNode.sh(del_cmd).result()
        self.logger.info(del_res)
        self.assertTrue(msg1.count(self.Constant.DROP_TABLE_SUCCESS) == 2,
                        text + '执行失败')
        self.assertIn(self.Constant.drop_cek_success, msg1, text + '执行失败')
        self.assertIn(self.Constant.drop_cmk_success, msg1, text + '执行失败')
        self.assertEqual('', del_res, text + '执行失败')
        self.logger.info(f'-----{os.path.basename(__file__)}' + ' end-----')

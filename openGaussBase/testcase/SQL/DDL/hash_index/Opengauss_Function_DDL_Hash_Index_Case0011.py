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
Case Type   : 功能
Case Name   : 同一个字段创建btree索引和hash索引
Description :
        1.建表并创建btree索引
        2.使用btree索引
        3.设置btree索引不可用
        4.创建hash索引
        5.使用哈希索引
        6.清理环境
Expect      :
        1.创建成功
        2.数据量大时查询计划走索引扫描
        3.设置成功
        4.创建成功
        5.索引数据存在且查询计划走索引扫描
        6.清理环境完成
History     :
"""
import unittest

from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH


class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0011start-')
        self.constant = Constant()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = "t_hash_index_0011"
        self.id_name = "i_hash_index_0011"
        self.id_name_01 = "i_hash_index_0011_01"

    def test_standby(self):
        text = '--step1:建表并创建btree索引;expect:创建成功--'
        self.log.info(text)
        create_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists 
            {self.tb_name};
           create table {self.tb_name} (id int, num int, sex varchar(20) \
            default 'male');
            insert into {self.tb_name} select random()*10, random()*3, \
            'XXX' from generate_series(1,5000);
            drop index if exists {self.id_name};
            create index {self.id_name} on {self.tb_name} using btree (id);''')
        self.log.info(create_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, create_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, create_cmd,
                      '执行失败:' + text)

        text = '--step2:使用索引;expect:查询计划走索引扫描--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''select count(*) from \
            {self.tb_name} where id=10;
            explain select count(*) from {self.tb_name} where id=10;''')
        self.log.info(sql_cmd)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

        text = '--step3:设置btree索引不可用;expect:查询计划走顺序扫描--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''alter index {self.id_name} \
            unusable;
            explain select count(*) from {self.tb_name} where id=10;''')
        self.log.info(sql_cmd)
        self.assertIn('ALTER INDEX', sql_cmd, '执行失败:' + text)
        self.assertIn('Seq Scan', sql_cmd, '执行失败:' + text)

        text = '--step4:创建hash索引;expect:创建成功--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f''' drop index if exists \
            {self.id_name_01};
            create index {self.id_name_01} on {self.tb_name} using \
            hash (id);''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, create_cmd,
                      '执行失败:' + text)

        text = '--step5:使用索引;expect:查询计划走索引扫描--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''select count(*) from \
            {self.tb_name} where id=10;
            explain select count(*) from {self.tb_name} where id=10;''')
        self.log.info(sql_cmd)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step6:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists \
            {self.tb_name};''')
        self.log.info(sql_cmd)
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0011finish--')

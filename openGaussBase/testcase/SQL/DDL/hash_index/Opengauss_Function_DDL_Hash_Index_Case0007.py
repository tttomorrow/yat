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
Case Name   : 创建索引后dump，drop索引后， 恢复数据
Description :
    1.创建测试库和表并创建hash索引
    2.dump数据
    3.删除索引
    4.恢复数据
    5.查询索引
    6.使用索引
    7.清理环境
Expect      :
    1.创建成功
    2.dump成功
    3.删除索引成功
    4.恢复数据成功
    5.索引存在
    6.索引数据存在且数据量大时走索引扫描
    7.清理环境完成
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class DDL(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0007start-')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = "t_hash_index_0007"
        self.id_name = "i_hash_index_0007"
        self.db_name = "db_hash_index_0007"
        self.dump_file = os.path.join(macro.DB_INSTANCE_PATH,
                                      'hash_index_0007.tar')

    def test_hash_index(self):
        text = '---step1:创建测试库和表;expect:创建成功-------'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};\
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        sql_cmd = f'''drop table if exists {self.tb_name};\
            create table {self.tb_name} (id int, num int, sex varchar(20) \
            default 'male');\
            insert into {self.tb_name} select random()*10, random()*3, 'XXX' \
            from generate_series(1,5000);drop index if exists {self.id_name};\
            drop index if exists {self.id_name};\
            create index {self.id_name} on {self.tb_name} using hash (id);'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)

        text = '---step2:导出指定数据库;expect:导出成功-------'
        self.log.info(text)
        dump_cmd = f"source {macro.DB_ENV_PATH};" \
                   f" gs_dump {self.db_name} " \
                   f"-p {self.primary_node.db_port} " \
                   f"-f {self.dump_file} -F t"
        self.log.info(dump_cmd)
        result = self.primary_node.sh(dump_cmd).result()
        self.log.info(result)
        flag = 'dump database ' + self.db_name + ' successfully'
        self.assertTrue(result.find(flag) > -1, '执行失败:' + text)

        text = '---step3:删除索引;expect:删除成功-------'
        self.log.info(text)
        sql_cmd = f'''drop index if exists {self.id_name};'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.DROP_INDEX_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)

        text = '---step4:导入之前导出的数据;expect:导出成功-------'
        self.log.info(text)
        restore_cmd = f"source {macro.DB_ENV_PATH};" \
                      f"gs_restore -p {self.primary_node.db_port} " \
                      f"-d {self.db_name} " \
                      f"{self.dump_file}"
        self.log.info(restore_cmd)
        result = self.primary_node.sh(restore_cmd).result()
        self.log.info(result)
        self.assertIn(self.constant.RESTORE_SUCCESS_MSG, result,
                      '执行失败:' + text)

        text = '--step5:查看hash索引;expect:索引存在--'
        self.log.info(text)
        sql_cmd = f'''\d+ {self.tb_name} '''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertTrue(sql_result.find(f'{self.id_name}') > -1)

        text = '--step6:使用索引;expect:索引数据存在且数据量大时走索引扫描--'
        self.log.info(text)
        sql_cmd = f'''set enable_seqscan = off;\
                select count(*) from {self.tb_name} where id=10;\
                explain select count(*) from {self.tb_name} \
                where id=10;'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn('1 row', sql_result, '执行失败:' + text)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_result, '执行失败:' + text)

    def tearDown(self):
        text = 'step7:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};''')
        self.log.info(sql_cmd)
        del_cmd = f'''rm -rf  {self.dump_file}'''
        msg = self.primary_node.sh(del_cmd).result()
        self.log.info(msg)
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0007finish--')

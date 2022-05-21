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
Case Type   : Hash分区表
Case Name   : 创建local索引并向分区表中插入数据，通过索引检索表中数据
Description :
    1、创建Hash分区表
    2、向分区表中插入数据
    3、创建local索引
    4、使用explain查询数据
    5、清理环境
Expect      :
    1、创建Hash分区表成功
    2、向分区表中插入数据成功
    3、创建local索引成功
    4、使用explain查询数据成功
    5、清理环境成功
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class HashPartitionCase(unittest.TestCase):

    def setUp(self):
        self.logger = Logger()
        self.logger.info(
            "---Opengauss_Function_DDL_Partition_Hash_Case0024开始执行---")
        self.commonsh = CommonSH("PrimaryDbUser")
        self.tab_name = "partition_hash_tab"
        self.index_name = "partition_index_01"

    def test_query_dop(self):
        step1_text = "---step1:创建Hash分区表;expect:建表成功---"
        self.logger.info(step1_text)
        sql_cmd1 = f'''drop table if exists {self.tab_name};
            create table {self.tab_name}(p_id int)
            partition by hash(p_id)
            (partition p1,
             partition p2,
             partition p3,
             partition p4);'''
        self.logger.info(sql_cmd1)
        sql_res1 = self.commonsh.execut_db_sql(sql_cmd1)
        self.logger.info(sql_res1)
        self.assertIn("CREATE TABLE", sql_res1, "执行失败" + step1_text)

        step2_text = "---step2:为分区表插入数据;expect:插入数据成功---"
        self.logger.info(step2_text)
        sql_cmd2 = f'''BEGIN
              for i in 1..2000 LOOP
                insert into {self.tab_name} values(i);
              end LOOP;
            end;'''
        self.logger.info(sql_cmd2)
        sql_res2 = self.commonsh.execut_db_sql(sql_cmd2)
        self.logger.info(sql_res2)
        self.assertIn("ANONYMOUS BLOCK EXECUTE", sql_res2,
                      "执行失败:" + step2_text)

        step3_text = "---step3:创建local索引;expect:创建成功---"
        self.logger.info(step3_text)
        sql_cmd3 = f'''drop index if exists {self.index_name};
        create index {self.index_name} on {self.tab_name}(p_id) local;'''
        self.logger.info(sql_cmd3)
        sql_res3 = self.commonsh.execut_db_sql(sql_cmd3)
        self.logger.info(sql_res3)
        self.assertIn("CREATE INDEX", sql_res3, "执行失败:" + step2_text)

        step4_text = "---step4:使用explain查询数据;expect:索引启用成功---"
        self.logger.info(step4_text)
        explain_res = self.commonsh.execut_db_sql(
            f'''explain select * from {self.tab_name} where p_id = 1995;''')
        self.logger.info(explain_res)
        assert_info = "Bitmap Index Scan on partition_index_01"
        self.assertIn(assert_info, explain_res, "执行失败:" + step4_text)

    def tearDown(self):
        self.logger.info("---清理环境---")

        drop_text = "---删除索引、分区表---"
        self.logger.info(drop_text)
        drop_cmd = f'''drop index if exists {self.index_name};
            drop table if exists {self.tab_name} cascade;'''
        self.logger.info(drop_cmd)
        drop_res = self.commonsh.execut_db_sql(drop_cmd)
        self.logger.info(drop_res)

        self.assertIn("DROP INDEX", drop_res, "执行失败" + drop_text)
        self.assertIn("DROP TABLE", drop_res, "执行失败" + drop_text)
        self.logger.info(
            "---Opengauss_Function_DDL_Partition_Hash_Case0024执行结束---")

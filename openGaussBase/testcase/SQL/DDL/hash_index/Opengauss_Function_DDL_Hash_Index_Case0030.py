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
Case Name   : 创建哈希索引后，查询计划后的where过滤条件设置不合理，即使索引
              存在，查询计划仍走顺序扫描
Description :
    1.创建测试表和哈希索引
    2.使用索引,where条件后为表达式
    3.使用索引,where条件后为函数
    4.使用索引,where条件后为类型转换
    5.使用索引,where条件后为逻辑操作符
    6.使用索引,where条件后为模糊匹配
    7.清理环境
Expect      :
    1.创建成功
    2.索引数据存在；索引失效，查询计划走顺序扫描
    3.索引数据存在；索引失效，查询计划走顺序扫描
    4.索引数据存在；索引失效，查询计划走顺序扫描
    5.索引数据存在；索引失效，查询计划走顺序扫描
    6.索引数据存在；索引失效，查询计划走顺序扫描
    7.清理环境完成
History     :
"""

import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class DdlTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0030start-')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = "t_hash_index_0030"
        self.id_name = "i_hash_index_0030"

    def test_hash_index(self):
        text = '---step1:创建测试表和哈希索引;expect:创建成功-------'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists \
            {self.tb_name};
            create table {self.tb_name} (id int, num int, sex varchar 
            default 'male');
            insert into {self.tb_name} select random()*10, random()*3, 'XXX' \
            from generate_series(1,5000);drop index if exists \
           {self.id_name};
           drop index if exists {self.id_name};
           create index {self.id_name} on {self.tb_name} using hash (id);''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        text = '--step2:使用索引,where条件后为表达式;' \
               'expect:索引数据存在；索引失效，查询计划走顺序扫描--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''explain select count(*) \
            from {self.tb_name} where id+1=10;''')
        self.log.info(sql_cmd)
        self.assertIn('Seq Scan', sql_cmd, '执行失败:' + text)

        text = '--step3:使用索引,where条件后为函数;' \
               'expect:索引数据存在；索引失效，查询计划走顺序扫描--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''explain select count(*) from \
        {self.tb_name} where power(id,2)=1;''')
        self.log.info(sql_cmd)
        self.assertIn('Seq Scan', sql_cmd, '执行失败:' + text)

        text = '--step4:使用索引,where条件后为类型转换;' \
               'expect:索引数据存在；索引失效，查询计划走顺序扫描--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''explain select count(*) from \
            {self.tb_name} where id::varchar = '10';''')
        self.log.info(sql_cmd)
        self.assertIn('Seq Scan', sql_cmd, '执行失败:' + text)

        text = '--step5:使用索引,where条件后为逻辑操作符;' \
               'expect:索引数据存在；索引失效，查询计划走顺序扫描--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''explain select count(*) from \
            {self.tb_name} where id != 10;
            explain select count(*) from {self.tb_name} where id is \
            not null;''')
        self.log.info(sql_cmd)
        self.assertIn('Seq Scan', sql_cmd, '执行失败:' + text)

        text = '--step6:使用索引,where条件后为模糊匹配;' \
               'expect:索引数据存在；索引失效，查询计划走顺序扫描--'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''explain select count(*) from \
            {self.tb_name} where id like '%10';''')
        self.log.info(sql_cmd)
        self.assertIn('Seq Scan', sql_cmd, '执行失败:' + text)

    def tearDown(self):
        self.log.info('--步骤7:清理环境--')
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop table if exists \
            {self.tb_name};''')
        self.log.info(sql_cmd)
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0030finish--')

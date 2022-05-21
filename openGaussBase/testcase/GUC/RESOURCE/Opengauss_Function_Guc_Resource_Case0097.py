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
Case Type   : GUC参数--资源消耗
Case Name   : 通过explain(analyze,buffers)查看多少数据来源磁盘，
              多少来源shared_buffers
Description :
        1、查询shared_buffers默认值；
        2、创建表并插入数据
        3、创建索引
        4、执行explain (analyze,buffers)语句
        5、再次执行上述语句
        6、清理环境
Expect      :
        1、显示默认值为1GB，资料描述默认值是8MB，om工具修改
        2、创建表并插入数据成功
        3、创建索引成功
        4、执行计划中的结果以shared read显示，表示取自磁盘且不被缓存
        5、再次执行查询计划后，结果以shared hit显示，表示读取shared_buffers
        6、清理环境完成
History     :
"""
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class GUC(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '--Opengauss_Function_Guc_Resource_Case0097.py start----')
        self.Constant = Constant()
        self.commonsh = CommonSH('dbuser')

    def test_startdb(self):
        self.log.info('步骤1:查询该参数默认值')
        sql_cmd = self.commonsh.execut_db_sql('''show shared_buffers;''')
        self.log.info(sql_cmd)
        self.assertEqual('1GB', sql_cmd.splitlines()[-2].strip())
        self.log.info('步骤2:创建表并插入数据')
        sql_cmd = self.commonsh.execut_db_sql('''drop table if exists test_97;
        create table test_97(id int,name varchar(20));
        begin
           for i in 1..100 loop
               insert into test_97 values(i,i||'a');
           end loop;
        end;
        ''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_ANONYMOUS_BLOCK_SUCCESS_MSG,
                      sql_cmd)
        self.log.info('步骤3:创建索引')
        sql_cmd = self.commonsh.execut_db_sql('''create index t_index on 
            test_97 using btree(id);''')
        self.log.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_INDEX_SUCCESS_MSG,
                      sql_cmd)
        self.log.info('步骤4:执行测试语句')
        sql_cmd = self.commonsh.execut_db_sql('''explain (analyze,buffers) 
                    select * from test_97 where id =45;''')
        self.log.info(sql_cmd)
        self.assertIn('Buffers: shared hit', sql_cmd)

    def tearDown(self):
        self.log.info('-------清理环境------------------')
        sql_cmd = self.commonsh.execut_db_sql('drop table if exists test_97;')
        self.log.info(sql_cmd)
        self.log.info(
            '-----Opengauss_Function_Guc_Resource_Case0097.py执行完成-----')

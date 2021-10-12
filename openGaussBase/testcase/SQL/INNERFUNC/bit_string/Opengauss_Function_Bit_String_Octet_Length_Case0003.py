"""
Copyright (c) 2021 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
'''

Case Type： 功能测试
Case Name： 位串作为octet_length函数的入参（参数为列）
Descption:

步骤 1.查看数据库状态，如果数据库没有启动则执行启动，如果已经启动则无操作
步骤 2.清理环境删除表防止新建失败
步骤 3.参数为列
'''
import os
import unittest
from yat.test import Node
from yat.test import macro
import sys

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH

logger = Logger()

class Bit_string_function(unittest.TestCase):

    def setUp(self):
        logger.info("------------------------Opengauss_BaseFunc_bit_string_octet_length_003开始执行--------------------------")
        logger.info("-----------查询数据库状态-----------")
        self.commonsh =  CommonSH('dbuser')
        self.common = Common()

    def test_bit_string_in_octet_length(self):

        sql_cmd = '''drop table if exists bit_type_t1;
                        CREATE TABLE bit_type_t1
                        (
                             BT_COL1 INTEGER,
                             BT_COL2 BIT(888),
                             BT_COL3 BIT VARYING(5)
                         ) ;
                         declare
                        begin
                            for i in 1..5000 loop
                                INSERT INTO bit_type_t1 VALUES(2, B'10'::bit(888), B'1011');
                            end loop;
                        end;
                        
            '''
        cmd1 = self.commonsh.execut_db_sql(sql_cmd)
        logger.info(cmd1)
        Normal_SqlMdg = self.commonsh.execut_db_sql("SELECT octet_length(BT_COL2) from bit_type_t1 where rownum < 10;")
        Normal_SqlMdg.splitlines()
        self.assertTrue(Normal_SqlMdg.count('111') == 9)
        self.commonsh.execut_db_sql(sql_cmd)
        Normal_SqlMdg1 = self.commonsh.execut_db_sql("SELECT octet_length(BT_COL3) from bit_type_t1 where rownum < 10;")
        Normal_SqlMdg1.splitlines()
        self.assertTrue(Normal_SqlMdg1.count('1') == 9)

    def tearDown(self):
        clear_sql = 'DROP table IF EXISTS bit_type_t1;'
        self.commonsh.execut_db_sql(clear_sql)
        logger.info('------------------------Opengauss_BaseFunc_bit_string_octet_length_003执行结束--------------------------')
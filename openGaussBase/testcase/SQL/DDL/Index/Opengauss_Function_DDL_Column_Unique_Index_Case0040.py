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
Case Type   : DDL
Case Name   : 多并发，创建列存表，同一索引列插入相同数据
Description :
    1.创建列存表
    2.开启两个会话，同时插入数据
    3.校验数据是否插入成功
    4.清理环境
Expect      :
    1.创建列存表成功
    2.开启两个会话，同时插入数据，其中一个会话插入失败
    3.校验数据，插入成功
    4.清理环境成功
History     : 
"""
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class DdlTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('Opengauss_Function_DDL_Column_Unique_Index_Case0040开始')
        self.constant = Constant()
        self.commonsh1 = CommonSH('PrimaryDbUser')
        self.commonsh2 = CommonSH('PrimaryDbUser')
        self.tb_name = 't_column_tab_0040'

    def test_unique_index(self):
        text1 = '-----step1.创建列存表; expect:列存表创建成功'
        self.log.info(text1)
        sql_cmd = self.commonsh1.execut_db_sql(
            f'drop table if exists {self.tb_name};'
            f'create table {self.tb_name}(id1 varchar,id2 int primary key)'
            f' with(orientation=column);')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_TABLE_SUCCESS, sql_cmd,
                      '执行失败:' + text1)

        text2 = '-----step2.开启两个会话，同时插入数据; expect:其中一个会话插入数据失败'
        self.log.info(text2)
        sql = f'''
        begin
        for i in 1..100 loop
        insert into {self.tb_name} values('a',i);
        end loop;
        end;
        '''
        thread_1 = ComThread(self.commonsh1.execut_db_sql, args=(sql, ''))
        thread_1.setDaemon(True)
        thread_1.start()

        thread_2 = ComThread(self.commonsh2.execut_db_sql, args=(sql, ''))
        thread_2.setDaemon(True)
        thread_2.start()

        thread_1.join(30)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)

        thread_2.join(30)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)

        expect_msg = "ERROR:  duplicate key value violates unique constraint"
        result = msg_result_1 + msg_result_2
        self.assertEqual(result.count(expect_msg), 1, '执行失败:' + text2)
        self.assertEqual(result.count('ANONYMOUS BLOCK EXECUTE'), 1,
                         '执行失败:' + text2)

        text3 = '-----step3.校验数据是否插入成功; expect:100条数据插入成功'
        self.log.info(text3)
        sql_cmd = self.commonsh1.execut_db_sql(
            f'select count(*) from {self.tb_name};')
        self.log.info(sql_cmd)
        self.assertIn('100', sql_cmd, '执行失败:' + text3)

    def tearDown(self):
        text4 = '--step4.清理环境; expect:清理数据成功'
        self.log.info(text4)
        sql_cmd = self.commonsh1.execut_db_sql(f'drop table {self.tb_name};')
        self.log.info(sql_cmd)
        self.log.info('Opengauss_Function_DDL_Column_Unique_Index_Case0040结束')

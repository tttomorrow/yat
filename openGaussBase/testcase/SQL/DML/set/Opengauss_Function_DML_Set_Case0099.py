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
"""
Case Type   : analyze--analyze Multi-column
Case Name   : 使用analyze收集32列数据，收集多列统计信息成功
Description :
    1.创建表，列数超过32列；插入一行数据
    2.使用analyze收集32列数据;analyze条件verbose参数
    3.查询pg_stat_user_tables系统表
    4.恢复参数default_statistics_target默认值
    5.删除表
Expect      :
    1.建表成功且数据插入成功
    2.analyze语句执行成功；添加verbose参数，显示目前正在处理的表
    3.显示analyze时间等信息
    4.默认值显示100
    5.表删除成功
History     :
"""
import sys
import unittest

from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class SYSOPERATION(unittest.TestCase):
    def setUp(self):
        logger.info('------Opengauss_Function_DML_Set_Case0099开始执行------')

    def test_analyze(self):
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists test_1;
            create table test_1 (c_id int,c_name varchar(20),c_age int,
            c_sex varchar(20),c_height int,c_color varchar(20),c_id1 int,
            c_name1 varchar(20),c_age1 int,c_sex1 varchar(20),c_height1 int,
            c_color1 varchar(20),c_id2 int,c_name2 varchar(20),c_age2 int,
            c_sex2 varchar(20),c_height2 int,c_color2 varchar(20),c_id3 int,
            c_name3 varchar(20),c_age3 int,c_sex3 varchar(20),c_height3 int,
            c_color3 varchar(20),c_id4 int,c_name4 varchar(20),c_age4 int,
            c_sex4 varchar(20),c_height4 int,c_color4 varchar(20),c_id5 int,
            c_name5 varchar(20),c_age5 int,c_sex5 varchar(20),c_height5 int,
            c_color5 varchar(20),c_id6 int,c_name6 varchar(20),c_age6 int,
            c_sex6 varchar(20),c_height6 int,c_color6 varchar(20));
            insert into test_1 values(1,'a',25,'boy',170,'yellow',2,'b',24,
            'boy',171,'yellow1',3,'b',24,'boy',171,'yellow1',4,'b',24,'boy',
            171,'yellow1',5,'b',24,'boy',171,'yellow1',6,'b',24,'boy',171,
            'yellow1',7,'b',24,'boy',171,'yellow1');''')
        logger.info(sql_cmd1)
        self.assertIn(constant.TABLE_CREATE_SUCCESS, sql_cmd1)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd1)

        sql_cmd2 = commonsh.execut_db_sql('''
            analyze test_1((c_id1,c_name1,c_age1,c_sex1,c_height1,c_color1,
            c_id2,c_name2,c_age2,c_sex2,c_height2,c_color2,c_id3,c_name3,
            c_age3,c_sex3,c_height3,c_color3,c_id4,c_name4,c_age4,c_sex4,
            c_height4,c_color4,c_id5,c_name5,c_age5,c_sex5,c_height5,c_color5,
            c_id6,c_name6));
            analyze verbose test_1((c_id1,c_name1,c_age1,c_sex1,c_height1,
            c_color1,c_id2,c_name2,c_age2,c_sex2,c_height2,c_color2,c_id3,
            c_name3,c_age3,c_sex3,c_height3,c_color3,c_id4,c_name4,c_age4,
            c_sex4,c_height4,c_color4,c_id5,c_name5,c_age5,c_sex5,c_height5,
            c_color5,c_id6,c_name6)); ''')
        logger.info(sql_cmd2)
        self.assertIn(constant.ANALYZE_SUCCESS_MSG, sql_cmd2)

        sql_cmd3 = commonsh.execut_db_sql('''
            select relname,last_autovacuum,last_analyze 
            from pg_stat_user_tables where relname='test_1';
            set default_statistics_target to default;''')
        logger.info(sql_cmd3)
        self.assertIn('test_1', sql_cmd3)
        self.assertIn(constant.SET_SUCCESS_MSG, sql_cmd3)

    def tearDown(self):
        logger.info('----------this is teardown-------')
        sql_cmd4 = commonsh.execut_db_sql('''drop table test_1;''')
        logger.info(sql_cmd4)
        logger.info('------Opengauss_Function_DML_Set_Case0099执行结束------')

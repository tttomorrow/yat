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
'''
--  @testpoint:创建联合唯一约束，并定义其中一列是序列型
'''
import sys
import unittest

sys.path.append(sys.path[0] + "/../")
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH

logger = Logger()
commonsh = CommonSH('dbuser')
constant = Constant()


class Privategrant(unittest.TestCase):
    def setUp(self):
        logger.info('------------------------Opengauss_Function_DML_Upsert_Case0118开始执行-----------------------------')

    def test_sysadmin_user_permission(self):
        # 建表指定id列为唯一约束且name列为数组类型
        sql_cmd1 = commonsh.execut_db_sql(''' drop table if exists test_4;
                                     create table test_4(name char[]  ,id int unique ,address nvarchar2(50)) ;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_TABLE_SUCCESS, sql_cmd1)
        # 常规insert插入一条数据
        # 使用insert..update..EXCLUDED语句，原数据(array['c','d','a'],3,'tianjin1')更改为(array['c','d','a'],3,YUNNAN)并新增一条数据(array['c','d'],4,'dalian1')
        # 使用insert..update..EXCLUDED语句，两条数据主键均重复，更改后的数据为(array['c','d','e'],3,'YUNNAN1')和(array['c','d','g'],4,'DAQING')
        sql_cmd2 = commonsh.execut_db_sql('''insert into test_4 values(array['c','d','a'],3,'tianjin1');
        explain analyse insert into test_4 values(array['c','d','e'],3,'yunnan'),(array['c','d'],4,'dalian1') ON duplicate key update address=upper(EXCLUDED.address);
        explain analyze insert into test_4 values(array['c','d','e'],3,'yunnan1'),(array['c','d','g'],4,'daqing') ON duplicate key update address=upper(EXCLUDED.address),name=EXCLUDED.name;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)
       # 清理表数据
        sql_cmd3 = commonsh.execut_db_sql('''truncate test_4;''')
        logger.info(sql_cmd3)
        self.assertIn(constant.TRUNCATE_SUCCESS_MSG, sql_cmd3)
        # 常规insert插入一条数据
        sql_cmd4 = commonsh.execut_db_sql('''insert into test_4 values(array['c','d','a'],3,'tianjin1');
        explain analyze insert into test_4 values(array['c','d','e'],3,'yunnan1'),(array['c','d','g'],4,'daqing') ON  duplicate key update  address=char_length(excluded.address);
        explain analyze insert into test_4 values(array['c','d','e'],3,'yunnan1'),(array['c','d','g'],4,'daqing1') ON duplicate key update address=test_4.name;
        truncate test_4;''')
        logger.info(sql_cmd4)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd4)
        self.assertIn(constant.TRUNCATE_SUCCESS_MSG, sql_cmd4)
        # 使用insert..update..语句，update后跟values，数据更改为(array['c','d','e'],3,array['c','d','g'])
        sql_cmd5 = commonsh.execut_db_sql('''explain analyze insert into test_4 values(array['c','d','e'],3,'yunnan1'),(array['c','d','g'],3,'daqing1') ON duplicate key update address=values(name);''')
        logger.info(sql_cmd5)
        self.assertIn('QUERY PLAN', sql_cmd5)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd6 = commonsh.execut_db_sql(''' drop table test_4;''')
        logger.info(sql_cmd6)
        logger.info('------------------------Opengauss_Function_DML_Upsert_Case0118执行结束--------------------------')






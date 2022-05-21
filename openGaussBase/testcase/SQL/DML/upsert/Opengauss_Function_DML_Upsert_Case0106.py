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
        logger.info('------------------------Opengauss_Function_DML_Upsert_Case0106开始执行-----------------------------')

    def test_sysadmin_user_permission(self):
        # 建表
        sql_cmd1 = commonsh.execut_db_sql('''drop table if exists mykey_4g;
                                     create table mykey_4g(name nvarchar2(20)  ,id serial unique  ,address nvarchar2(50)) ;''')
        logger.info(sql_cmd1)
        self.assertIn(constant.CREATE_TABLE_SUCCESS, sql_cmd1)
        # 常规插入一条数据，插入数据('a',1,'xx')
        # 使用insert..update语句插入一条数据，主键重复，修改数据('a',1,'xx')为('a',1,'yy')
        # 使用insert..update语句插入一条数据,('a',2,'yy')
        # 使用insert..update..excluded语句，插入两条数据，唯一列都是default，新增两条数据
        # 使用insert..nothing语句，插入两条数据，唯一列都是default，新增两条数据
        # 使用insert..nothing语句，插入两条数据,主键列两行重复，直接返回

        sql_cmd2 = commonsh.execut_db_sql(''' insert into mykey_4g values('a',default,'xx');
                                        insert into mykey_4g values('a',1,'yy') ON DUPLICATE KEY UPDATE address='yy';
                                        insert into mykey_4g values('a',default,'yy') ON  DUPLICATE KEY UPDATE address='yy';
                                        insert into mykey_4g values('a',default,'zz'),('a',default,'xx') ON  DUPLICATE KEY UPDATE address=excluded.address;
                                        insert into mykey_4g values('a',default,'zz'),('a',default,'xx') ON  DUPLICATE KEY update nothing;
                                        insert into mykey_4g values('a',3,'zz'),('a',4,'xx') ON  DUPLICATE KEY update nothing;''')
        logger.info(sql_cmd2)
        self.assertIn(constant.INSERT_SUCCESS_MSG, sql_cmd2)

    # 清理环境
    def tearDown(self):
        logger.info('----------this is teardown-------')
        # 删除表
        sql_cmd3 = commonsh.execut_db_sql(''' drop table mykey_4g;''')
        logger.info(sql_cmd3)
        logger.info('------------------------Opengauss_Function_DML_Upsert_Case0106执行结束--------------------------')






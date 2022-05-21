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
Case Type   : 触发器函数
Case Name   : pg_get_triggerdef(oid) 描述：获取触发器的定义信息
Description :
    1.创建源表和触发表
    2.创建触发器函数
    3.创建触发器
    4.获取触发器的oid
    5.获取触发器的定义信息
    6.清理环境
Expect      :
    1.创建源表和触发表成功
    2.创建触发器函数成功
    3.创建触发器成功
    4.获取触发器的oid成功
    5.获取触发器的定义信息成功
    6.清理环境
History     : 
"""

import unittest
from yat.test import Node
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant

LOG = Logger()


class Tools(unittest.TestCase):
    def setUp(self):
        LOG.info('-Opengauss_Function_Innerfunc_Trigger_Func_Case0003开始-')
        self.dbuser_node = Node('dbuser')
        self.commonsh = CommonSH('dbuser')
        self.Constant = Constant()

    def test_func_sys_manage(self):
        LOG.info('---------步骤1.创建源表和触发表---------')
        sql_cmd = self.commonsh.execut_db_sql(f'''
            drop table if exists test_tb_trigger_001;
            drop table if exists test_tb_trigger_002;
            create table test_tb_trigger_001(id1 int, id2 int, id3 int);
            create table test_tb_trigger_002(id1 int, id2 int, id3 int);
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.Constant.TABLE_CREATE_SUCCESS, sql_cmd)

        LOG.info('---------步骤2.创建触发器函数---------')
        sql_cmd = self.commonsh.execut_db_sql(f'''
            create or replace function tri_truncate_func() returns trigger as
            \\$\\$
            declare
            begin
                truncate test_tb_trigger_002;
                return old;
            end
            \\$\\$ language plpgsql;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(self.Constant.CREATE_FUNCTION_SUCCESS_MSG, sql_cmd)

        LOG.info('---------步骤3.创建触发器---------')
        sql_cmd = self.commonsh.execut_db_sql(f'''
        create trigger truncate_trigger before \
        truncate on test_tb_trigger_001 execute procedure tri_truncate_func();
        ''')
        LOG.info(sql_cmd)
        self.assertIn(self.Constant.TRIGGER_CREATE_SUCCESS_MSG, sql_cmd)

        LOG.info('---------步骤4.获取触发器的oid---------')
        sql_cmd = self.commonsh.execut_db_sql(f'''
            select oid from pg_trigger where tgname='truncate_trigger';
            ''')
        LOG.info(sql_cmd)
        num1 = int(sql_cmd.split('\n')[2].strip())
        LOG.info(num1)
        self.assertTrue(num1 > 0)

        LOG.info('---------步骤5.获取触发器的定义信息---------')
        sql_cmd = self.commonsh.execut_db_sql(f'''
            select pg_get_triggerdef({num1}) from pg_trigger;
            ''')
        LOG.info(sql_cmd)
        self.assertIn(f' CREATE TRIGGER truncate_trigger BEFORE TRUNCATE'
                      f' ON test_tb_trigger_001 FOR EACH STATEMENT'
                      f' EXECUTE PROCEDURE tri_truncate_func()', sql_cmd)

    def tearDown(self):
        LOG.info('---------------步骤6.清理环境----------------')
        sql_cmd = self.commonsh.execut_db_sql(f'''
            drop table test_tb_trigger_001;
            drop table test_tb_trigger_002;
            drop function tri_truncate_func();
            ''')
        LOG.info(sql_cmd)
        LOG.info('-Opengauss_Function_Innerfunc_Trigger_Func_Case0003结束-')

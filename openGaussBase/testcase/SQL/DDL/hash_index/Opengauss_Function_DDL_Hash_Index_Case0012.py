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
Case Name   : 对表创建行访问控制策略，表字段创建hash索引
Description :
    1.创建测试库
    2.指定数据库下创建表和用户
    3.将表的读取权限赋予用户
    4.打开行访问控制策略开关并创建行访问控制策略
    5.当前用户执行select操作
    6.切换至{self.u_name}用户查询
    7.清理环境
Expect      :
    1.创建成功
    2.创建成功
    3.权限赋予用户成功
    4.打开行访问控制策略开关并创建行访问控制策略成功
    5.查询到表的所有记录
    6.select只能查询到role为{self.u_name}这一行数据且查询计划显示受行访问
    策略影响
    7.清理环境完成
History     :
"""


import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class DDL(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0012start-')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.tb_name = "t_hash_index_0012"
        self.id_name = "i_hash_index_0012"
        self.db_name = "db_hash_index_0012"
        self.policy_name = "po_hash_index_0012"
        self.u_name = "u_hash_index_0012"
        self.u_name_01 = "u_hash_index_0012_01"

    def test_hash_index(self):
        text = '---step1:创建测试库;expect:创建成功-------'
        self.log.info(text)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd,
                      '执行失败:' + text)

        text = '---step2:指定数据库下创建表和用户;expect:创建成功-------'
        self.log.info(text)
        sql_cmd = f'''drop user if exists {self.u_name};
            create user {self.u_name} password '{macro.COMMON_PASSWD}';
            drop user if exists {self.u_name_01};
            create user {self.u_name_01} password '{macro.COMMON_PASSWD}';
            drop table if exists t_hash_index_0012;
            create table {self.tb_name} (id int, role varchar(20), sex text);
            insert into {self.tb_name} values(1, '{self.u_name}', 'alice');
            insert into {self.tb_name} values(2, '{self.u_name_01}', 'bob');
            insert into {self.tb_name} values(3, 'peter', 'peter data');
            insert into {self.tb_name} select random()*10, random()*3, 'XXX' \
            from generate_series(1,5000);
            drop index if exists {self.id_name};
            create index {self.id_name} on {self.tb_name} using hash (id);'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS, sql_result,
                      '执行失败:' + text)

        text = '---step3:将表的读取权限赋予用户;expect:授予权限成功-------'
        self.log.info(text)
        sql_cmd = f'''grant select on {self.tb_name} to {self.u_name},\
            {self.u_name_01};'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, sql_result,
                      '执行失败:' + text)

        text = '---step4:打开行访问控制策略开关并创建行访问控制策略;' \
               'expect:授予权限成功-------'
        self.log.info(text)
        sql_cmd = f'''alter table {self.tb_name} enable row level security;
            create row level security policy {self.policy_name} on \
            {self.tb_name} using(role = current_user);'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.ALTER_TABLE_MSG, sql_result,
                      '执行失败:' + text)
        self.assertIn(
            self.constant.CREATE_ROW_LEVEL_SECURITY_POLICY_SUCCESS_MSG,
            sql_result, '执行失败:' + text)

        text = '--step5:当前用户执行select操作;expect:查询到表的所有数据--'
        self.log.info(text)
        sql_cmd = f'''select count(*) from {self.tb_name};
            explain select  count(*) from {self.tb_name} where id =1;'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        msg = sql_result.splitlines()
        self.log.info(msg)
        self.assertEqual('5003', sql_result.splitlines()[2].strip(),
                         '执行失败:' + text)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_result, '执行失败:' + text)

        text = f'--step6:切换至{self.u_name}用户查询;' \
               f'expect:select只能查询到role为{self.u_name}这一行数据且查询' \
               f'计划显示受行访问策略影响--'
        self.log.info(text)
        sql_cmd = f'''select * from {self.tb_name};
                    explain select count(*) from {self.tb_name} where id =1;'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               sql_type=f'-U {self.u_name} '
                                               f'-W {macro.COMMON_PASSWD}',
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn('1 | u_hash_index_0012 | alice', sql_result,
                      '执行失败:' + text)
        self.assertIn('Notice: This query is influenced by row level security'
                      ' feature', sql_result, '执行失败:' + text)
        self.assertIn('Bitmap Index Scan' or 'Index Scan',
                      sql_result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('--步骤7:清理环境--')
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            drop user if exists {self.u_name};
            drop user if exists {self.u_name_01};''')
        self.log.info(sql_cmd)
        self.log.info('-Opengauss_Function_DDL_Hash_Index_Case0012finish--')

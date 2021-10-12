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
Case Type   : 列存表支持主键、唯一索引
Case Name   : 修改列存表唯一索引，重建索引
Description :
    1、创建普通列存表、创建唯一索引;
    2、修改索引文件权限，使索引不可用;
    3、插入异常数据;
    4、重建索引;
    5、再次插入异常数据;
    6、清理环境;
Expect      :
    1、创建列存表成功，创建唯一索引成功;
    2、修改文件权限成功;
    3、插入数据失败;
    4、重建索引成功;
    5、插入数据失败，提示数据重复;
    6、清理环境成功;
History     :
"""

import unittest
from yat.test import Node
from yat.test import macro
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant

logger = Logger()
primary_sh = CommonSH('PrimaryDbUser')


class DdlTestCase(unittest.TestCase):
    def setUp(self):
        self.constant = Constant()
        self.user_node = Node('PrimaryDbUser')
        self.table = 'column_tab05'
        self.index = 'column_index05'
        logger.info("======SetUp:检查数据库状态是否正常======")
        status = primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_column_unique_index(self):
        logger.info("Opengauss_Function_DDL_Column_Unique_Index_Case0005开始执行")
        logger.info("======步骤1:创建普通列存表，创建唯一索引======")
        sql_cmd1 = f'''drop table if exists {self.table};
            create table {self.table}(id int) with(orientation=column);
            create unique index {self.index} on {self.table} using btree(id);
            '''
        logger.info(sql_cmd1)
        sql_res1 = primary_sh.execut_db_sql(sql_cmd1)
        logger.info(sql_res1)
        self.assertTrue(self.constant.CREATE_TABLE_SUCCESS in sql_res1
                        and self.constant.CREATE_INDEX_SUCCESS in sql_res1)

        logger.info("======步骤2:设置索引不可用======")
        sql_cmd2 = f"select oid from pg_class where relname='{self.index}';"
        logger.info(sql_cmd2)
        sql_res2 = primary_sh.execut_db_sql(sql_cmd2)
        logger.info(sql_res2)

        oid = sql_res2.splitlines()[2].strip()

        sql_cmd3 = f"""select pg_relation_filepath('{oid}'::regclass);"""
        logger.info(sql_cmd3)
        sql_res3 = primary_sh.execut_db_sql(sql_cmd3)
        logger.info(sql_res3)

        self.path = sql_res3.splitlines()[2].strip()

        shell = f'''chmod 000 {macro.DB_INSTANCE_PATH}/{self.path};
            ls -l {macro.DB_INSTANCE_PATH}/{self.path};'''
        logger.info(shell)
        shell_res = self.user_node.sh(shell).result()
        logger.info(shell_res)

        logger.info("======步骤3:插入异常数据======")
        sql_cmd4 = f'''insert into {self.table} values(1),(1);'''
        logger.info(sql_cmd4)
        sql_res4 = primary_sh.execut_db_sql(sql_cmd4)
        logger.info(sql_res4)
        self.assertTrue('Permission denied' in sql_res4)

        logger.info("======步骤4:重建索引======")
        sql_cmd5 = f'''alter index {self.index} rebuild;'''
        logger.info(sql_cmd5)
        sql_res5 = primary_sh.execut_db_sql(sql_cmd5)
        logger.info(sql_res5)
        self.assertTrue(self.constant.REINDEX_SUCCESS_MSG in sql_res5)

        logger.info("======步骤5:再次插入异常数据======")
        sql_cmd6 = f'''insert into {self.table} values(1),(1);'''
        logger.info(sql_cmd6)
        sql_res6 = primary_sh.execut_db_sql(sql_cmd6)
        logger.info(sql_res6)
        self.assertTrue(self.constant.unique_index_error_info in sql_res6)

    def tearDown(self):
        logger.info("======步驟6:清理环境======")
        shell = f'''chmod 700 {macro.DB_INSTANCE_PATH}/{self.path};
            ls -l {macro.DB_INSTANCE_PATH}/{self.path};'''
        logger.info(shell)
        shell_res = self.user_node.sh(shell).result()
        logger.info(shell_res)

        drop_cmd = f'''drop table {self.table} cascade;'''
        logger.info(drop_cmd)
        drop_res = primary_sh.execut_db_sql(drop_cmd)
        logger.info(drop_res)
        logger.info("Opengauss_Function_DDL_Column_Unique_Index_Case0005执行结束")

"""
Case Type   : 列存表支持主键、唯一索引
Case Name   : 创建列存普通表，插入数据，更新为其他数据，清空表数据，再次插入第一次+第二次数据
Description :
    1、创建普通列存表，字段1添加主键约束，字段2添加唯一约束;
    2、字段3创建唯一索引;
    3、插入数据，数据非空且唯一;
    4、更新表中数据为其他数据;
    5、清空数据，再次插入之前第一次+第二次数据;
    6、清理环境;
Expect      :
    1、创建普通列存表成功;
    2、创建唯一索引成功;
    3、插入数据成功;
    4、更新数据成功;
    5、插入数据成功;
    6、清理环境成功;
History     :
"""

import unittest
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant

logger = Logger()
primary_sh = CommonSH('PrimaryDbUser')


class DdlTestCase(unittest.TestCase):
    def setUp(self):
        self.constant = Constant()
        self.table = 'column_tab36'
        self.index = 'column_index36'
        logger.info("======SetUp:检查数据库状态是否正常======")
        status = primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

    def test_column_unique_index(self):
        logger.info("Opengauss_Function_DDL_Column_Unique_Index_Case0036开始执行")
        logger.info("======步骤1:创建普通列存表，添加主键约束和唯一约束======")
        logger.info("======步骤2:创建唯一索引======")
        sql_cmd1 = f'''drop table if exists {self.table};
            create table {self.table}(id1 int primary key,
            id2 int unique,id3 int) with(orientation=column);
            create unique index {self.index} on {self.table} using btree(id3);
            '''
        logger.info(sql_cmd1)
        sql_res1 = primary_sh.execut_db_sql(sql_cmd1)
        logger.info(sql_res1)
        self.assertTrue(self.constant.CREATE_TABLE_SUCCESS in sql_res1
                        and self.constant.CREATE_INDEX_SUCCESS in sql_res1)

        logger.info("======步骤3:插入数据，数据唯一且非空======")
        sql_cmd2 = f'''insert into {self.table} 
            values(generate_series(1,10000),generate_series(1,10000),
            generate_series(1,10000));'''
        logger.info(sql_cmd2)
        sql_res2 = primary_sh.execut_db_sql(sql_cmd2)
        logger.info(sql_res2)
        self.assertTrue(self.constant.INSERT_SUCCESS_MSG in sql_res2)

        logger.info("======步骤4:更新表中数据为其他唯一且非空数据======")
        sql_cmd3 = f'''update {self.table} set id1 = id1+10000;
            update {self.table} set id2 = id2+10000;
            update {self.table} set id3 = id3+10000;
            '''
        logger.info(sql_cmd3)
        sql_res3 = primary_sh.execut_db_sql(sql_cmd3)
        logger.info(sql_res3)
        self.assertTrue(self.constant.UPDATE_SUCCESS_MSG in sql_res3)

        logger.info("======步骤5:清空数据，再次插入之前已插入1+2次数据=====")
        sql_cmd4 = f'''truncate table {self.table};
            insert into {self.table} values(generate_series(1,20000),
            generate_series(1,20000),generate_series(1,20000));'''
        logger.info(sql_cmd4)
        sql_res4 = primary_sh.execut_db_sql(sql_cmd4)
        logger.info(sql_res4)
        self.assertTrue(self.constant.INSERT_SUCCESS_MSG in sql_res4)

    def tearDown(self):
        logger.info("======步驟6：清理环境======")
        drop_cmd = f'''drop table {self.table} cascade;'''
        logger.info(drop_cmd)
        drop_res = primary_sh.execut_db_sql(drop_cmd)
        logger.info(drop_res)
        logger.info("Opengauss_Function_DDLColumn_Unique_Index_Case0036执行结束")

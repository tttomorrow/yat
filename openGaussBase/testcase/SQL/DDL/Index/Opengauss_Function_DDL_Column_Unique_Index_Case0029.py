"""
Case Type   : 列存表支持主键、唯一索引
Case Name   : 开启delta表功能，指定阈值为1000，插入小于1000数据量，更新，清空数据，再次插入原始数据+更新数据
Description :
    1、开启列存delta表功能，重启数据库;
       gs_guc set -N all -D {dn1} -c "enable_delta_store = on"
    2、创建列存表，指定deltarow_threshold阈值为1000;
    3、创建唯一索引;
    4、插入小于1000数据，数据唯一且非空值;
    5、更新表中数据为其他唯一且非空数据;
    6、清空数据，再次插入原始数据+更新数据;
    7、清理环境;
Expect      :
    1、设置参数成功，重启数据库成功;
    2、创建列存表、指定阈值为10000成功;
    3、创建唯一索引成功;
    4、插入数据成功;
    5、更新数据成功;
    6、清空数据成功，再次插入数据成功;
    7、清理环境成功;
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
        self.table = 'column_tab29'
        self.index = 'column_index29'
        logger.info("======SetUp:检查数据库状态是否正常======")
        status = primary_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

        logger.info('======步骤1:检查参数，修改配置，并重启数据库======')
        self.config_item = "enable_delta_store=on"
        check_res = primary_sh.execut_db_sql(f'''show enable_delta_store;''')
        if 'on' != check_res.splitlines()[-2].strip():
            primary_sh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     self.config_item)
            primary_sh.restart_db_cluster()
            result = primary_sh.get_db_cluster_status()
            self.assertTrue("Degraded" in result or "Normal" in result)

        logger.info("======查看参数修改是否成功======")
        alter_res = primary_sh.execut_db_sql(f'''show enable_delta_store;''')
        logger.info(alter_res)

    def test_column_unique_index(self):
        logger.info("Opengauss_Function_DDL_Column_Unique_Index_Case0029开始执行")
        logger.info("======步骤2:创建列存表，指定deltarow_threshold阈值为1000======")
        logger.info("======步骤3:创建唯一索引======")
        sql_cmd1 = f'''drop table if exists {self.table};
            create table {self.table}(id int) 
            with(orientation=column,deltarow_threshold=1000);
            create unique index {self.index} on {self.table} using btree(id);
            '''
        logger.info(sql_cmd1)
        sql_res1 = primary_sh.execut_db_sql(sql_cmd1)
        logger.info(sql_res1)
        self.assertTrue(self.constant.CREATE_TABLE_SUCCESS in sql_res1
                        and self.constant.CREATE_INDEX_SUCCESS in sql_res1)

        logger.info("======步骤4:插入小于1000数据，数据唯一且非空======")
        sql_cmd2 = f'''insert into {self.table} 
            values(generate_series(1,999));'''
        logger.info(sql_cmd2)
        sql_res2 = primary_sh.execut_db_sql(sql_cmd2)
        logger.info(sql_res2)
        self.assertTrue(self.constant.INSERT_SUCCESS_MSG in sql_res2)

        logger.info("======步骤5:更新表中数据为其他唯一且非空数据======")
        sql_cmd3 = f'''update {self.table} set id=id+1000;'''
        logger.info(sql_cmd3)
        sql_res3 = primary_sh.execut_db_sql(sql_cmd3)
        logger.info(sql_res3)
        self.assertTrue(self.constant.UPDATE_SUCCESS_MSG in sql_res3)

        logger.info("======步骤6:清空表中数据，再次插入源表数据及更新数据======")
        sql_cmd4 = f'''truncate table {self.table};
            insert into {self.table} values(generate_series(1,1999));'''
        logger.info(sql_cmd4)
        sql_res4 = primary_sh.execut_db_sql(sql_cmd4)
        logger.info(sql_res4)
        self.assertTrue(self.constant.TRUNCATE_SUCCESS_MSG in sql_res4
                        and self.constant.INSERT_SUCCESS_MSG in sql_res4)

    def tearDown(self):
        logger.info("======步驟7:清理环境======")
        drop_cmd = f'''drop table {self.table} cascade;'''
        logger.info(drop_cmd)
        drop_res = primary_sh.execut_db_sql(drop_cmd)
        logger.info(drop_res)

        self.config_item = "enable_delta_store=off"
        recov_res = primary_sh.execut_db_sql(f'''show enable_delta_store;''')
        if 'off' != recov_res.splitlines()[-2].strip():
            primary_sh.execute_gsguc('set',
                                     self.constant.GSGUC_SUCCESS_MSG,
                                     self.config_item)
            primary_sh.restart_db_cluster()
            result = primary_sh.get_db_cluster_status()
            self.assertTrue("Degraded" in result or "Normal" in result)
        logger.info("Opengauss_Function_DDL_Column_Unique_Index_Case0029执行结束")

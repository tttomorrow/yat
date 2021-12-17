"""
Case Type   : 功能测试
Case Name   : 使用pg_tablespace_size(name)查询指定名称的表空间使用的磁盘空间。
Description : 验证表空间在插入数据前后占磁盘空间大小
Expect      :
    1. 创建两个表空间
    2. 修改表空间名
    4。创建分区表属于表空间
History     :
    1.创建成功
    2.修改名字不影响表空间大小
    3.创建表后表空间占磁盘空间变大
"""
import unittest
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Logger import Logger


class Function(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('''Opengauss_Function_Sysmanagement_Dbobject_Tsn_\
        Case0001开始''')
        self.commonsh = CommonSH('dbuser')

    def test_tablespace(self):
        sql_cmd0 = '''DROP TABLESPACE if exists ds_location1;
                    DROP TABLESPACE if exists ds_location4;
                    DROP TABLESPACE if exists ds_location5;
                    DROP TABLE if exists customer_address'''
        self.commonsh.execut_db_sql(sql_cmd0)

        sql_cmd1 = '''CREATE TABLESPACE ds_location1 \
            RELATIVE LOCATION 'tablespace/tablespace_1';
            select pg_tablespace_size(a.oid) from pg_tablespace a \
            where a.spcname = 'ds_location1';'''
        msg1 = self.commonsh.execut_db_sql(sql_cmd1)
        self.log.info(msg1)
        msg1_list = msg1.splitlines()
        self.assertTrue(msg1.find("CREATE TABLESPACE") > -1)
        self.assertTrue(int(msg1_list[3]) > 0)

        sql_cmd2 = '''CREATE TABLESPACE  ds_location4 RELATIVE \
            LOCATION 'tablespace/tablespace_4';
            select pg_tablespace_size('ds_location4');'''
        msg2 = self.commonsh.execut_db_sql(sql_cmd2)
        self.log.info(msg2)
        msg2_list = msg2.splitlines()
        self.assertTrue(msg2.find("CREATE TABLESPACE") > -1)

        sql_cmd3 = '''ALTER TABLESPACE ds_location1 RENAME TO ds_location5;
            select pg_tablespace_size('ds_location5');
            '''
        msg3 = self.commonsh.execut_db_sql(sql_cmd3)
        self.log.info(msg3)
        msg3_list = msg3.splitlines()
        self.assertTrue(msg3.find("ALTER TABLESPACE") > -1)
        sql_cmd4 = '''CREATE TABLE customer_address(id1 int,id2 int) TABLESPACE\
            ds_location4 PARTITION BY RANGE (id1) (PARTITION P1 VALUES \
            LESS THAN(5000),PARTITION P8 VALUES LESS THAN(MAXVALUE) \
            TABLESPACE  ds_location5);
            '''
        msg4 = self.commonsh.execut_db_sql(sql_cmd4)
        self.log.info(msg4)
        self.assertTrue(msg4.find("CREATE TABLE") > -1)
        sql_cmd5 = '''select pg_tablespace_size('ds_location4');'''
        msg5 = self.commonsh.execut_db_sql(sql_cmd5)
        self.log.info(msg5)
        msg5_list = msg5.splitlines()
        self.assertTrue(int(msg5_list[2]) > int(msg2_list[3]))
        sql_cmd6 = '''select pg_tablespace_size('ds_location5');'''
        msg6 = self.commonsh.execut_db_sql(sql_cmd6)
        self.log.info(msg6)
        msg6_list = msg6.splitlines()
        self.assertTrue(int(msg6_list[2]) > int(msg3_list[3]))

    def tearDown(self):
        sql_cmd7 = '''drop table customer_address;'''
        msg7 = self.commonsh.execut_db_sql(sql_cmd7)
        self.log.info(msg7)
        self.assertTrue(msg7.find("DROP TABLE") > -1)
        sql_cmd8 = '''DROP TABLESPACE ds_location4;'''
        msg8 = self.commonsh.execut_db_sql(sql_cmd8)
        self.log.info(msg8)
        self.assertTrue(msg8.find("DROP TABLESPACE") > -1)
        sql_cmd9 = '''DROP TABLESPACE ds_location5;'''
        msg9 = self.commonsh.execut_db_sql(sql_cmd9)
        self.log.info(msg9)
        self.assertTrue(msg9.find("DROP TABLESPACE") > -1)
        self.log.info('''Opengauss_Function_Sysmanagement_Dbobject_Tsn_\
        Case0001结束''')
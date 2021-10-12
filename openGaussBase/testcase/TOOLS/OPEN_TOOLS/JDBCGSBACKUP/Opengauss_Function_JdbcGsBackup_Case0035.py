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
Case Type   : openGauss-tools-backup
Case Name   :  JdbcGsBackup -m xx，导出/导入指定数据库下的行存分区表
Description :
        1.创建数据库
        2.指定数据库下建范围分区表，间隔分区表，哈希分区表，列表分区
        3.修改信任方式为sha256
        4.导出
        5.删表后执行导入
        6.查询导入的表数据及结构
        7.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.修改成功
        4.导出成功
        5.导入成功
        6.导入表为分区表且数据正确
        7.清理环境完成
History     :
"""
import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class ToolsBackup(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0035start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_zh')
        self.db_name = "gs_db03"
        self.user = "us_03"
        self.tb_name = "range_t"
        self.log.info('---备份pg_hba.conf文件---')
        cmd = f"cp {os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}  " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')}"
        self.log.info(cmd)
        msg = self.Primary_Node.sh(cmd).result()
        self.log.info(msg)

    def test_tools_backup(self):
        self.log.info('---创建工具所在目录---')
        mkdir_cmd = f'''if [ ! -d "{self.package}" ]
                        then
                            mkdir -p {self.package}
                        fi'''
        self.log.info(mkdir_cmd)
        result = self.Primary_Node.sh(mkdir_cmd).result()
        self.log.info(result)
        self.assertEqual(result, '')
        self.log.info('---获取openGauss-tools-backup工具包---')
        sql_cmd = f'''wget -P {self.package} {macro.PACKAGE_URL}; '''
        self.log.info(sql_cmd)
        result = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(result)
        self.assertIn(f"‘{self.package}/openGauss-tools-backup.tar.gz’ saved"
                      , result)
        self.log.info('---解压工具包---')
        sql_cmd = f'''cd {self.package};
            tar -zxvf openGauss-tools-backup.tar.gz; '''
        self.log.info(sql_cmd)
        result = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(result)

        self.log.info('-----创建数据库----')
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            create database {self.db_name};''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS, sql_cmd)
        self.log.info('--创建测试用户和行存范围分区表---')
        sql_cmd = f'''drop user if exists {self.user};
            create user {self.user} with sysadmin \
            password '{macro.COMMON_PASSWD}';
            drop table if exists {self.tb_name};
            create table {self.tb_name}(
            field1   integer,
            field2   bigint,
            field3   real,
            field4   decimal(10,2),
            field5   number(38),
            field6   char(10),
            field7   varchar(2000),
            field8   varchar2(20),
            field9   CLOB,
            field10  BLOB,
            field11  varchar2(1024),
            field12 date,
            field13 timestamp,
            field14 INTERVAL DAY(7) TO SECOND(4),
            field15 timestamp with time zone,
            field16 timestamp,
            field17 boolean,
            field18  varchar(1024),
            field19  raw(1027)
            )partition by range(field12)
              (
            partition part01 values less than \
            (TO_DATE('2003-07-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part02 values less than \
            (TO_DATE('2005-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part03 values less than \
            (TO_DATE('2008-09-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part04 values less than \
            (TO_DATE('2009-07-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part05 values less than \
            (TO_DATE('2010-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part06 values less than \
            (TO_DATE('2012-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part07 values less than \
            (TO_DATE('2014-06-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part08 values less than \
            (TO_DATE('2015-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part09 values less than \
            (TO_DATE('2016-08-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part10 values less than \
            (TO_DATE('2017-05-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part11 values less than \
            (TO_DATE('2018-09-1 00:00:00','yyyy-mm-dd hh24:mi:ss')),
            partition part12 values less than \
            (TO_DATE('2019-09-1 00:00:00','yyyy-mm-dd hh24:mi:ss'))
             );
             declare
            i int:=0;
            begin
              loop
                i:=i+1;
            insert into {self.tb_name} \
            '简自豪',lpad('345abc',50,'abc'),'151515',null,\
            '2010-09-11 00:00:00','2012-11-11 00:00:00',interval '2' day,\
            '2016-12-11 00:00:00', '2011-12-11 00:00:00','true',null,null);
            exit when i= 1000;
              end loop;
              raise info'111';
            end;'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_result)
        self.log.info('--创建间隔分区表---')
        sql_cmd = f'''drop table if exists interval_range035;
            CREATE TABLE interval_range035
            (prod_id NUMBER(6),
             cust_id NUMBER,
             time_id DATE,
             channel_id CHAR(1),
             promo_id NUMBER(6),
             quantity_sold NUMBER(3),
             amount_sold NUMBER(10,2)
            )
            PARTITION BY RANGE (time_id)
            INTERVAL('1 day')
            ( PARTITION p1 VALUES LESS THAN ('2019-02-01 00:00:00'),
              PARTITION p2 VALUES LESS THAN ('2019-02-02 00:00:00')
            );
            INSERT INTO interval_range035 VALUES\
            (1, 12, '2019-01-10 00:00:00', 'a', 1, 1, 1);
            INSERT INTO interval_range035 VALUES\
            (1, 12, '2019-02-01 00:00:00', 'a', 1, 1, 1);
            INSERT INTO interval_range035 VALUES\
            (1, 12, '2019-02-05 00:00:00', 'a', 1, 1, 1);'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result)
        self.log.info('--创建哈希分区表---')
        sql_cmd = f'''drop tablespace if exists jdbcpgbackup_tabspace01;
            drop tablespace if exists jdbcpgbackup_tabspace02;
            drop tablespace if exists jdbcpgbackup_tabspace03;
            create tablespace jdbcpgbackup_tabspace01 relative \
            location 'tablespace/jdbcpgbackup_tabspace01';
            create tablespace jdbcpgbackup_tabspace02 relative \
            location 'tablespace/jdbcpgbackup_tabspace02';
            create tablespace jdbcpgbackup_tabspace03 relative \
            location 'tablespace/jdbcpgbackup_tabspace03';
            drop table if exists partition_hash_tab;
            create table partition_hash_tab(p_id int,p_name varchar,p_age int)
            partition by hash(p_id)
            (partition part_1 tablespace jdbcpgbackup_tabspace01,
             partition part_2 tablespace jdbcpgbackup_tabspace02,
             partition part_3 tablespace jdbcpgbackup_tabspace03);
             create or replace procedure insert_partition_hash()
                as
                insert_str varchar;
                begin
                    for i in 0..5 loop
                        insert_str = 'insert into partition_hash_tab \
                        values(10),(20),(30);';
                        execute immediate insert_str;
                    end loop;
                end;
                call insert_partition_hash();'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result)
        sql_cmd = '''drop tablespace if exists part_tabspace;
            create tablespace part_tabspace relative location \
            'tablespace/part_tablespace';
            drop table if exists partition_list_tab01;
            create table partition_list_tab01(p_id int,p_name varchar,\
            p_age int)tablespace part_tabspace
            partition by list(p_id)
            (partition part_1 values(10),
             partition part_2 values(20),
             partition part_3 values(30));'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result)

        self.log.info('---修改信任方式为sha256---')
        cmd = f"grep -nr '127.0.0.1/32' " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}"
        self.log.info(cmd)
        line = self.Primary_Node.sh(
            cmd).result().splitlines()[0].split(':')[0]
        self.log.info(line)
        cmd = f'sed -i "{str(int(line)+1)} ihost   all     all ' \
              f'{self.Primary_Node.db_host}/32   sha256" ' \
              f'{os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")}; ' \
              f'cat {os.path.join(macro.DB_INSTANCE_PATH, "pg_hba.conf")};'
        self.log.info(cmd)
        result = self.Primary_Node.sh(cmd).result()
        self.log.info(result)

        self.log.info('---导出--')
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m dump \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s public '''
        self.log.info(sql_cmd)
        msg = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.jdbcgsbackup_success, msg)
        self.assertNotIn(self.constant.jdbcgsbackup_failed[0] and
                         self.constant.jdbcgsbackup_failed[1] and
                         self.constant.jdbcgsbackup_failed[2], msg)
        self.log.info('---删表后执行导入--')
        sql_cmd = f'''drop table if exists {self.tb_name} cascade;
            drop table if exists interval_range035;
            drop table if exists partition_hash_tab;
            drop table if exists partition_list_tab01;'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.log.info('---导入--')
        sql_cmd = f'''cd {self.package}/openGauss-tools-backup;\
            java -jar openGauss-tools-backup.jar \
            -m restore \
            -d {self.db_name} \
            -h {self.Primary_Node.db_host} \
            -p {self.Primary_Node.db_port} \
            -U {self.user} \
            -P {macro.COMMON_PASSWD} \
            -s public \
            -n public'''
        self.log.info(sql_cmd)
        msg = self.Primary_Node.sh(sql_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.jdbcgsbackup_success, msg)
        self.assertNotIn(self.constant.jdbcgsbackup_failed[0] and
                         self.constant.jdbcgsbackup_failed[1] and
                         self.constant.jdbcgsbackup_failed[2], msg)
        self.log.info('---查询导入表数据--')
        sql_cmd_list = [f'select count(*) from {self.tb_name}',
                        'select count(*) from interval_range035',
                        'select count(*) from partition_hash_tab',
                        'select count(*) from partition_list_tab01']
        sql_result = ''
        for cmd in sql_cmd_list:
            sql_result += self.pri_sh.execut_db_sql(sql=cmd,
                                                    dbname=f'{self.db_name}')
            self.log.info(sql_result)
        self.assertIn('1000' and '3' and '0', sql_result)
        self.log.info('---查询表结构--')
        sql_cmd_list = [f'\d+ {self.tb_name}', '\d+ interval_range035',
                        '\d+ partition_hash_tab',
                        '\d+ partition_list_tab01']
        sql_result = ''
        for cmd in sql_cmd_list:
            sql_result += self.pri_sh.execut_db_sql(sql=cmd,
                                                    dbname=f'{self.db_name}')
            self.log.info(sql_result)
        self.assertIn('Range partition by(field12)' and
                      'Interval partition by(time_id)'
                      and 'Hash partition by(p_id)' and
                      'List partition by(p_id)', sql_result)

    def tearDown(self):
        self.log.info('---清理环境---')
        sql_cmd = f'''rm -rf {self.package};'''
        self.log.info(sql_cmd)
        result = self.Root_Node.sh(sql_cmd).result()
        self.log.info(result)
        cmd = f"rm -rf " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};" \
              f"mv " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf_t_bak')} " \
              f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')}"
        self.log.info(cmd)
        self.Primary_Node.sh(cmd)
        sql_cmd = self.pri_sh.execut_db_sql(f'''drop database if exists \
            {self.db_name};
            drop user if exists {self.user} cascade;
            drop tablespace if exists part_tabspace;
            drop tablespace if exists jdbcpgbackup_tabspace01;
            drop tablespace if exists jdbcpgbackup_tabspace02;
            drop tablespace if exists jdbcpgbackup_tabspace03;''')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0035finish---')

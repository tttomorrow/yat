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
Case Type   : openGauss-tools-backup
Case Name   :  JdbcGsBackup -m xx，导出/导入指定数据库下的列存表
              （覆盖基本常用数据类型）
Description :
        1.创建数据库
        2.指定数据库下建列存表，建用户
        3.依次创建btree索引，gin索引，psort索引；创建视图
        4.修改信任方式为sha256
        5.导出指定数据库
        6.删表后执行导入
        7.查询导入的表数据；视图；索引信息
        8.清理环境
Expect      :
        1.创建成功
        2.创建成功
        3.创建成功
        4.修改成功
        5.导出成功
        6.导入成功
        7.表数据，视图数据导入成功且数据正确；索引导入成功
        8.清理环境完成
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
            '---Opengauss_Function_JdbcGsBackup_Case0033start---')
        self.constant = Constant()
        self.DB_ENV_PATH = macro.DB_ENV_PATH
        self.Primary_Node = Node('PrimaryDbUser')
        self.Root_Node = Node('PrimaryRoot')
        self.package = os.path.join(
            os.path.dirname(macro.DB_INSTANCE_PATH), 'package_zh')
        self.db_name = "gs_db03"
        self.user = "us_03"
        self.tb_name = "t_03"
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
        self.log.info('--创建测试用户和列存表---')
        sql_cmd = f'''drop user if exists {self.user};
            create user {self.user} with sysadmin \
            password '{macro.COMMON_PASSWD}';
            drop table if exists {self.tb_name};
            create table {self.tb_name}
            (
            col_tinyint tinyint ,
            col_smallint smallint ,
            col_integer integer,
            col_int int,
            col_binary_integer binary_integer,
            col_bigint bigint,
            col_real real,
            col_float4 float4,
            col_double_precision double precision,
            col_float8 float8,
            col_float float,
            col_float1 float(38),
            col_binary_double binary_double,
            col_char char,
            col_char1 char(50),
            col_character character,
            col_character1 character(50),
            col_varchar varchar,
            col_varchar1 varchar(50),
            col_character_varying character varying(50),
            col_clob clob,
            col_text text,
            col_bytea bytea,
            col_date date,
            col_time time,
            col_time1 time(6),
            col_time2 time without time zone,
            col_time3 time(6) without time zone,
            col_time4 time with time zone,
            col_time5 time(6) with time zone,
            col_timestamp timestamp,
            col_timestamp1 timestamp(6),
            col_timestamp2 timestamp without time zone,
            col_timestamp3 timestamp(6) without time zone,
            col_timestamp4 timestamp with time zone,
            col_timestamp5 timestamp(6) with time zone,
            col_serial serial,
            col_smallserial smallserial,
            col_bigserial bigserial
            )with(ORIENTATION=column);
            insert into {self.tb_name} (col_tinyint,col_smallint,
            col_integer,col_int,col_binary_integer,col_bigint,col_real,\
            col_float4,col_double_precision,
            col_float8,col_float,col_float1,col_binary_double,col_char,\
            col_char1,col_character,
            col_character1,col_varchar,col_varchar1,col_character_varying,\
            col_clob,col_text,
            col_bytea,col_date,col_time,col_time1,col_time2,col_time3,\
            col_time4,col_time5,col_timestamp,col_timestamp1,col_timestamp2,\
            col_timestamp3,col_timestamp4,col_timestamp5) \
            values (34,35,36,37,38,39,37.74,75.48,113.22,\
            150.96,188.7,226.44,264.18,'3',
            'wxwhlayyawajbcqzhrctszhddqrwkyzjdwbygz3','h',\
            'V_character_50_length34','V_varchar34',
            'V_varchar_5034','V_character_varying34','V_clob34','V_text34',\
            '21:21:36','22:22:37','21:21:38-08', '22:22:39+08',\
            '1034-04-22 00:00:00','1035-04-22 pst','1036-04-22 21:22:23',\
            '1037-04-22 21:22:23.333333','1038-04-22 pst','1039-04-22 pst');'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_result)
        self.log.info('--创建btree索引、gin索引、psort索引和视图---')
        sql_cmd = f'''drop index if exists jdbcpgbackup_index1;
            create  index jdbcpgbackup_index1 ON {self.tb_name} using \
            btree(col_tinyint);
            drop table if exists cgin_create_test;
            create table cgin_create_test(a int, b text) with \
            (orientation = column);
            drop index if exists cgin_test;
            create index cgin_test on cgin_create_test using \
            gin(to_tsvector('ngram', b));
            drop index if exists a_index;
            create index a_index on cgin_create_test(a);
            drop view if exists jdbcpgbackup_v033;
            create view jdbcpgbackup_v033 as select * from {self.tb_name};'''
        self.log.info(sql_cmd)
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn(self.constant.CREATE_INDEX_SUCCESS, sql_result)
        self.assertIn(self.constant.CREATE_VIEW_SUCCESS_MSG, sql_result)

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
        restart_msg = self.pri_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.pri_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

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
        drop table if exists cgin_create_test;'''
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
        self.log.info('---查询导入表数据以及视图数据--')
        sql_cmd_list = [f'select * from {self.tb_name}',
                        'select * from jdbcpgbackup_v033']
        for cmd in sql_cmd_list:
            sql_result = self.pri_sh.execut_db_sql(sql=cmd,
                                                   dbname=f'{self.db_name}')
            self.log.info(sql_result)
            self.assertIn('1 row', sql_result)
        self.log.info('---查询索引--')
        sql_cmd = f'''\d+ {self.tb_name}'''
        sql_result = self.pri_sh.execut_db_sql(sql=sql_cmd,
                                               dbname=f'{self.db_name}')
        self.log.info(sql_result)
        self.assertIn('"jdbcpgbackup_index1" cbtree', sql_result)

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
            drop user if exists {self.user} cascade;''')
        self.log.info(sql_cmd)
        self.log.info(
            '---Opengauss_Function_JdbcGsBackup_Case0033finish---')

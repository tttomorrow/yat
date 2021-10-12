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
Case Type   : 逻辑复制
Case Name   : 备机进行逻辑复制,验证解码数据类型
Description :
        1.修改wal_level为logical;enable_slot_log为on
        2.重启数据库
        3.主机pg_hba.conf文件中配置逻辑复制的用户白名单
        4.主机创建逻辑复制槽
        5.主机上查询逻辑复制槽
        6.备机创建解码文件
        7.备机执行逻辑复制槽流式解码
        8.创建表(覆盖基本数据类型)并进行DML操作
        9.备机查看解码文件
        10.停止解码
        11.主机删除逻辑复制槽
        12.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.重启数据库成功
        3.pg_hba.conf 配置逻辑复制的用户白名单成功
        4.主机创建逻辑复制槽成功
        5.显示slot_test010复制槽信息
        6.备机创建解码文件成功
        7.屏幕输出备机逻辑复制槽流式解码过程
        8.创建表(无主键)并进行DML操作成功
        9.解码成功，解码文件update和delete操作不会记录列的旧值(具体哪些数据类型
        不支持，未明确)
        10.停止解码成功
        11.删除成功
        12.清理环境完成
History     :
"""
import os
import time
import unittest
from testcase.utils.ComThread import ComThread

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Primary_SH.get_node_num(),
                 '单机环境不执行')
class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '----Opengauss_Function_Logical_Replication_Case0010start-----')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.standby_node1 = Node('Standby1DbUser')
        self.root_node = Node('Standby1Root')
        self.decode_file = os.path.join(macro.DB_INSTANCE_PATH, 
                                        'logical10.txt')

    def test_standby_logical(self):
        self.log.info('--步骤1:修改wal_level为logical;enable_slot_log为on--')
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'wal_level =logical',
                                           node_name='all',
                                           single=False)
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Primary_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'enable_slot_log =on',
                                           node_name='all',
                                           single=False)
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        self.log.info('--步骤2:重启数据库--')
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('--步骤3:配置逻辑复制的用户--')
        sql_cmd = Primary_SH.execut_db_sql(f'''drop role if exists rep;
            create role rep with login password '{macro.COMMON_PASSWD}';
            alter role rep with replication sysadmin;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd)
        self.log.info('--步骤4:主机创建逻辑复制槽--')
        check_res = Primary_SH.execut_db_sql('select slot_name from '
                                             'pg_replication_slots;')
        self.log.info(check_res)
        if 'slot_test010' in check_res.split('\n')[-2].strip():
            del_cmd = Primary_SH.execut_db_sql("select * from "
                                               "pg_drop_replication_slot"
                                               "('slot_test010');")
            self.log.info(del_cmd)
        cre_cmd = Primary_SH.execut_db_sql("select * from "
                                           "pg_create_logical_replication_slot"
                                           "('slot_test010', 'mppdb_decoding')"
                                           ";")
        self.log.info(cre_cmd)
        self.log.info('--步骤5:查询复制槽--')
        query_cmd = Primary_SH.execut_db_sql('select slot_name,plugin from'
                                             ' pg_get_replication_slots();')
        self.log.info(query_cmd)
        self.assertIn('slot_test010', query_cmd)
        self.log.info('--步骤6:备机创建解码文件--')
        touch_cmd = f'''touch {self.decode_file};'''
        self.log.info(touch_cmd)
        result = self.standby_node.sh(touch_cmd).result()
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result)
        self.log.info('--步骤7:备机执行逻辑复制槽流式解码--')
        decode_cmd = f"pg_recvlogical " \
                     f"-d {self.standby_node.db_name} " \
                     f"-S slot_test010 " \
                     f"-p {self.standby_node.db_port} " \
                     f"--start " \
                     f"-f {self.decode_file} " \
                     f"-s 2 " \
                     f"-v " \
                     f"-P mppdb_decoding " \
                     f"-U rep"
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                           expect <<EOF
                           set timeout 300
                           spawn {decode_cmd}
                           expect "Password:"
                           send "{macro.COMMON_PASSWD}\\n"
                           expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        thread_2 = ComThread(self.standby_node.sh, args=(execute_cmd,))
        thread_2.setDaemon(True)
        thread_2.start()
        thread_2.join(10)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)
        self.log.info('步骤8:创建表(无主键)并进行DML操作')
        sql_cmd = Primary_SH.execut_db_sql('''drop table if exists \
        logicl_rep025;
        create table logicl_rep025
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
        col_bigserial bigserial);
        insert into logicl_rep025 (col_tinyint,col_smallint,col_integer,\
        col_int,col_binary_integer,col_bigint,col_real,col_float4,\
        col_double_precision,col_float8,col_float,col_float1,\
        col_binary_double,col_char,col_char1,col_character,col_character1,\
        col_varchar,col_varchar1,col_character_varying,col_clob,col_text,\
        col_bytea,col_date,col_time,col_time1,col_time2,col_time3,col_time4,\
        col_time5,col_timestamp,col_timestamp1,col_timestamp2,col_timestamp3,\
        col_timestamp4,col_timestamp5) \
        values (34,35,36,37,38,39,37.74,75.48,113.22,150.96,188.7,226.44,\
        264.18,'3','wxwhlayyawajbcqzhrctszhddqrwkyzjdwbygz3','h',\
        'V_character_50_length34','V_varchar34', 'V_varchar_5034',\
        '1034-01-08 00:00:00','19:41:34','20:41:35','21:21:36','22:22:37',\
        '21:21:38-08','22:22:39+08','1034-04-22 00:00:00','1035-04-22 pst',
        '1036-04-22 21:22:23','1037-04-22 21:22:23.333333','1038-04-22 pst',\
        '1039-04-22 pst');
        update logicl_rep025 set col_tinyint=0,col_smallint=0,col_integer=0,\
        col_int=0,col_binary_integer=0,col_bigint=0,col_real=0,col_float4=0.0,\
        col_double_precision=0.00,col_float8=0.00,col_float=0.00,\
        col_float1=0.00,col_binary_double=0.00,col_char='0',col_char1='000',\
        col_character='1',col_character1='0000',col_varchar='00003',\
        col_varchar1='00000',col_character_varying='00001',\
        col_date='2000-01-01 00:00:00',col_time='00:00:00',\
        col_time1='00:00:01',col_time2='00:00:02',\
        col_time3='00:00:03',col_time4='00:00:04',col_time5='00:00:05',\
        col_timestamp='2000-1-1',col_timestamp1='2000-1-1 pst',\
        col_timestamp2='2000-1-1 00:00:00',\
        col_timestamp3='2000-1-1 00:00:00.123',col_timestamp4='2000-1-4 pst',\
        col_timestamp5='2000-1-5 pst' where col_tinyint=34;
        delete from logicl_rep025;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd)
        time.sleep(3)
        self.log.info('步骤9:停止解码')
        stop_cmd = "ps -ef |  grep  pg_recvlogical | grep -v grep | " \
                   "awk '{{print $2}}' | xargs sudo kill -9"
        self.log.info(stop_cmd)
        result = self.root_node.sh(stop_cmd).result()
        self.log.info(result)
        time.sleep(3)
        self.log.info('步骤10:备机查看解码文件')
        cat_cmd = f"cat {self.decode_file}| grep 'old_keys_name';"
        self.log.info(cat_cmd)
        result = self.standby_node1.sh(cat_cmd).result()
        self.log.info(result)
        self.assertIn('"old_keys_name":[]', result)
        self.log.info('--步骤11:主机删除复制槽--')
        del_cmd = Primary_SH.execut_db_sql("select * from "
                                           "pg_drop_replication_slot"
                                           "('slot_test010');")
        self.log.info(del_cmd)
        self.assertIn('', del_cmd)

    def tearDown(self):
        self.log.info('--步骤12:清理环境--')
        sql_cmd = Primary_SH.execut_db_sql('''drop role if exists rep;
            drop table if exists logicl_rep025;''')
        self.log.info(sql_cmd)
        rm_cmd = f"rm -rf {self.decode_file};"
        result = self.standby_node.sh(rm_cmd).result()
        self.log.info(result)
        restore_cmd = Primary_SH.execute_gsguc('set',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               'wal_level=hot_standby')
        self.log.info(restore_cmd)
        restore_cmd = Primary_SH.execute_gsguc('set',
                                               self.constant.GSGUC_SUCCESS_MSG,
                                               'enable_slot_log=off')
        self.log.info(restore_cmd)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info(
            '--Opengauss_Function_Logical_Replication_Case0010finish----')

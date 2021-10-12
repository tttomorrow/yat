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
Case Name   : 创建逻辑复制槽后，建表执行DML操作(表无主键),备机进行逻辑复制操作
Description :
        1.修改wal_level为logical;enable_slot_log为on
        2.重启数据库
        3.主机pg_hba.conf文件中配置逻辑复制的用户白名单
        4.主机创建逻辑复制槽
        5.主机上查询逻辑复制槽
        6.备机创建解码文件
        7.备机执行逻辑复制槽流式解码
        8.创建表(无主键)并进行DML操作
        9.备机查看解码文件
        10.停止解码
        11.主机删除逻辑复制槽
        12.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.重启数据库成功
        3.pg_hba.conf 配置逻辑复制的用户白名单成功
        4.主机创建逻辑复制槽成功
        5.显示slot_test004复制槽信息
        6.备机创建解码文件成功
        7.屏幕输出备机逻辑复制槽流式解码过程
        8.创建表(无主键)并进行DML操作成功
        9.解码文件update和delete操作不会记录列的旧值
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
            '----Opengauss_Function_Logical_Replication_Case0004start-----')
        self.constant = Constant()
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.standby_node1 = Node('Standby1DbUser')
        self.root_node = Node('Standby1Root')
        self.decode_file = os.path.join(macro.DB_INSTANCE_PATH, 'logical4.txt')

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
        if 'slot_test004' in check_res.split('\n')[-2].strip():
            del_cmd = Primary_SH.execut_db_sql("select * from "
                                               "pg_drop_replication_slot"
                                               "('slot_test004');")
            self.log.info(del_cmd)
        cre_cmd = Primary_SH.execut_db_sql("select * from "
                                           "pg_create_logical_replication_slot"
                                           "('slot_test004', 'mppdb_decoding')"
                                           ";")
        self.log.info(cre_cmd)
        self.log.info('--步骤5:查询复制槽--')
        query_cmd = Primary_SH.execut_db_sql('select slot_name,plugin from'
                                             ' pg_get_replication_slots();')
        self.log.info(query_cmd)
        self.assertIn('slot_test004', query_cmd)
        self.log.info('--步骤6:备机创建解码文件--')
        touch_cmd = f'''touch {self.decode_file};'''
        self.log.info(touch_cmd)
        result = self.standby_node.sh(touch_cmd).result()
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result)
        self.log.info('--步骤7:备机执行逻辑复制槽流式解码--')
        decode_cmd = f"pg_recvlogical " \
                     f"-d {self.standby_node.db_name} " \
                     f"-S slot_test004 " \
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
        sql_cmd = Primary_SH.execut_db_sql('''drop table if exists test004;
            create table test004(c_1 integer,
            c_2 bigint,
            c_3 smallint,
            c_4 tinyint,
            c_5 serial,
            c_6 smallserial,
            c_7 bigserial,
            c_8 float,
            c_9 double precision,
            c_10 date,
            c_11 time without time zone,
            c_12 timestamp without time zone,
            c_13 char(10),
            c_14 varchar(20),
            c_15 text,
            c_16 blob,
            c_17 bytea);
            insert into test004 values(1,10,5,25,default,default,default,\
            1237.127,123456.1234,date '12-10-2010','21:21:21','2010-12-12',\
            '测试','测试工程师','西安',empty_blob(),E'\\xDEADBEEF');
            update test004 set c_15 = '数据库';
            delete from test004 where c_16 = empty_blob();''')
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
                                           "('slot_test004');")
        self.log.info(del_cmd)
        self.assertIn('', del_cmd)

    def tearDown(self):
        self.log.info('--步骤12:清理环境--')
        sql_cmd = Primary_SH.execut_db_sql('''drop role if exists rep;
            drop table if exists test004;''')
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
            '--Opengauss_Function_Logical_Replication_Case0004finish----')

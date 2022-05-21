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
Case Type   : 逻辑复制
Case Name   : 备机解码时，主机删除复制槽，解码报错，查询主备状态正常
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.配置逻辑复制的用户
        3.主机创建逻辑复制槽
        4.查询复制槽并创建解码文件
        5.备机进行解码
        6.创建表(无主键)并进行DML操作
        7.主机删除复制槽
        8.查询主备环境状态
        9.停止解码
        10.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.设置成功
        3.主机创建逻辑复制槽成功
        4.查询复制槽并创建解码文件成功
        5.显示解码过程
        6.创建成功
        7.删除复制槽成功，备机解码报错，复制槽不存在
        8.主备环境状态正常
        9.停止解码成功
        10.清理环境完成
History     :
"""
import os
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Pri_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(1 == Pri_SH.get_node_num(), '单机环境不执行')
class LogicalReplication(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(
            '-Opengauss_Function_Standby_Logical_Replication_Case0024start-')
        self.constant = Constant()
        self.com = Common()
        self.standby_sh = CommonSH('Standby1DbUser')
        self.primary_node = Node('PrimaryDbUser')
        self.primary_node1 = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.root_standby_node = Node('Standby1DbUser')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.de_file = os.path.join(macro.DB_INSTANCE_PATH, 'logical0024.txt')
        self.us_name = "u_logical_replication_0024"
        self.slot_name = "slot_logical_replication_0024"
        self.tb_name = "tb_logical_replication_0024"

    def test_standby(self):
        text = '--step1:修改wal_level为logical;enable_slot_log为on;' \
               'expect:修改成功--'
        self.log.info(text)
        mod_msg = Pri_SH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       'wal_level =logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Pri_SH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       'enable_slot_log =on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)

        text = '--step2:配置逻辑复制的用户;expect:设置成功--'
        self.log.info(text)
        sql_cmd = Pri_SH.execut_db_sql(f"drop role if exists {self.us_name};"
                                       f"create role {self.us_name} "
                                       f"with login password "
                                       f"'{macro.COMMON_PASSWD}';"
                                       f"alter role {self.us_name} "
                                       f"with replication sysadmin;")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)

        self.log.info('配置主机')
        mod_msg = f"sed -i '$a\local   replication  {self.us_name}   trust' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"127.0.0.1/32   trust' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host   replication  {self.us_name}   " \
                  f"::1/128    trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        self.log.info('配置备机')
        mod_msg = f"sed -i '$a\local   replication  {self.us_name}   trust' " \
                  f"{self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host  replication  {self.us_name}   " \
                  f"127.0.0.1/32   trust' {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host   replication  {self.us_name}   " \
                  f"::1/128    trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = self.standby_sh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.standby_sh.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step3:主机创建逻辑复制槽--;expect:创建成功'
        self.log.info(text)
        check_res = Pri_SH.execut_db_sql(f"select slot_name "
                                         "from pg_replication_slots;")
        self.log.info(check_res)
        if f'{self.slot_name}' in check_res.split('\n')[-2].strip():
            del_cmd = Pri_SH.execut_db_sql(f"select * from "
                                           f"pg_drop_replication_slot"
                                           f"('{self.slot_name}');")
            self.log.info(del_cmd)
        cre_cmd = Pri_SH.execut_db_sql(f"select * from "
                                       f"pg_create_logical_replication_slot"
                                       f"('{self.slot_name}', "
                                       f"'mppdb_decoding');")
        self.log.info(cre_cmd)

        text = '--step4:查询复制槽并创建解码文件--;' \
               'expect:复制槽存在且创建解码文件成功--'
        self.log.info(text)
        query_cmd = Pri_SH.execut_db_sql(f"select slot_name,plugin "
                                         "from pg_get_replication_slots();")
        self.log.info(query_cmd)
        self.assertIn(f'{self.slot_name}', query_cmd, '执行失败:' + text)
        touch_cmd = f'''touch {self.de_file};'''
        self.log.info(touch_cmd)
        result = self.standby_node.sh(touch_cmd).result()
        self.log.info(result)

        text = '--step5:备机执行逻辑复制槽流式解码;expect:解码成功--'
        self.log.info(text)
        decode_cmd = f"pg_recvlogical " \
                     f"-d postgres " \
                     f"-S {self.slot_name} " \
                     f"-p {self.standby_node.db_port} " \
                     f"--start " \
                     f"-f {self.de_file} " \
                     f"-s 2 " \
                     f"-v " \
                     f"-P mppdb_decoding " \
                     f"-U {self.us_name}"
        self.log.info(decode_cmd)
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                          expect <<EOF
                          set timeout 300
                          spawn {decode_cmd}
                          expect "Password:"
                          send "{macro.COMMON_PASSWD}\\n"
                          expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        thread_1 = ComThread(self.com.get_sh_result, args=(self.standby_node,
                                                           execute_cmd,))
        thread_1.setDaemon(True)
        thread_1.start()

        text = '--step6:创建表(无主键)并进行DML操作;expect:创建成功--'
        self.log.info(text)
        sql_cmd = Pri_SH.execut_db_sql(f'''drop table if exists {self.tb_name};
           create table {self.tb_name}(c_1 integer,
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
           insert into {self.tb_name} values(1,10,5,25,default,default,\
           default,1237.127,123456.1234,date '12-10-2010','21:21:21',\
           '2010-12-12', '测试','测试工程师','西安',empty_blob(),\
           E'\\xDEADBEEF');
           update {self.tb_name} set c_15 = '数据库';
           delete from {self.tb_name} where c_16 = empty_blob();''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        self.assertTrue('INSERT' in sql_cmd and 'UPDATE' in sql_cmd and
                        'DELETE' in sql_cmd, '执行失败:' + text)
        time.sleep(3)

        text = '--step7:主机删除复制槽;expect:删除成功--'
        self.log.info(text)
        del_cmd = Pri_SH.execut_db_sql(f"select * from "
                                       f"pg_drop_replication_slot"
                                       f"('{self.slot_name}');")
        self.log.info(del_cmd)
        self.assertIn('', del_cmd, '执行失败:' + text)

        text = '--step8:获取step5结果;expect:解码报错--'
        self.log.info(text)
        thread_1.join(10 * 60)
        msg_result_1 = thread_1.get_result()
        self.log.info(msg_result_1)
        self.assertIn(f'FATAL:  replication slot "{self.slot_name}" '
                      f'was not created', msg_result_1, '执行失败:' + text)

        text = '--step9:查询主备环境状态;expect:主备环境正常--'
        self.log.info(text)
        status_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_om -t status --detail;"
        self.log.info(status_cmd)
        status_msg = self.primary_node1.sh(status_cmd).result()
        self.log.info(status_msg)
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step10:停止解码;expect:停止解码成功--'
        self.log.info(text)
        stop_cmd = "ps -ef |  grep  pg_recvlogical | grep -v grep | " \
                   "awk '{{print $2}}' | xargs sudo kill -9"
        self.log.info(stop_cmd)
        result = self.root_standby_node.sh(stop_cmd).result()
        self.log.info(result)

    def tearDown(self):
        text = '--step11:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = Pri_SH.execut_db_sql(f"drop role if exists {self.us_name};")
        self.log.info(sql_cmd)
        rm_cmd = f"rm -rf {self.de_file};"
        self.log.info(rm_cmd)
        result = self.standby_node.sh(rm_cmd).result()
        self.log.info(result)
        del_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.primary_node.sh(del_msg).result()
        self.log.info(msg)
        del_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.standby_node.sh(del_msg).result()
        self.log.info(msg)
        restore_cmd = Pri_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'wal_level=hot_standby')
        self.log.info(restore_cmd)
        restore_cmd = Pri_SH.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           'enable_slot_log=off')
        self.log.info(restore_cmd)
        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)
        self.log.info(
            '--Opengauss_Function_Standby_Logical_Replication_Case0024finish-')

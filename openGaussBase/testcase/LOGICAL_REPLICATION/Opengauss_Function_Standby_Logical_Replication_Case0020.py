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
Case Type   : 备机支持逻辑复制
Case Name   : 主备对同一个逻辑复制槽解码
Description :
        1.修改参数wal_level为logical;enable_slot_log为on
        2.创建逻辑复制用户
        3.配置逻辑复制用户白名单
        4.创建逻辑复制槽
        5.查询逻辑复制槽
        6.主机执行逻辑复制槽解码
        7.备机解码同一个逻辑复制槽
        8.创建表(无主键)并进行DML操作
        9.获取step5&step6结果
        10.停止解码
        11.主机和备机查看解码文件
        12.清理环境
Expect      :
        1.修改成功
        2.创建成功
        3.设置成功
        4.创建成功
        5.显示${self.slot_name}复制槽信息
        6.显示解码过程
        7.解码报错，逻辑复制槽已经占用
        8.创建成功
        9.主机解码正常；备机解码报错
        10.停止解码成功
        11.主机解码DML操作正常;备机解码报错，但解码文件依然有解码信息(已知问题)
        12.清理环境完成
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
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.constant = Constant()
        self.com = Common()
        self.standby_sh = CommonSH('Standby1DbUser')
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.root_standby_node = Node('Standby1Root')
        self.root_pri_node = Node('PrimaryRoot')
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)
        self.parent_path = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.decode_file_01 = os.path.join(self.parent_path, 'decode01')
        self.decode_file_02 = os.path.join(self.parent_path, 'decode02')
        self.us_name = "u_logical_replication_0020"
        self.slot_name = "slot_logical_replication_0020"
        self.tb_name = "tb_logical_replication_0020"
        self.ha_port = str(int(self.primary_node.db_port) + 1)

    def test_standby(self):
        text = '--step1:修改参数wal_level为logical;enable_slot_log为on;' \
               'expect:修改成功--'
        self.log.info(text)
        mod_msg = Pri_SH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       'wal_level=logical')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)
        mod_msg = Pri_SH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       'enable_slot_log=on')
        self.log.info(mod_msg)
        self.assertTrue(mod_msg, '执行失败:' + text)
        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step2:创建逻辑复制用户;expect:创建成功--'
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

        text = '--step3:配置逻辑复制用户白名单;expect:设置成功--'
        self.log.info(text)
        guc_cmd = f'source {macro.DB_ENV_PATH};' \
                  f'gs_guc reload -N all -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "local   replication  {self.us_name}  trust"'
        self.log.info(guc_cmd)
        msg = self.primary_node.sh(guc_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, msg,
                      '执行失败:' + text)
        guc_cmd = f'source {macro.DB_ENV_PATH};' \
                  f'gs_guc reload -N all -D {macro.DB_INSTANCE_PATH}  ' \
                  f'-h  " host  replication  {self.us_name}  ' \
                  f'127.0.0.1/32   trust"'
        self.log.info(guc_cmd)
        msg = self.primary_node.sh(guc_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, msg,
                      '执行失败:' + text)
        guc_cmd = f'source {macro.DB_ENV_PATH};' \
                  f'gs_guc reload -N all -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "host   replication  {self.us_name}  ' \
                  f'::1/128    trust"'
        self.log.info(guc_cmd)
        msg = self.primary_node.sh(guc_cmd).result()
        self.log.info(msg)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, msg,
                      '执行失败:' + text)

        text = '--step4:创建逻辑复制槽;expect:创建成功--'
        self.log.info(text)
        check_res = Pri_SH.execut_db_sql('select slot_name from '
                                         'pg_replication_slots;')
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

        text = '--step5:查询复制槽;expect:显示{self.slot_name}复制槽信息--'
        self.log.info(text)
        query_cmd = Pri_SH.execut_db_sql("select slot_name,plugin from "
                                         "pg_get_replication_slots();")
        self.log.info(query_cmd)
        self.assertIn(f'{self.slot_name}', query_cmd, '执行失败:' + text)

        text = '--step6:主机执行逻辑复制槽流式解码;expect:解码成功--'
        self.log.info(text)
        decode_cmd = f"pg_recvlogical " \
                     f"-d {self.primary_node.db_name} " \
                     f"-S {self.slot_name} " \
                     f"-p {self.ha_port} " \
                     f"--start " \
                     f"-f {self.decode_file_01} " \
                     f"-s 2 " \
                     f"-v " \
                     f"-P mppdb_decoding " \
                     f"-U {self.us_name}"
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                          expect <<EOF
                          set timeout 300
                          spawn {decode_cmd}
                          expect "Password:"
                          send "{macro.COMMON_PASSWD}\\n"
                          expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        thread_1 = ComThread(self.com.get_sh_result, args=(self.primary_node,
                                                           execute_cmd,))
        thread_1.setDaemon(True)
        thread_1.start()
        time.sleep(3)

        text = '--step7:备机解码同一个逻辑复制槽;expect:解码报错--'
        self.log.info(text)
        decode_cmd = f"pg_recvlogical " \
                     f"-d {self.standby_node.db_name} " \
                     f"-S {self.slot_name} " \
                     f"-p {self.ha_port} " \
                     f"--start " \
                     f"-f {self.decode_file_02} " \
                     f"-s 2 " \
                     f"-v " \
                     f"-P mppdb_decoding " \
                     f"-U {self.us_name}"
        execute_cmd = f'''source {macro.DB_ENV_PATH}
                          expect <<EOF
                          set timeout 300
                          spawn {decode_cmd}
                          expect "Password:"
                          send "{macro.COMMON_PASSWD}\\n"
                          expect eof\n''' + '''EOF'''
        self.log.info(execute_cmd)
        thread_2 = ComThread(self.com.get_sh_result, args=(self.standby_node,
                                                           execute_cmd,))
        thread_2.setDaemon(True)
        thread_2.start()

        text = '--step8:创建表(无主键)并进行DML操作;expect:创建成功--'
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
        self.assertTrue('INSERT' in sql_cmd and 'UPDATE' in sql_cmd and
                        'DELETE' in sql_cmd, '执行失败:' + text)
        time.sleep(3)

        self.log.info('--step9:获取step5&step6结果;expect:主机解码正常;'
                      '备机解码报错--')
        thread_1.join(10 * 60)
        thread_1_result = thread_1.get_result()
        self.log.info(thread_1_result)
        self.assertIn('confirming write up', thread_1_result,
                      '执行失败:' + text)
        self.assertNotIn('FATAL' and 'ERROR', thread_1_result,
                         '执行失败:' + text)
        thread_2.join(10 * 60)
        thread_2_result = thread_2.get_result()
        self.log.info(thread_2_result)
        self.assertIn('could not connect to server: FATAL', thread_2_result,
                      '执行失败:' + text)

        time.sleep(3)
        text = '--step10:停止解码;expect:停止解码成功--'
        self.log.info(text)
        stop_cmd = "ps -ef |  grep  pg_recvlogical | grep -v grep | " \
                   "awk '{{print $2}}' | xargs sudo kill -9"
        self.log.info(stop_cmd)
        result = self.root_standby_node.sh(stop_cmd).result()
        self.log.info(result)
        time.sleep(3)
        stop_cmd = "ps -ef |  grep  pg_recvlogical | grep -v grep | " \
                   "awk '{{print $2}}' | xargs sudo kill -9"
        self.log.info(stop_cmd)
        result = self.root_pri_node.sh(stop_cmd).result()
        self.log.info(result)
        time.sleep(3)

        text = '--step11:主机和备机查看解码文件;expect:主机解码正常;' \
               '备机解码报错，但解码文件依然有解码信息--'
        self.log.info(text)
        cat_cmd = f"cat {self.decode_file_01};"
        self.log.info(cat_cmd)
        result = self.primary_node.sh(cat_cmd).result()
        self.log.info(result)
        self.assertIn('"old_keys_name":[]', result, '执行失败:' + text)
        cat_cmd = f"cat {self.decode_file_02};"
        self.log.info(cat_cmd)
        result = self.standby_node.sh(cat_cmd).result()
        self.log.info(result)
        self.assertIn('"old_keys_name":[]', result, '执行失败:' + text)

    def tearDown(self):
        text = '--step12:清理环境;expect:清理环境完成--'
        self.log.info(text)
        self.log.info('删除用户和表')
        drop_cmd1 = Pri_SH.execut_db_sql(f"drop role if exists "
                                         f"{self.us_name};")
        self.log.info(drop_cmd1)
        drop_cmd2 = Pri_SH.execut_db_sql(f"drop table if exists "
                                         f"{self.tb_name};")
        self.log.info(drop_cmd2)
        self.log.info('删除复制槽')
        drop_slot_cmd = Pri_SH.execut_db_sql(f"select * from "
                                             f"pg_drop_replication_slot"
                                             f"('{self.slot_name}');")
        self.log.info(drop_slot_cmd)
        self.log.info('删除解码文件')
        rm_cmd1 = f"rm -rf {self.decode_file_01};"
        self.log.info(rm_cmd1)
        result1 = self.primary_node.sh(rm_cmd1).result()
        self.log.info(result1)
        rm_cmd2 = f"rm -rf {self.decode_file_02};"
        self.log.info(rm_cmd2)
        result2 = self.standby_node.sh(rm_cmd2).result()
        self.log.info(result2)
        self.log.info('恢复pg_hba.conf文件')
        guc_cmd = f'source {macro.DB_ENV_PATH};' \
                  f'gs_guc reload -N all -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "local   replication  {self.us_name}"'
        self.log.info(guc_cmd)
        msg = self.primary_node.sh(guc_cmd).result()
        self.log.info(msg)
        guc_cmd = f'source {macro.DB_ENV_PATH};' \
                  f'gs_guc reload -N all -D {macro.DB_INSTANCE_PATH}  ' \
                  f'-h  " host  replication  {self.us_name}  ' \
                  f'127.0.0.1/32"'
        self.log.info(guc_cmd)
        msg = self.primary_node.sh(guc_cmd).result()
        self.log.info(msg)
        guc_cmd = f'source {macro.DB_ENV_PATH};' \
                  f'gs_guc reload -N all -D {macro.DB_INSTANCE_PATH} ' \
                  f'-h "host   replication  {self.us_name}  ::1/128"'
        self.log.info(guc_cmd)
        msg = self.primary_node.sh(guc_cmd).result()
        self.log.info(msg)
        self.log.info('恢复参数默认值')
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
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('断言teardown成功')
        self.assertIn(self.constant.DROP_ROLE_SUCCESS_MSG, drop_cmd1,
                      '执行失败:' + text)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_cmd2,
                      '执行失败:' + text)
        self.assertEqual('', drop_slot_cmd.splitlines()[2].strip(),
                         '执行失败:' + text)
        self.assertEqual(len(result1), 0, '执行失败:' + text)
        self.assertEqual(len(result2), 0,  '执行失败:' + text)
        self.assertIn(self.constant.GSGUC_SUCCESS_MSG, msg,
                      '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

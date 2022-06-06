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
Case Name   : 创建逻辑复制槽后，建表执行DML操作(表有主键),备机进行逻辑复制操作
Description :
        1.修改wal_level为logical;enable_slot_log为on
        2.重启数据库
        3.主机pg_hba.conf文件中配置逻辑复制的用户白名单
        4.主机创建逻辑复制槽
        5.主机上查询逻辑复制槽
        6.备机创建解码文件
        7.备机执行逻辑复制槽流式解码
        8.创建表(有主键)并进行DML操作
        9.备机查看解码文件
        10.停止解码
        11.主机删除逻辑复制槽
        12.清理环境
Expect      :
        1.修改参数wal_level为logical;enable_slot_log为on成功
        2.重启数据库成功
        3.pg_hba.conf 配置逻辑复制的用户白名单成功
        4.主机创建逻辑复制槽成功
        5.显示{self.slot_name}复制槽信息
        6.备机创建解码文件成功
        7.屏幕输出备机逻辑复制槽流式解码过程
        8.创建表(有主键)并进行DML操作成功
        9.解码文件update和delete操作均会记录主键列的旧值
        10.停止解码成功
        11.删除成功
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
        self.log.info(
            '----Opengauss_Function_Logical_Replication_Case0005start-----')
        self.constant = Constant()
        self.com = Common()
        self.primary_node = Node('PrimaryDbUser')
        self.standby_node = Node('Standby1DbUser')
        self.standby_node1 = Node('Standby1DbUser')
        self.root_node = Node('Standby1Root')
        self.decode_file = os.path.join(macro.DB_INSTANCE_PATH, 'logical5.txt')
        self.us_name = "us_logical_replication_case0005"
        self.slot_name = "slot_logical_replication_case0005"
        self.tb_name = "tb_logical_replication_case0005"
        self.pg_hba = os.path.join(macro.DB_INSTANCE_PATH,
                                   macro.PG_HBA_FILE_NAME)

    def test_standby_logical(self):
        text = '--step1:修改wal_level为logical;enable_slot_log为on;' \
               'expect:修改成功--'
        self.log.info(text)
        mod_msg = Pri_SH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       'wal_level =logical',
                                       node_name='all',
                                       single=False)
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)
        mod_msg = Pri_SH.execute_gsguc('set',
                                       self.constant.GSGUC_SUCCESS_MSG,
                                       'enable_slot_log =on',
                                       node_name='all',
                                       single=False)
        self.log.info(mod_msg)
        self.assertTrue(mod_msg)

        text = '--step2:重启数据库;expect:重启成功--'
        self.log.info(text)
        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step3:配置逻辑复制的用户;expect:配置成功--'
        self.log.info(text)
        sql_cmd = Pri_SH.execut_db_sql(f'''drop role if exists \
            {self.us_name};
            create role {self.us_name} with login password \
            '{macro.COMMON_PASSWD}';
            alter role {self.us_name} with replication sysadmin;''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        self.assertIn(self.constant.ALTER_ROLE_SUCCESS_MSG, sql_cmd,
                      '执行失败:' + text)
        self.log.info('--step2.1:配置主机--')
        mod_msg = f"sed -i '$a\local    replication     {self.us_name}      " \
                  f"trust'   {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host    replication     " \
                  f"{self.us_name}   127.0.0.1/32   trust'   {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host   replication     " \
                  f"{self.us_name}   ::1/128    trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.primary_node.sh(mod_msg).result()
        self.log.info(msg)
        self.log.info('--step2.2:配置备机--')
        mod_msg = f"sed -i '$a\local    replication     {self.us_name}     " \
                  f"trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host    replication     {self.us_name}   " \
                  f"127.0.0.1/32   trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        mod_msg = f"sed -i '$a\host    replication     {self.us_name}   " \
                  f"::1/128   trust'  {self.pg_hba}"
        self.log.info(mod_msg)
        msg = self.standby_node.sh(mod_msg).result()
        self.log.info(msg)
        restart_msg = Pri_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Pri_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败:' + text)

        text = '--step4:主机创建逻辑复制槽;expect:创建成功--'
        self.log.info(text)
        check_res = Pri_SH.execut_db_sql("select slot_name from "
                                         "pg_replication_slots;")
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

        text = '--step5:查询复制槽;expect:复制槽存在--'
        self.log.info(text)
        query_cmd = Pri_SH.execut_db_sql("select slot_name,plugin from "
                                         "pg_get_replication_slots();")
        self.log.info(query_cmd)
        self.assertIn(f'{self.slot_name}', query_cmd, '执行失败:' + text)

        text = '--step6:备机创建解码文件;expect:创建成功--'
        self.log.info(text)
        touch_cmd = f'''touch {self.decode_file};'''
        self.log.info(touch_cmd)
        result = self.standby_node.sh(touch_cmd).result()
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = '--step7:备机执行逻辑复制槽流式解码;expect:解码无报错--'
        self.log.info(text)
        decode_cmd = f"pg_recvlogical " \
                     f"-d {self.standby_node.db_name} " \
                     f"-S {self.slot_name} " \
                     f"-p {self.standby_node.db_port} " \
                     f"--start " \
                     f"-f {self.decode_file} " \
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
        thread_2.join(10)
        msg_result_2 = thread_2.get_result()
        self.log.info(msg_result_2)

        text = '--step7:创建表(无主键)并进行DML操作;expect:创建成功--'
        self.log.info(text)
        sql_cmd = Pri_SH.execut_db_sql(f'''drop table if exists {self.tb_name};
            create table {self.tb_name}(c_1 integer primary key,
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
            '2010-12-12','测试','测试工程师','西安',\
            empty_blob(),E'\\xDEADBEEF');
            UPDATE {self.tb_name} SET c_1 = 666;
            UPDATE {self.tb_name} SET c_15 = '陕西';
            delete from {self.tb_name} where c_16 = empty_blob();''')
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败:' + text)
        time.sleep(3)

        text = '--step9:停止解码;expect:停止解码成功--'
        self.log.info(text)
        stop_cmd = "ps -ef |  grep  pg_recvlogical | grep -v grep | " \
                   "awk '{{print $2}}' | xargs sudo kill -9"
        self.log.info(stop_cmd)
        result = self.root_node.sh(stop_cmd).result()
        self.log.info(result)
        time.sleep(3)

        text = '-step10:备机查看解码文件;expect:update和delete操作会记录旧值-'
        self.log.info(text)
        cat_cmd = f"cat {self.decode_file}| grep 'old_keys_name';"
        self.log.info(cat_cmd)
        res = self.standby_node1.sh(cat_cmd).result()
        self.log.info(res)
        self.assertIn('"old_keys_name":["c_1"],"old_keys_type":["integer"],'
                      '"old_keys_val":["1"]', res, '执行失败:' + text)
        self.assertIn('"old_keys_name":["c_1"],"old_keys_type":["integer"],'
                      '"old_keys_val":["666"]', res, '执行失败:' + text)

        text = 'step11:主机删除复制槽;expect:删除成功--'
        self.log.info(text)
        del_cmd = Pri_SH.execut_db_sql(f"select * from "
                                       f"pg_drop_replication_slot"
                                       f"('{self.slot_name}');")
        self.log.info(del_cmd)
        self.assertIn('', del_cmd, '执行失败:' + text)

    def tearDown(self):
        text = '--step12:清理环境;expect:清理环境完成--'
        self.log.info(text)
        sql_cmd = Pri_SH.execut_db_sql(f'''drop role if exists {self.us_name};    
            drop table if exists {self.tb_name};''')
        self.log.info(sql_cmd)
        rm_cmd = f"rm -rf {self.decode_file};"
        result = self.standby_node.sh(rm_cmd).result()
        self.log.info(result)
        del_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.standby_node.sh(del_msg).result()
        self.log.info(msg)
        del_msg = f"sed -i '/{self.us_name}/d' {self.pg_hba}"
        self.log.info(del_msg)
        msg = self.primary_node.sh(del_msg).result()
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
            '--Opengauss_Function_Logical_Replication_Case0005finish----')

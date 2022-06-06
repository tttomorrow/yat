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
Case Type   : 基础功能
Case Name   : 使用pitr恢复至创建发布订阅之后
Description :
    1.两集群开启归档，并进行基础备份
    2.在两个集群创建表
    3.创建发布订阅
    4.两个集群均创建laber_name
    5.更新数据
    6.查询数据是否更新
    7.发布端恢复至laber_name
    8.更新数据
    9.查询数据是否更新
    10.订阅端恢复至laber_name
    11.更新数据
    12.查询数据是否更新
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.更新
    7.成功
    8.成功
    9.更新
    10.成功
    11.成功
    12.更新
History     :
"""
import unittest
import os
import time
from yat.test import macro
from yat.test import Node
from testcase.utils.Logger import Logger
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common
from testcase.utils.Constant import Constant

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class Pubsubclass(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info("-Opengauss_Function_Pub_Sub_Case0072 start-")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com_pub = Common()
        self.com_sub = Common('remote1_PrimaryDbUser')
        self.tb_name1 = 'tb_pubsub_case072_1'
        self.tb_name2 = 'tb_pubsub_case072_2'
        self.tbs_name = 'tps_pubsub_case072'
        self.schema_name1 = 's_pubsub_case072_1'
        self.subname1 = "sub_case072_1"
        self.pubname1 = "pub_case072_1"
        self.parent_path_pub = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.parent_path_sub = os.path.dirname(macro.DB_INSTANCE_PATH_REMOTE1)
        self.port = str(int(self.pri_userdb_pub.db_port) + 1)
        self.wal_level = self.com_pub.show_param("wal_level")
        self.user_param_pub = f'-U {self.pri_userdb_pub.db_user} ' \
            f'-W {self.pri_userdb_pub.db_password}'
        self.user_param_sub = f'-U {self.pri_userdb_sub.db_user} ' \
            f'-W {self.pri_userdb_sub.db_password}'

        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')};"
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')}" \
            f" {os.path.join(self.parent_path_sub, 'pg_hba.conf')};"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        self.backup_path_pub = os.path.join(self.parent_path_pub,
                                            'back_pubsub_case072')
        self.backup_path_sub = os.path.join(self.parent_path_sub,
                                            'back_pubsub_case072')
        self.comsh_sta_pub = []
        self.nodelist_pub = ['Standby1DbUser', 'Standby2DbUser']
        for i in range(2):
            self.comsh_sta_pub.append(CommonSH(self.nodelist_pub[i]))
        self.comsh_sta_sub = []
        self.nodelist_sub = ['remote1_Standby1DbUser',
                             'remote1_Standby2DbUser']
        for i in range(2):
            self.comsh_sta_sub.append(CommonSH(self.nodelist_sub[i]))
        self.tbs_path_pub = os.path.join(self.parent_path_pub, self.tbs_name)
        self.tbs_path_sub = os.path.join(self.parent_path_sub, self.tbs_name)
        self.archive_path_pub = os.path.join(self.parent_path_pub, 'archive')
        self.archive_path_sub = os.path.join(self.parent_path_sub, 'archive')
        self.recovery_path_pub = os.path.join(macro.DB_INSTANCE_PATH,
                                              'recovery.conf')
        self.recovery_path_sub = os.path.join(macro.DB_INSTANCE_PATH_REMOTE1,
                                              'recovery.conf')
        self.archive_mode_pub = self.com_pub.show_param("archive_mode")
        self.enable_slot_log_pub = self.com_pub.show_param("enable_slot_log")
        self.archive_mode_sub = self.com_sub.show_param(
            "archive_mode", macro.DB_ENV_PATH_REMOTE1)
        self.enable_slot_log_sub = self.com_sub.show_param(
            "enable_slot_log", macro.DB_ENV_PATH_REMOTE1)
        self.hostname_pub = self.pri_userdb_pub.sh('hostname').result()
        self.hostname_sub = self.pri_userdb_sub.sh('hostname').result()

    def test_pubsub(self):
        text = '--step:预置条件,修改pg_hba expect:成功'
        self.log.info(text)
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.pri_userdb_sub.db_user} '
            f'{self.pri_userdb_sub.db_host}/32 sha256')
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'wal_level=logical')
        self.assertTrue(result, '执行失败:' + text)
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_pub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)

        text = '--step1:两集群开启归档，并进行基础备份 expect:成功--'
        self.log.info(text)
        self.log.info("发布端:\n")
        cmd = f"mkdir {self.backup_path_pub};mkdir {self.archive_path_pub};"
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'archive_mode=on',
            self.hostname_pub)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f"archive_command = 'cp %p {self.archive_path_pub}/%f'",
            self.hostname_pub)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'enable_slot_log=on')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.restart_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        time.sleep(10)
        result = self.commsh_pub.exec_gs_basebackup(
            self.backup_path_pub, self.pri_userdb_pub.ssh_host,
            self.pri_userdb_pub.db_port,)
        self.assertTrue(result, '执行失败:' + text)
        cmd = f"chmod -R 700 {self.backup_path_pub}"
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        self.log.info("订阅端：\n")
        cmd = f"mkdir {self.backup_path_sub};mkdir {self.archive_path_sub};"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'archive_mode=on',
            self.hostname_sub, dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f"archive_command = 'cp %p {self.archive_path_sub}/%f'",
            self.hostname_sub, dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'enable_slot_log=on',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.restart_db_cluster(True,
                                                    macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        time.sleep(10)
        result = self.commsh_sub.exec_gs_basebackup(
            self.backup_path_sub, self.pri_userdb_sub.ssh_host,
            self.pri_userdb_sub.db_port,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        cmd = f"chmod -R 700 {self.backup_path_sub}"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)

        text = '--step2:两个集群均创建表 expect:成功--'
        self.log.info(text)
        sql1 = f"create tablespace {self.tbs_name} " \
            f" LOCATION '{self.tbs_path_pub}';"
        sql2 = f"create tablespace {self.tbs_name} " \
            f" LOCATION '{self.tbs_path_sub}';"
        sql = f"create schema {self.schema_name1};" \
            f"create table {self.schema_name1}.{self.tb_name1}" \
            f"(id1 INT primary key, id2 INT, id3 INT) " \
            f"tablespace {self.tbs_name};" \
            f"create table {self.tb_name2}(id int primary key " \
            f"CONSTRAINT id_nn NOT NULL,use_filename VARCHAR2(20)," \
            f"filename VARCHAR2(255),text VARCHAR2(2000))" \
            f"PARTITION BY RANGE(id)" \
            f"(PARTITION P1 VALUES LESS THAN(30), " \
            f"PARTITION P2 VALUES LESS THAN(60)," \
            f"PARTITION P3 VALUES LESS THAN(90)," \
            f" PARTITION P4 VALUES LESS THAN(MAXVALUE));"
        result = self.commsh_pub.execut_db_sql(
            sql1+sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         5, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql2+sql, self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         5, '执行失败:' + text)

        text = '--step3:创建发布订阅 expect:成功--'
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname1}  " \
            f"FOR  TABLE  {self.tb_name2}," \
            f"{self.schema_name1}.{self.tb_name1} ;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.ssh_password}' " \
            f"PUBLICATION {self.pubname1};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.create_sub_succ_msg), 1,
                         '执行失败:' + text)

        text = '--step4:两个集群均创建laber_name expect:成功--'
        self.log.info(text)
        sql = "select pg_switch_xlog();" \
              "select pg_create_restore_point('point1');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn('pg_create_restore_point', result, '执行失败' + text)
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('pg_create_restore_point', result, '执行失败' + text)

        text = '--step5:更新数据 expect:成功--'
        self.log.info(text)
        sql_insert = f"insert into {self.schema_name1}.{self.tb_name1} " \
            f"values(generate_series(1,100), 1, 1);" \
            f"insert into {self.tb_name2} values(1, 'first', '%一', '')," \
            f"(60, 'first', '%二', ''),(90, 'first', '%三', ''); "
        result = self.commsh_pub.execut_db_sql(sql_insert,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         2, '执行失败' + text)

        text = "--step6:查询数据是否更新 expect:更新--"
        self.log.info(text)
        sql_select = f"select count(*) from " \
            f"{self.schema_name1}.{self.tb_name1};" \
            f"select * from {self.tb_name2};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('3 rows', result, '执行失败' + text)
        self.assertIn('1 | first        | %一     |', result, '执行失败' + text)
        result_a = self.commsh_pub.execut_db_sql(sql_select,
                                               sql_type=self.user_param_pub)
        self.log.info(result_a)
        self.assertEqual(result_a, result, '执行失败' + text)

        text = "--step7:发布端恢复至laber_name expect:更新--"
        self.log.info(text)
        result = self.commsh_pub.stop_db_cluster()
        self.assertTrue(result, '执行失败:' + text)
        cmd = f"mv {macro.DB_INSTANCE_PATH} {macro.DB_INSTANCE_PATH}_bak;" \
            f"mv {self.backup_path_pub} {macro.DB_INSTANCE_PATH};" \
            f"ls -al {self.archive_path_pub}"
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        cmd = f"touch {self.recovery_path_pub};" \
            f"echo \"restore_command = " \
            f"'cp {self.archive_path_pub}/%f %p'\" > " \
            f"{self.recovery_path_pub};" \
            f"echo \"recovery_target_name='point1'\" >> " \
            f"{self.recovery_path_pub};" \
            f"cat {self.recovery_path_pub};"
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        result = self.commsh_pub.start_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        time.sleep(20)
        cmd_resume = "select pg_xlog_replay_resume();select pg_sleep(10);" \
                     "select pg_is_in_recovery();"
        result = self.commsh_pub.execut_db_sql(cmd_resume)
        self.log.info(result)
        self.assertIn('f', result.splitlines()[-2], '执行失败:' + text)
        for i in range(2):
            result = self.comsh_sta_pub[i].build_standby("-t 3600")
            self.assertIn(self.constant.BUILD_SUCCESS_MSG,
                          result, '执行失败:' + text)
        cmd = f"ls -al  {macro.DB_INSTANCE_PATH}"
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        result = self.commsh_pub.execut_db_sql(sql_select,
                                               sql_type=self.user_param_pub)
        self.log.info(result)

        text = '--step8:更新数据 expect:成功--'
        self.log.info(text)
        sql_insert = f"insert into {self.schema_name1}.{self.tb_name1} " \
            f"values(201, 1, 1);" \
            f"insert into {self.tb_name2} values(2, 'first', '%一', 'new');"
        result = self.commsh_pub.execut_db_sql(sql_insert,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         2, '执行失败' + text)

        text = "--step9:查询数据是否更新 expect:更新--"
        self.log.info(text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('4 rows', result, '执行失败' + text)
        self.assertIn('1 row', result, '执行失败' + text)
        self.assertIn('101', result, '执行失败' + text)
        self.assertIn('2 | first        | %一     | new',
                      result, '执行失败' + text)

        text = "--step10:订阅端恢复至laber_name expect:更新--"
        self.log.info(text)
        result = self.commsh_sub.stop_db_cluster(
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        cmd = f"mv {macro.DB_INSTANCE_PATH_REMOTE1} " \
            f"{macro.DB_INSTANCE_PATH_REMOTE1}_bak;" \
            f"mv {self.backup_path_sub} {macro.DB_INSTANCE_PATH_REMOTE1};"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        cmd = f"touch {self.recovery_path_sub};" \
            f"echo \"restore_command = " \
            f"'cp {self.archive_path_sub}/%f %p'\" > " \
            f"{self.recovery_path_sub};" \
            f"echo \"recovery_target_name='point1'\" >> " \
            f"{self.recovery_path_sub};" \
            f"cat {self.recovery_path_sub};"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        result = self.commsh_sub.start_db_cluster(
            True, env_path=macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        time.sleep(10)
        result = self.commsh_sub.execut_db_sql(cmd_resume,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('f', result.splitlines()[-2], '执行失败:' + text)
        for i in range(2):
            result = self.comsh_sta_sub[i].build_standby(
                "-t 3600", macro.DB_ENV_PATH_REMOTE1,
                macro.DB_INSTANCE_PATH_REMOTE1)
            self.assertIn(self.constant.BUILD_SUCCESS_MSG,
                          result, '执行失败:' + text)

        text = '--step11:更新数据 expect:成功--'
        self.log.info(text)
        sql_insert = f"insert into {self.schema_name1}.{self.tb_name1} " \
            f"values(202, 1, 1);" \
            f"insert into {self.tb_name2} values(222, 'first', '%一', 'new');"
        result = self.commsh_pub.execut_db_sql(sql_insert,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         2, '执行失败' + text)

        text = "--step12:查询数据是否更新 expect:更新--"
        self.log.info(text)
        sql_select = f"select * from " \
            f"{self.schema_name1}.{self.tb_name1};" \
            f"select * from {self.tb_name2};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('1 row'), 2, '执行失败' + text)
        self.assertIn('222 | first        | %一     | new',
                      result, '执行失败' + text)
        self.assertIn('202 |   1 |   1', result, '执行失败' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        result = self.commsh_pub.get_db_cluster_status('status')
        if not result:
            cmd = f"mv {macro.DB_INSTANCE_PATH}_bak {macro.DB_INSTANCE_PATH};"
            self.log.info(cmd)
            result = self.pri_userdb_pub.sh(cmd).result()
            self.log.info(result)
            self.commsh_pub.restart_db_cluster()
            for i in range(2):
                result = self.comsh_sta_pub[i].build_standby("-t 3600")
                self.assertIn(self.constant.BUILD_SUCCESS_MSG,
                              result, '执行失败:' + text)
        result = self.commsh_sub.get_db_cluster_status(
            'status', env_path=macro.DB_ENV_PATH_REMOTE1)
        if not result:
            cmd = f"mv {macro.DB_INSTANCE_PATH_REMOTE1}_bak " \
                f"{macro.DB_INSTANCE_PATH_REMOTE1};"
            self.log.info(cmd)
            result = self.pri_userdb_sub.sh(cmd).result()
            self.log.info(result)
            self.commsh_sub.restart_db_cluster(True,
                                               macro.DB_ENV_PATH_REMOTE1)
            for i in range(2):
                result = self.comsh_sta_sub[i].build_standby(
                    "-t 3600", macro.DB_ENV_PATH_REMOTE1,
                    macro.DB_INSTANCE_PATH_REMOTE1)
                self.assertIn(self.constant.BUILD_SUCCESS_MSG,
                              result, '执行失败:' + text)
        sql = f"DROP PUBLICATION if exists {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP SUBSCRIPTION  {self.subname1};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP table if exists {self.schema_name1}.{self.tb_name1};" \
            f"DROP table if exists {self.tb_name2};" \
            f"drop schema {self.schema_name1};" \
            f"drop tablespace {self.tbs_name};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        result = self.commsh_pub.execut_db_sql(sql, 
                                               sql_type=self.user_param_pub)
        self.log.info(result)

        cmd = f"mv " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};" \
            f"rm -rf {self.backup_path_pub};" \
            f"rm -rf {macro.DB_INSTANCE_PATH}_bak;" \
            f"rm -rf {self.tbs_path_pub};" \
            f"rm -rf {self.archive_path_pub};" \
            f"rm -rf {self.recovery_path_pub}"
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_sub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')};" \
            f"rm -rf {self.tbs_path_sub};" \
            f"rm -rf {self.backup_path_sub};" \
            f"rm -rf {macro.DB_INSTANCE_PATH_REMOTE1}_bak;" \
            f"rm -rf {self.archive_path_sub};" \
            f"rm -rf {self.recovery_path_sub}"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        result_wal = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level}')
        result1 = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'archive_mode={self.archive_mode_pub}',
            self.hostname_pub)
        result2 = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'enable_slot_log={self.enable_slot_log_pub}')
        result3 = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'archive_mode={self.archive_mode_sub}',
            self.hostname_sub, dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'enable_slot_log={self.enable_slot_log_sub}',
            self.hostname_sub, dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result and result1 and result2 and result3,
                        '执行失败:' + text)
        self.assertTrue(result_wal, '执行失败:' + text)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info("-Opengauss_Function_Pub_Sub_Case0072 end-")

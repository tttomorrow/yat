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
Case Name   : 订阅端配置max_logical_replication_workers
Description :
    1.检查默认值
    2.在两个集群创建表
    3.创建发布端
    4.创建订阅
    5.修改数据
    6.查询同步
    7.修改订阅端max_logical_replication_workers为无效值
    8.set方式配置
    9.修改数据
    10.查询同步
    12.创建订阅
    13.修改数据
    14.查询同步
    16.删除订阅
    18.创建订阅
Expect      :
    1.默认值为4
    2.成功
    3.成功
    4.成功
    5.成功
    6.数据均更新
    7.失败
    8.成功
    9.成功
    10.更新
    11.成功
    12.成功，但复制槽无法激活，且订阅端提示out of logical replication worker slots
    13.成功
    14.更新
    15.成功，原有复制槽失效
    16.成功
    17.成功
    18.成功，但复制槽无法激活，且订阅端提示out of logical replication worker slots
History     :
    modified：2022-4-1 by 5328126;修改pg_log目录，避免其他日志影响
"""
import unittest
import os
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
        self.log.info("-Opengauss_Function_Pub_Sub_Case0044 start-")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com_pub = Common()
        self.com_sub = Common('remote1_PrimaryDbUser')
        self.tb_name1 = 'tb_pubsub_case044_1'
        self.subname1 = "sub_case044_1"
        self.subname2 = "sub_case044_2"
        self.pubname1 = "pub_case044_1"
        self.parent_path_pub = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.parent_path_sub = os.path.dirname(macro.DB_INSTANCE_PATH_REMOTE1)
        self.port = str(int(self.pri_userdb_pub.db_port) + 1)
        self.wal_level = self.com_pub.show_param("wal_level")
        self.user_param_pub = f'-U {self.pri_userdb_pub.db_user} ' \
            f'-W {self.pri_userdb_pub.db_password}'
        self.user_param_sub = f'-U {self.pri_userdb_sub.db_user} ' \
            f'-W {self.pri_userdb_sub.db_password}'
        self.max_logical_replication_workers = \
            self.com_sub.show_param("max_logical_replication_workers",
                                    env_path=macro.DB_ENV_PATH_REMOTE1)
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
        self.case_no = os.path.basename(__file__)[-6:-3]
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    f'pub_sub_case{self.case_no}')
        self.log_directory = self.com_pub.show_param("log_directory")
        self.hostname = self.pri_userdb_sub.sh('hostname').result().strip()

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
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    all  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_pub.db_host}/32 sha256')
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'wal_level=logical')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.restart_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_pub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host all  {self.pri_userdb_sub.db_user} '
            f'{self.pri_userdb_sub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f"log_directory='{self.dir_new}'",
            self.hostname, False, False,
            macro.DB_INSTANCE_PATH_REMOTE1, '',
            macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.restart_db_cluster(True,
                                                    macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step1:检查默认值 expect:默认值为4--'
        self.log.info(text)
        self.assertEqual(self.max_logical_replication_workers,
                         '4', '执行失败:' + text)

        result = self.commsh_pub.execute_gsguc(
            'check', self.constant.GSGUC_SUCCESS_MSG,
            'max_logical_replication_workers',
            get_detail=True)
        flg = 'NULL' in result or '4' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step2:两个集群均创建表 expect:成功--'
        self.log.info(text)
        sql_table = f"CREATE TABLE {self.tb_name1}(" \
            f"id NUMBER(7) primary key, use_filename VARCHAR2(20) , " \
            f"filename VARCHAR2(255), text VARCHAR2(2000));"
        result = self.commsh_pub.execut_db_sql(
            sql_table, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         2, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql_table,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         2, '执行失败:' + text)

        text = '--step3:创建发布端 expect:成功--'
        self.log.info(text)
        sql = f"begin;" \
            f"CREATE PUBLICATION {self.pubname1} " \
            f"for table {self.tb_name1};" \
            f"end;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.COMMIT_SUCCESS_MSG, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = '--step4:创建订阅 expect:成功--'
        self.log.info(text)
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

        text = '--step5:修改数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} values(1, '66^^&', '中文', 'test');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result, '执行失败' + text)

        text = "--step6:查询同步  expect:数据均更新--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('1 row', result, '执行失败' + text)
        self.assertIn('1 | 66^^&        | 中文   | test',
                      result, '执行失败' + text)

        text = "--step7:修改订阅端max_logical_replication_workers为无效值  expect:失败--"
        self.log.info(text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'max_logical_replication_workers=262144',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1,
            get_detail=True)
        flg = 'valid range for parameter ' \
              '"max_logical_replication_workers" (0 .. 262143)'
        self.assertIn(flg, result, '执行失败:' + text)
        self.assertNotIn(self.constant.GSGUC_SUCCESS_MSG,
                         result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'max_logical_replication_workers=-1',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1,
            get_detail=True)
        self.assertIn(flg, result, '执行失败:' + text)
        self.assertNotIn(self.constant.GSGUC_SUCCESS_MSG,
                         result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'max_logical_replication_workers=1.5',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1,
            get_detail=True)
        flg = "is incorrect, requires a integer value"
        self.assertIn(flg, result, '执行失败:' + text)
        self.assertNotIn(self.constant.GSGUC_SUCCESS_MSG,
                         result, '执行失败:' + text)

        text = "--step8:set方式配置  expect:成功--"
        self.log.info(text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'max_logical_replication_workers=262143',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.restart_db_cluster(True,
                                                    macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or \
              'Degraded' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step9:修改数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} " \
            f"values(generate_series(2,100), '66^^&', '中文', 'test');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         1, '执行失败' + text)

        text = '--step10:查询同步 expect:更新--'
        self.log.info(text)
        sql = f"select count(*) from {self.tb_name1};"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('100', result, '执行失败' + text)
        sql = f"update {self.tb_name1} set " \
            f"use_filename='update' where id=1;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.UPDATE_SUCCESS_MSG, result, '执行失败' + text)
        sql = f"select count(*) from {self.tb_name1} " \
            f"where use_filename='update';"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual('1', result.splitlines()[-2].strip(), '执行失败' + text)
        sql = f"delete from {self.tb_name1} where id>90;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.DELETE_SUCCESS_MSG, result, '执行失败' + text)
        sql = f"select count(*) from {self.tb_name1} ;"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('90', result, '执行失败' + text)

        text = '--step11:alter方式修改  expect:成功--'
        self.log.info(text)
        sql = f"ALTER SYSTEM SET max_logical_replication_workers TO 1;"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.alter_system_success_msg,
                      result, '执行失败' + text)
        result = self.commsh_sub.restart_db_cluster(True,
                                                    macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or \
              'Degraded' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step12:创建订阅 ' \
               'expect:成功，但复制槽无法激活，' \
               '且订阅端提示out of logical replication worker slots--'
        self.log.info(text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"show max_logical_replication_workers;" \
            f"CREATE SUBSCRIPTION {self.subname2} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.ssh_password}' " \
            f"PUBLICATION {self.pubname1};" \
            f"select * from pg_subscription ;" \
            f"select pg_sleep(3);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.create_sub_succ_msg, result,
                         '执行失败:' + text)
        log_flg = f'WARNING:  out of logical replication worker slot'
        result = self.com_pub.find_pglog_content(
            node=self.pri_userdb_sub,
            content=log_flg, env_path=macro.DB_ENV_PATH_REMOTE1,
            path=self.dir_new)
        self.assertTrue(result, '执行失败' + text)

        self.assertTrue(result, '执行失败' + text)
        sql_f = "select pg_sleep(30);" \
              "select slot_name from pg_replication_slots where active=false;"
        result = self.commsh_pub.execut_db_sql(sql_f,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.subname2, result, '执行失败' + text)

        text = '--step13:修改数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} " \
            f"values(generate_series(200,230), '66^^&', '中文', 'test');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         1, '执行失败' + text)

        text = '--step14:查询同步 expect:更新--'
        self.log.info(text)
        sql = f"select count(*) from {self.tb_name1};"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('121', result, '执行失败' + text)
        sql = f"update {self.tb_name1} set " \
            f"use_filename='update2' where id=201;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.UPDATE_SUCCESS_MSG, result, '执行失败' + text)
        sql = f"select count(*) from {self.tb_name1} " \
            f"where use_filename='update2';"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual('1', result.splitlines()[-2].strip(), '执行失败' + text)
        sql = f"delete from {self.tb_name1} where id>220;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.DELETE_SUCCESS_MSG, result, '执行失败' + text)
        sql = f"select count(*) from {self.tb_name1} ;"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('111', result, '执行失败' + text)

        text = '--step15:alter方式修改  expect:成功，原有复制槽失效--'
        self.log.info(text)
        sql = f"ALTER SYSTEM SET max_logical_replication_workers TO 0;"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.alter_system_success_msg,
                      result, '执行失败' + text)
        result = self.commsh_sub.restart_db_cluster(True,
                                                    macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or \
              'Degraded' in result
        self.assertTrue(flg, '执行失败:' + text)
        result = self.com_pub.find_pglog_content(
            node=self.pri_userdb_sub,
            content=log_flg, env_path=macro.DB_ENV_PATH_REMOTE1,
            path=self.dir_new)

        self.assertTrue(result, '执行失败' + text)
        result = self.commsh_pub.execut_db_sql(sql_f,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.subname2, result, '执行失败' + text)
        self.assertIn(self.subname1, result, '执行失败' + text)

        text = '--step16:删除订阅  expect:成功--'
        self.log.info(text)
        sql = f"select * from pg_subscription ;" \
            f"drop SUBSCRIPTION {self.subname1};" \
            f"drop SUBSCRIPTION {self.subname2};"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.drop_sub_succ_msg, result, '执行失败' + text)

        text = '--step17:alter方式修改  expect:成功--'
        self.log.info(text)
        sql = f"ALTER SYSTEM SET max_logical_replication_workers TO 0;"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.alter_system_success_msg,
                      result, '执行失败' + text)
        result = self.commsh_sub.restart_db_cluster(True,
                                                    macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or \
              'Degraded' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step18:创建订阅 expect:成功，但复制槽无法激活，' \
               '且订阅端提示out of logical replication worker slots--'
        self.log.info(text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"CREATE SUBSCRIPTION {self.subname2} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.ssh_password}' " \
            f"PUBLICATION {self.pubname1};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.create_sub_succ_msg, result,
                         '执行失败:' + text)
        result = self.com_pub.find_pglog_content(
            node=self.pri_userdb_sub,
            content=log_flg, env_path=macro.DB_ENV_PATH_REMOTE1,
            path=self.dir_new)

        self.assertTrue(result, '执行失败' + text)
        sql = "select pg_sleep(30);" \
              "select slot_name from pg_replication_slots where active=false;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.subname2, result, '执行失败' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"DROP PUBLICATION if exists {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP SUBSCRIPTION  {self.subname1};" \
            f"DROP SUBSCRIPTION  {self.subname2};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP table if exists {self.tb_name1};"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)

        cmd = f"mv " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} "
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_sub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')} "
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level}')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'max_logical_replication_workers='
            f'{self.max_logical_replication_workers}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        result1 = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f"log_directory='{self.log_directory}'",
            self.hostname, False, False,
            macro.DB_INSTANCE_PATH_REMOTE1, '',
            macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result and result1, '执行失败:' + text)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info("-Opengauss_Function_Pub_Sub_Case0044 end-")

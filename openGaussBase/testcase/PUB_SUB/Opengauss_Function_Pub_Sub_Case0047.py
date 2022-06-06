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
Case Name   : max_replication_slots等于物理+逻辑(激活的发布)
Description :
    1.修改max_replication_slots为5
    2.两个集群创建表
    3.创建逻辑复制槽
    4.创建发布端订阅端（假设集群为1主2备，则需再逻辑复制槽2个）
    5.修改数据
    6.读取复制槽slot1解码结果
    7.查看数据是否更新
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.成功,tb_pubsub_case047_1/tb_pubsub_case047_2存在于解码记录中
    7.tb_pubsub_case047_1/tb_pubsub_case047_2更新，其余未更新
History     :
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
        self.log.info("-Opengauss_Function_Pub_Sub_Case0047 start-")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com = Common()
        self.tb_name = ['tb_pubsub_case047_1', 'tb_pubsub_case047_2',
                        'tb_pubsub_case047_3']
        self.subname = ["sub_case047_1", "sub_case047_2"]
        self.pubname = ["pub_case047_1", "pub_case047_2"]
        self.slot_name = "slot_case047"
        self.parent_path_pub = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.parent_path_sub = os.path.dirname(macro.DB_INSTANCE_PATH_REMOTE1)
        self.port = str(int(self.pri_userdb_pub.db_port) + 1)
        self.wal_level = self.com.show_param("wal_level")
        self.max_replication_slots = \
            self.com.show_param("max_replication_slots")
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

        text = '--step1:修改max_replication_slots为5 expect:成功--'
        self.log.info(text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'max_replication_slots=5')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.restart_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step2:两个集群均创建表 expect:成功--'
        self.log.info(text)
        sql_table = f"CREATE TABLE {self.tb_name[0]}(id NUMBER(7) " \
            f"CONSTRAINT s_longtext_id_nn NOT NULL,  " \
            f"use_filename VARCHAR2(20) primary key, " \
            f"filename VARCHAR2(255), text VARCHAR2(2000));" \
            f"CREATE TABLE {self.tb_name[1]}(like " \
            f"{self.tb_name[0]} including all);" \
            f"CREATE TABLE {self.tb_name[2]}(i int primary key, " \
            f"text varchar(1024)) WITH " \
            f"(ORIENTATION = COLUMN, COMPRESSION=HIGH);"
        result = self.commsh_pub.execut_db_sql(
            sql_table, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         6, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql_table,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         6, '执行失败:' + text)

        text = '--step3:创建逻辑复制槽 expect:成功--'
        self.log.info(text)
        sql = f"SELECT * FROM pg_create_logical_replication_slot(" \
            f"'{self.slot_name}', 'mppdb_decoding');"
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.slot_name, result, '执行失败:' + text)

        text = '--step4:创建发布端订阅端（假设集群为1主2备，则需再创建逻辑复制槽2个） expect:成功--'
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname[0]} " \
            f"for table {self.tb_name[0]} ;" \
            f"CREATE PUBLICATION {self.pubname[1]} for " \
            f"table {self.tb_name[1]},{self.tb_name[2]};" \
            f"select * from pg_PUBLICATION;"
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        for i in range(2):
            sql = f"CREATE SUBSCRIPTION {self.subname[i]} CONNECTION " \
                f"'host={self.pri_userdb_pub.db_host} " \
                f"port={self.port} " \
                f"user={self.pri_userdb_pub.db_user} " \
                f"dbname={self.pri_userdb_pub.db_name} " \
                f"password={self.pri_userdb_pub.ssh_password}' " \
                f"PUBLICATION {self.pubname[i]};" \
                f"select pg_sleep(30);" \
                f"select * from pg_SUBSCRIPTION;"
            result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub,
                                                   None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            self.assertIn(self.constant.create_sub_succ_msg,
                          result, '执行失败:' + text)

        text = '--step5:修改数据 expect:成功--'
        self.log.info(text)
        sql = f"select * from pg_replication_slots ;" \
            f"insert into {self.tb_name[0]} " \
            f"values(1, '1', '{self.tb_name[0]}', 'equal');" \
            f"insert into {self.tb_name[1]} " \
            f"values(1, '1', '{self.tb_name[1]}', 'equal');" \
            f"insert into {self.tb_name[2]} " \
            f"values(1, '1');"
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                      result, '执行失败' + text)
        self.assertIn('5 rows', result, '执行失败' + text)

        text = "--step6:读取复制槽slot1解码结果  " \
               "expect:成功,tb_pubsub_case047_1/tb_pubsub_case047_2存在于解码记录中--"
        self.log.info(text)
        sql = f"SELECT * FROM pg_logical_slot_peek_changes(" \
            f"'{self.slot_name}', NULL, 4096);"
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result)
        for i in range(2):
            flg = f'"table_name":"public.{self.tb_name[i]}",' \
                f'"op_type":"INSERT","columns_name":'
            self.assertIn(flg, result, '执行失败:' + text)

        text = '--step7:查看数据是否更新 ' \
               'expect:tb_pubsub_case047_1/tb_pubsub_case047_2更新，其余未更新--'
        self.log.info(text)
        for i in range(3):
            sql = f"select * from {self.tb_name[i]};"
            result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub,
                                                   None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            if i < 2:
                self.assertIn('1 row', result, '执行失败:' + text)
                flg = f'1 | 1            | {self.tb_name[i]} | equal'
                self.assertIn(flg, result, '执行失败:' + text)
            else:
                self.assertIn('0 rows', result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        for i in range(2):
            sql = f"DROP PUBLICATION if exists {self.pubname[i]};"
            drop_pub_result = self.commsh_pub.execut_db_sql(
                sql, sql_type=self.user_param_pub)
            self.log.info(drop_pub_result)
            sql = f"DROP SUBSCRIPTION if exists {self.subname[i]};"
            drop_sub_result = self.commsh_sub.execut_db_sql(
                sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
            self.log.info(drop_sub_result)
        for i in range(3):
            sql = f"DROP table if exists {self.tb_name[i]};"
            result = self.commsh_sub.execut_db_sql(sql,
                                                   self.user_param_sub, None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            result = self.commsh_pub.execut_db_sql(
                sql, sql_type=self.user_param_pub)
            self.log.info(result)
        sql = f"select * from pg_drop_replication_slot('{self.slot_name}');"
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
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
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'max_replication_slots={self.max_replication_slots}')
        self.assertTrue(result, '执行失败:' + text)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info("-Opengauss_Function_Pub_Sub_Case0047 end-")

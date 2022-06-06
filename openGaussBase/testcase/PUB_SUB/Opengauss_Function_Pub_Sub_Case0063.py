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
Case Name   : 发布端和订阅端同时执行事务
Description :
    1.两个集群创建表
    2.创建发布订阅
    3.发布端订阅端执行事务
    4.创建发布订阅
    5.执行事务的过程中更新数据
    6.查询数据是否更新
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.更新
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
from testcase.utils.ComThread import ComThread

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class Pubsubclass(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} start-----")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com_pub = Common()
        self.com_sub = Common('remote1_PrimaryDbUser')
        self.tb_name1 = 'tb_pubsub_063_1'
        self.tb_name2 = 'tb_pubsub_063_2'
        self.tb_name3 = 'tb_pubsub_063_3'
        self.subname1 = "sub_063_1"
        self.pubname1 = "pub_063_1"
        self.schema_name = "schema_063_1"
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

    def test_pubsub(self):
        text = '--step:预置条件,修改pg_hba expect:成功'
        self.log.info(text)
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_sub.db_host}/32 sha256')
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

        text = '--step1:两个集群创建表 expect:成功--'
        self.log.info(text)
        create_sql = f"create schema {self.schema_name};" \
            f"CREATE TABLE {self.schema_name}.{self.tb_name1}" \
            f"(id1 INT primary key, id2 INT, id3 INT);" \
            f"CREATE TABLE {self.tb_name2}" \
            f"(id int primary key CONSTRAINT id_nn NOT NULL," \
            f"use_filename VARCHAR2(20)," \
            f"filename VARCHAR2(255)," \
            f"text VARCHAR2(2000))PARTITION BY RANGE(id)" \
            f"(        PARTITION P1 VALUES LESS THAN(30)," \
            f"        PARTITION P2 VALUES LESS THAN(60)," \
            f"        PARTITION P3 VALUES LESS THAN(90)," \
            f"        PARTITION P4 VALUES LESS THAN(MAXVALUE));" \
            f"create table {self.tb_name3}(i int, t text);"
        result = self.commsh_pub.execut_db_sql(
            create_sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         5, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(create_sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         5, '执行失败:' + text)

        text = "--step2:创建发布订阅 expect:成功--"
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname1} for table " \
            f"{self.schema_name}.{self.tb_name1},{self.tb_name2};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.create_keycipher_success,
                      result, '执行失败:' + text)
        sql = f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.ssh_password}' " \
            f"PUBLICATION {self.pubname1} ;"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.create_sub_succ_msg), 1,
                         '执行失败:' + text)

        text3 = "--step3:发布端订阅端执行事务 expect:成功--"
        self.log.info(text3)
        sql = f"insert into {self.tb_name3} values" \
            f"(generate_series(1,99999), 'test');" \
            f"update {self.tb_name3} set t='update' where i>200;" \
            f"delete from {self.tb_name3} where t='update';" \
            f"insert into {self.tb_name3} values" \
            f"(generate_series(100000,109999), 'new');" \
            f"update {self.tb_name3} set i=1;"
        pub_thread = ComThread(self.commsh_pub.execut_db_sql,
                               args=(sql, self.user_param_pub))
        pub_thread.setDaemon(True)
        pub_thread.start()
        sub_thread = ComThread(self.commsh_sub.execut_db_sql,
                               args=(sql, self.user_param_sub,
                                     None, macro.DB_ENV_PATH_REMOTE1))
        sub_thread.setDaemon(True)
        sub_thread.start()

        text = "--step4:执行事务的过程中更新数据 expect:成功--"
        self.log.info(text)
        sql = f"insert into {self.schema_name}.{self.tb_name1} " \
            f"values(1, 1, 1),(2,2,2);" \
            f"insert into {self.tb_name2} values(1, 'first', '%一', '')," \
            f"(60, 'first', '%二', ''),(90, 'first', '%三', ''); "
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(2, result.count(self.constant.INSERT_SUCCESS_MSG),
                         '执行失败:' + text)

        text = "--step5:查询数据是否更新 expect:成功--"
        self.log.info(text)
        sql = f"select * from {self.schema_name}.{self.tb_name1};" \
            f"select * from {self.tb_name2};"
        result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('2 rows', result, '执行失败:' + text)
        self.assertIn('3 rows', result, '执行失败:' + text)
        self.assertIn('1 |   1 |   1', result, '执行失败:' + text)
        self.assertIn('2 |   2 |   2', result, '执行失败:' + text)
        self.assertIn('1 | first        | %一     |', result, '执行失败:' + text)
        self.assertIn('60 | first        | %二     |', result, '执行失败:' + text)
        self.assertIn('90 | first        | %三     |', result, '执行失败:' + text)
        pub_thread.join(30)
        result = pub_thread.get_result()
        self.log.info(result)
        self.assertEqual(2, result.count(self.constant.INSERT_SUCCESS_MSG),
                         '执行失败:' + text3)
        self.assertEqual(2, result.count(self.constant.UPDATE_SUCCESS_MSG),
                         '执行失败:' + text3)
        self.assertEqual(1, result.count(self.constant.DELETE_SUCCESS_MSG),
                         '执行失败:' + text3)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text3)
        sub_thread.join(30)
        result = sub_thread.get_result()
        self.log.info(result)
        self.assertEqual(2, result.count(self.constant.INSERT_SUCCESS_MSG),
                         '执行失败:' + text3)
        self.assertEqual(2, result.count(self.constant.UPDATE_SUCCESS_MSG),
                         '执行失败:' + text3)
        self.assertEqual(1, result.count(self.constant.DELETE_SUCCESS_MSG),
                         '执行失败:' + text3)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text3)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"select pg_sleep(10);" \
            f"DROP SUBSCRIPTION  {self.subname1};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP PUBLICATION if exists {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP table if exists {self.tb_name2};" \
            f"DROP table if exists {self.schema_name}.{self.tb_name1};" \
            f"drop schema {self.schema_name};" \
            f"drop table if exists {self.tb_name3}"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)

        cmd = f"mv " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};"
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
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

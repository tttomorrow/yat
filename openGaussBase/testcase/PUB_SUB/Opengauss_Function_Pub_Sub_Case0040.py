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
Case Name   : 删除已有发布内容
Description :
    1.在两个集群创建表
    2.创建发布端
    3.创建订阅
    4.修改数据
    5.查询同步
    6.修改发布端
    7.修改发布端
    8.修改数据
    9.查询同步
    10.修改发布端
    11.修改数据
    12.查询同步
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.除tb_pubsub_case040_3未更新。其余均更新
    6.失败
    7.成功
    8.成功
    9.除tb_pubsub_case040_1更新。其余均未更新
    10.成功
    11.成功
    12..除tb_pubsub_case040_1更新。其余均未更新
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
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} start-----")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com_pub = Common()
        self.tb_name1 = 'tb_pubsub_case040_1'
        self.tb_name2 = 'tb_pubsub_case040_2'
        self.tb_name3 = 'tb_pubsub_case040_3'
        self.subname1 = "sub_case040_1"
        self.pubname1 = "pub_case040_1"
        self.port = str(int(self.pri_userdb_pub.db_port) + 1)
        self.wal_level = self.com_pub.show_param("wal_level")
        self.user_param_pub = f'-U {self.pri_userdb_pub.db_user} ' \
            f'-W {self.pri_userdb_pub.db_password}'
        self.user_param_sub = f'-U {self.pri_userdb_sub.db_user} ' \
            f'-W {self.pri_userdb_sub.db_password}'

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
        if 'logical' != self.wal_level:
            result = self.commsh_pub.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG, 'wal_level=logical')
            self.assertTrue(result, '执行失败:' + text)
            result = self.commsh_pub.restart_db_cluster(True)
            flg = self.constant.START_SUCCESS_MSG in result \
                  or 'Degrade' in result
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

        text = '--step1:两个集群均创建表 expect:成功--'
        self.log.info(text)
        sql_table = f"CREATE TABLE {self.tb_name1}(id NUMBER(7) " \
            f"CONSTRAINT s_longtext_id_nn NOT NULL, " \
            f"use_filename VARCHAR2(20) primary key, " \
            f"filename VARCHAR2(255), text VARCHAR2(2000));" \
            f"CREATE TABLE {self.tb_name2}" \
            f"(like {self.tb_name1} including all);" \
            f"create table {self.tb_name3}(i int primary key, " \
            f"use_filename VARCHAR2(2000), " \
            f"constraint fk_id foreign key(use_filename) " \
            f"references {self.tb_name1}(use_filename));"
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

        text = '--step2:创建发布端 expect:成功--'
        self.log.info(text)        
        sql = f"CREATE PUBLICATION {self.pubname1}  for table " \
            f"{self.tb_name1}*, {self.tb_name2};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = '--step3:创建订阅 expect:成功--'
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

        text = '--step4:修改表数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} " \
            f"values(1, '66666^^&', '中文', 'test');select pg_sleep(5.5);" \
            f"insert into {self.tb_name2} " \
            f"values(1, '66666^^&', '中文', 'test');" \
            f"insert into {self.tb_name3} values(1, '66666^^&');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         3, '执行失败' + text)

        text = "--step5:查询是否同步  expect:除tb_pubsub_case039_3未更新。其余均更新--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1};" \
            f"select * from {self.tb_name2};" \
            f"select * from {self.tb_name3};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('1 row'), 2, '执行失败' + text)
        self.assertEqual(result.count('0 rows'), 1, '执行失败' + text)
        self.assertIn('1 | 66666^^&     | 中文   | test',
                      result.splitlines()[2], '执行失败' + text)
        self.assertIn('1 | 66666^^&     | 中文   | test',
                      result.splitlines()[7], '执行失败' + text)

        text = '--step6:修改发布端  expect:失败--'
        self.log.info(text)
        sql = f"ALTER PUBLICATION {self.pubname1}  set table tb_not_exists;" \
            f"ALTER PUBLICATION {self.pubname1} " \
            f"drop table only {self.tb_name3};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.NOT_EXIST, result, '执行失败:' + text)
        self.assertIn('is not part of the publication',
                      result, '执行失败:' + text)

        text = '--step7:修改发布端  expect:成功--'
        self.log.info(text)
        sql = f"ALTER PUBLICATION {self.pubname1}  " \
            f"drop table {self.tb_name1};" \
            f"ALTER PUBLICATION {self.pubname1}  " \
            f"add table {self.tb_name3};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.alter_pub_succ_msg,
                      result, '执行失败:' + text)

        text = '--step8:修改表数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} " \
            f"values(9, '6666^^&', '中文', 'test');" \
            f"insert into {self.tb_name2} " \
            f"values(9, '6666^^&', '中文', 'test');" \
            f"insert into {self.tb_name3} values(9, '66666^^&');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         3, '执行失败' + text)

        text = "--step9:查询是否同步  expect:除tb_pubsub_case039_1未更新。其余均更新--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1};" \
            f"select * from {self.tb_name2};" \
            f"select * from {self.tb_name3};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('1 row'), 2, '执行失败' + text)
        self.assertEqual(result.count('2 rows'), 1, '执行失败' + text)
        self.assertIn('1 | 66666^^&     | 中文   | test',
                      result.splitlines()[2], '执行失败' + text)
        self.assertIn('9 | 6666^^&      | 中文   | test', result, '执行失败' + text)
        self.assertIn(' 9 | 66666^^&', result.splitlines()[-2], '执行失败' + text)

        text = '--step10:修改发布端  expect:成功--'
        self.log.info(text)
        sql = f"ALTER PUBLICATION {self.pubname1}  " \
            f"drop table {self.tb_name2};" \
            f"ALTER PUBLICATION {self.pubname1} " \
            f"add table {self.tb_name2};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.alter_pub_succ_msg,
                      result, '执行失败:' + text)

        text = '--step11:修改表数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} " \
            f"values(2, 'relation^^&', '中文', 'test');" \
            f"insert into {self.tb_name2} " \
            f"values(2, 'relation^^&', '中文', 'test');" \
            f"insert into {self.tb_name3} values(2, 'relation^^&');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         3, '执行失败' + text)

        text = "--step12:查询是否同步  expect:除tb_pubsub_case039_1未更新。其余均更新--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1};" \
            f"select * from {self.tb_name2};" \
            f"select * from {self.tb_name3};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('1 row'), 1, '执行失败' + text)
        self.assertEqual(result.count('2 rows'), 1, '执行失败' + text)
        self.assertEqual(result.count('3 rows'), 1, '执行失败' + text)
        self.assertIn('1 | 66666^^&     | 中文   | test',
                      result.splitlines()[2], '执行失败' + text)
        self.assertIn('2 | relation^^&',
                      result.splitlines()[-2], '执行失败' + text)
        self.assertIn('2 | relation^^&  | 中文   | test',
                      result, '执行失败' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"DROP PUBLICATION if exists {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP SUBSCRIPTION  {self.subname1};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP table if exists {self.tb_name2};" \
            f"DROP table if exists {self.tb_name3};" \
            f"DROP table if exists {self.tb_name1};"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        guc_res1 = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.pri_userdb_sub.db_user} '
            f'{self.pri_userdb_sub.db_host}/32')
        self.log.info(guc_res1)
        guc_res2 = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    all  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_pub.db_host}/32 sha256')
        self.log.info(guc_res2)
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_pub.db_host}/32',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        guc_res3 = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host all  {self.pri_userdb_sub.db_user} '
            f'{self.pri_userdb_sub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res3)
        self.assertTrue(guc_res and guc_res1 and guc_res2 and guc_res3,
                        '执行失败:' + text)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

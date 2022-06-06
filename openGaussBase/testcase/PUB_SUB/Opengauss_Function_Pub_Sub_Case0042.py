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
Case Name   : 删除发布
Description :
    1.在两个集群创建表
    2.创建发布端
    3.创建订阅
    4.删除不存在发布
    5.删除不存在发布
    6.删除发布
    7.修改数据
    8.查询同步
    9.创建发布订阅
    10.修改数据，并查询同步情况
    11.删除订阅sub1
    12.修改数据，并查询同步
    13.删除发布
    14.修改数据
    15.查询同步
Expect      :
    1.成功
    2.成功
    3.成功
    4.失败
    5.成功，提示不存在无需删除
    6.成功
    7.成功
    8.未更新
    9.成功
    10.集群A插入数据成功，集群B同步，pg_log显示找不到"pub1" does not exist
    11.成功
    12.集群A插入成功，(22, '66', '中文', 'test');被同步到集群B
    13.成功
    14.成功
    15.未同步
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
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} start-----")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com_pub = Common()
        self.com_sub = Common('remote1_PrimaryDbUser')
        self.tb_name1 = 'tb_pubsub_case042_1'
        self.tb_name2 = 'tb_pubsub_case042_2'
        self.tb_name3 = 'tb_pubsub_case042_3'
        self.subname1 = "sub_case042_1"
        self.subname2 = "sub_case042_2"
        self.pubname1 = "pub_case042_1"
        self.pubname2 = "pub_case042_2"
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
        self.case_no = os.path.basename(__file__)[-6:-3]
        self.dir_new = os.path.join('$GAUSSLOG', 'pg_log', 'pg_bak'
                                    f'pub_sub_case{self.case_no}')
        self.log_directory = self.com_sub.show_param(
            "log_directory", macro.DB_ENV_PATH_REMOTE1)
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
        sql = f"CREATE PUBLICATION {self.pubname1}  for " \
            f"table {self.tb_name1},{self.tb_name2};"
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

        text = '--step4:删除不存在发布 expect:失败--'
        self.log.info(text)
        sql = f"drop PUBLICATION not_exists;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.NOT_EXIST, result, '执行失败:' + text)

        text = '--step5:删除不存在发布 expect:成功，提示不存在无需删除--'
        self.log.info(text)
        sql = f"drop PUBLICATION if exists not_exists;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.drop_pub_succ_msg, result, '执行失败:' + text)

        text = '--step6:删除发布 expect:成功--'
        self.log.info(text)
        sql = f"drop PUBLICATION if exists {self.pubname1} cascade;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.drop_pub_succ_msg, result, '执行失败:' + text)

        text = '--step7:修改数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} values(2, '66^^&', '中文', 'test');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result, '执行失败' + text)

        text = "--step8:查询同步  expect:未更新--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1};" \
            f"select * from {self.tb_name2};" \
            f"select * from {self.tb_name3};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('0 rows'), 3, '执行失败' + text)

        text = '--step9:创建发布订阅  expect:成功--'
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname2} for all tables;"
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
        sql = f"CREATE SUBSCRIPTION {self.subname2} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.ssh_password}' " \
            f"PUBLICATION {self.pubname2};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.create_sub_succ_msg), 1,
                         '执行失败:' + text)

        text = '--step10:修改数据，并查询同步情况 ' \
               'expect:集群A插入数据成功，集群B同步，pg_log显示找不到"pub1" does not exist--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} values(3, '6^^&', '中文', 'test');" \
            f"select pg_sleep(5.5);" \
            f"insert into {self.tb_name2} values(3, '6^^&', '中文', 'test');" \
            f"insert into {self.tb_name3} values(3, '6^^&');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         3, '执行失败' + text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('1 row'), 3, '执行失败' + text)

        flg = f'FATAL:  publication "{self.pubname1}" does not exist'
        result = self.com_pub.find_pglog_content(
            node=self.pri_userdb_sub,
            content=flg, env_path=macro.DB_ENV_PATH_REMOTE1,
            path=self.dir_new)
        self.assertTrue(result, '执行失败' + text)

        text = '--step11:删除订阅sub1  expect:成功--'
        self.log.info(text)
        sql = f"drop SUBSCRIPTION {self.subname1};" \
            f"select pg_sleep(30);"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.drop_sub_succ_msg, result, '执行失败' + text)

        text = "--step12:修改数据，并查询同步情况 " \
               "expect:集群A插入成功，(22, '66', '中文', 'test');被同步到集群B--"
        self.log.info(text)
        sql = f"insert into {self.tb_name1} values(22, '66', '中文', 'test');" \
            f"select * from pg_replication_slots ;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         1, '执行失败' + text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('1 row'), 2, '执行失败' + text)
        self.assertEqual(result.count('2 rows'), 1, '执行失败' + text)
        self.assertIn('22 | 66           | 中文   | test',
                      result, '执行失败' + text)
        self.assertIn(' 3 | 6^^&         | 中文   | test',
                      result, '执行失败' + text)

        text = '--step13:删除发布 expect:成功--'
        self.log.info(text)
        sql = f"drop PUBLICATION if exists {self.pubname2} RESTRICT;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)

        text = "--step14:修改数据 expect:成功--"
        self.log.info(text)
        sql = f"insert into {self.tb_name1} values(35, '6ddd&', '中文', 'test');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         1, '执行失败' + text)

        text = "--step15:查询同步 expect:未同步--"
        self.log.info(text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('1 row'), 2, '执行失败' + text)
        self.assertEqual(result.count('2 rows'), 1, '执行失败' + text)
        self.assertIn('22 | 66           | 中文   | test',
                      result, '执行失败' + text)
        self.assertIn(' 3 | 6^^&         | 中文   | test',
                      result, '执行失败' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"DROP PUBLICATION if exists {self.pubname1};" \
            f"DROP PUBLICATION if exists {self.pubname2};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP SUBSCRIPTION  {self.subname1};" \
            f"DROP SUBSCRIPTION  {self.subname2};"
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
        result1 = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f"log_directory='{self.log_directory}'",
            self.hostname, False, False,
            macro.DB_INSTANCE_PATH_REMOTE1, '',
            macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result and result1, '执行失败:' + text)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info("-Opengauss_Function_Pub_Sub_Case0042 end-")

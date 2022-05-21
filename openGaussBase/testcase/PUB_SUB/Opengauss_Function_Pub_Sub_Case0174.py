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
Case Name   : 以二进制模式传输存在不支持表时使用For all tables创建发布
Description :
    1.在两个集群创建表
    2.创建发布端
    3.创建订阅指定以二进制模式传输
    4.修改表数据
    5.查询是否同步
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.tb_pubsub_case174_3/4更新，其余表格不更新，视图可正常查询，
    物化视图refresh不同步，执行刷新后可查询到正确结果
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
        self.tb_name = []
        for i in range(5):
            self.tb_name.append(f'tb_pubsub_case174_{i}')
        self.mv_name1 = 'mv_pubsub_case174_1'
        self.mv_name2 = 'mv_pubsub_case174_2'
        self.subname = "sub_case174"
        self.pubname = "pub_case174"
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

        text1 = '--step1:两个集群均创建表 expect:成功--'
        self.log.info(text1)
        sql_create = f"create UNLOGGED table {self.tb_name[0]}" \
            f"(i int primary key, t text);" \
            f"create GLOBAL temp table  {self.tb_name[1]}" \
            f"(i int primary key, t text);" \
            f"create local temp table  {self.tb_name[2]}" \
            f"(i int primary key, t text);" \
            f"create table {self.tb_name[3]}(i int primary key, t text) " \
            f"WITH (STORAGE_TYPE='astore');" \
            f"create table {self.tb_name[4]}" \
            f"(i int primary key, id int, t text) WITH (segment=on);" \
            f"CREATE VIEW {self.mv_name1}  as " \
            f"select * from {self.tb_name[3]};" \
            f"CREATE MATERIALIZED VIEW {self.mv_name2} " \
            f"AS select * from {self.tb_name[4]};"

        text = '--step2:创建发布端 expect:成功--'
        self.log.info(text)        
        sql = f"CREATE PUBLICATION {self.pubname} FOR ALL TABLES;"
        result = self.commsh_pub.execut_db_sql(sql, 
                                               self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = '--step3:创建订阅指定以二进制模式传输 expect:成功--'
        self.log.info(text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"CREATE SUBSCRIPTION {self.subname} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.ssh_password}' " \
            f"PUBLICATION {self.pubname} with (binary=True);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)

        text = '--step4:修改表数据 expect:成功--'
        self.log.info(text)
        sql_modify = f"insert into {self.tb_name[0]} values(1, 'first');" \
            f"insert into {self.tb_name[1]} values(1, 'first');" \
            f"insert into {self.tb_name[2]} values(1,  'first');" \
            f"insert into {self.tb_name[3]} values(1, 'first');" \
            f"insert into {self.tb_name[4]} values(1, 1, 'first');" \
            f"REFRESH MATERIALIZED VIEW {self.mv_name2};"
        pub_thread = ComThread(self.commsh_pub.execut_db_sql,
                               args=(sql_create + sql_modify,
                                     self.user_param_pub))
        pub_thread.setDaemon(True)
        pub_thread.start()
        pub_thread.join(30)
        result = pub_thread.get_result()
        self.log.info(result)
        self.assertEqual(result.count(self.constant.CREATE_TABLE_SUCCESS),
                         10, '执行失败:' + text1)
        self.assertEqual(result.count(self.constant.CREATE_VIEW_SUCCESS_MSG),
                         1, '执行失败:' + text1)
        self.assertEqual(result.count('CREATE MATERIALIZED VIEW'),
                         1, '执行失败:' + text1)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         5, '执行失败:' + text)
        self.assertEqual(result.count('REFRESH MATERIALIZED VIEW'),
                         1, '执行失败:' + text)

        text = '--step5:查询是否同步 ' \
               'expect:tb_pubsub_case174_3/4更新，' \
               '其余表格不更新，视图可正常查询，物化视图refresh不同步，' \
               '执行刷新后可查询到正确结果'
        self.log.info(text)
        sql_select = f"select pg_sleep(10);" \
            f"select * from {self.tb_name[0]};" \
            f"select * from {self.tb_name[1]};" \
            f"select * from {self.tb_name[2]};" \
            f"select * from {self.tb_name[3]};" \
            f"select * from {self.tb_name[4]};" \
            f"select * from {self.mv_name1};" \
            f"select * from {self.mv_name2};" \
            f"REFRESH MATERIALIZED VIEW {self.mv_name2};" \
            f"select * from {self.mv_name2};"
        sub_thread = ComThread(self.commsh_sub.execut_db_sql,
                               args=(sql_create + sql_select,
                                     self.user_param_sub, None,
                                     macro.DB_ENV_PATH_REMOTE1))
        sub_thread.setDaemon(True)
        sub_thread.start()
        sub_thread.join(30)
        result = sub_thread.get_result()
        self.log.info(result)
        self.assertEqual(result.count(self.constant.CREATE_TABLE_SUCCESS),
                         10, '执行失败:' + text1)
        self.assertEqual(result.count(self.constant.CREATE_VIEW_SUCCESS_MSG),
                         1, '执行失败:' + text1)
        self.assertEqual(result.count('CREATE MATERIALIZED VIEW'),
                         1, '执行失败:' + text1)
        self.assertIn('1 |  1 | first', result.splitlines()[-17],
                      '执行失败:' + text)
        self.assertIn('1 | first', result.splitlines()[-22], '执行失败:' + text)
        self.assertIn('0 rows', result.splitlines()[-7], '执行失败:' + text)
        self.assertIn('1 | first', result.splitlines()[-12], '执行失败:' + text)
        self.assertIn('1 |  1 | first', result.splitlines()[-2],
                      '执行失败:' + text)
        self.assertEqual(result.count('REFRESH MATERIALIZED VIEW'),
                         1, '执行失败:' + text)
        self.assertEqual(result.count('1 row'), 5, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"DROP PUBLICATION if exists {self.pubname};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP SUBSCRIPTION  {self.subname};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        drop_result_sub = []
        drop_result_pub = []
        sql = f"drop view {self.mv_name1};" \
            f"drop MATERIALIZED  view {self.mv_name2};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        for i in range(5):
            sql = f"DROP table if exists {self.tb_name[i]} CASCADE;"
            drop_result_sub.append(
                self.commsh_sub.execut_db_sql(
                    sql, self.user_param_sub, None,
                    macro.DB_ENV_PATH_REMOTE1))
            self.log.info(drop_result_sub[i])
            drop_result_pub.append(self.commsh_pub.execut_db_sql(
                sql, sql_type=self.user_param_pub))
            self.log.info(drop_result_pub[i])
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result)
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.pri_userdb_sub.db_user} '
            f'{self.pri_userdb_sub.db_host}/32 ')
        self.log.info(guc_res)
        guc_res1 = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_pub.db_host}/32',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res1)
        self.assertTrue(guc_res, '执行失败:' + text)
        self.assertTrue(guc_res1, '执行失败:' + text)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        for i in range(5):
            self.assertIn(self.constant.DROP_TABLE_SUCCESS,
                          drop_result_pub[i], '执行失败:' + text)
            self.assertIn(self.constant.DROP_TABLE_SUCCESS,
                          drop_result_sub[i], '执行失败:' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

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
Case Name   : 创建新订阅，订阅端参数enabled验证
Description :
    1、创建用户，赋予所有权限
    2、在两个集群中创建相同字段表
    3、多个订阅，订阅同一个发布
    3.1:创建发布端(集群A)    expect:成功
    3.2.创建多个订阅，对应于同一个发布（集群B）   expect:创建订阅成功
    3.3:向发布端表中插入数据   expect:成功
    3.4:查询集群B中表中数据是否同步   expect:数据已同步
    4、创建1个订阅，订阅不同库的发布
    4.1:创建多个发布端（集群A不同数据库下，存在表关系）   expect:成功
    4.2:创建一个订阅，对应于不同的发布（集群B）   expect:创建订阅成功
    4.3:向发布端表中插入数据   expect:成功
    4.4:查询集群B中表中数据是否同步   expect:数据已同步(三个发布端涉及到的表数据 全部订阅成功，订阅端需要在不同的库中创建同字段表)
    5、创建1个订阅，订阅相同库的多个发布
    5.1:创建多个发布端（集群A同个库下）   expect:成功
    5.2:创建一个订阅，对应于多个发布（集群B）   expect:创建订阅成功
    5.3:向发布端表中插入数据   expect:成功
    5.4:查询集群B中表中数据是否同步   expect:数据已同步，同步数据为3个发布的内容
Expect      :
    1：成功
    2：成功
    3.1：成功
    3.2：创建订阅成功
    3.3：插入数据成功
    3.4：数据同步成功
    4.1：成功
    4.2：创建订阅成功
    4.3：插入数据成功
    4.4：成功，数据同步
    5.1：成功
    5.2：创建订阅成功
    5.3：插入数据成功
    5.4：成功，数据同步
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
        self.subname = ["sub_case103_1", "sub_case103_2", "sub_case103_3"]
        self.pubname = ["pub_case103_1", "pub_case103_2", "pub_case103_3"]
        self.tb_name = ["public.t_case103_1", "public.t_case103_2",
                        "public.t_case103_3"]
        self.db_name1 = "db_case103_1"
        self.port = str(int(self.pri_userdb_pub.db_port) + 1)
        self.wal_level = self.com_pub.show_param("wal_level")
        self.user_name = "u_case103_1"
        self.user_param_u = f'-U {self.user_name} ' \
            f'-W {macro.COMMON_PASSWD}'
        self.user_param_pub = f'-U {self.pri_userdb_pub.db_user} ' \
            f'-W {self.pri_userdb_pub.db_password}'
        self.user_param_sub = f'-U {self.pri_userdb_sub.db_user} ' \
            f'-W {self.pri_userdb_sub.db_password}'

    def test_pubsub(self):
        text = '--step:预置条件,修改pg_hba expect:成功'
        self.log.info(text)
        self.log.info("#######发布端: ")
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.user_name} '
            f'{self.pri_userdb_sub.db_host}/32 sha256')
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    {self.pri_userdb_pub.db_name}  {self.user_name} '
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
        self.log.info("#######订阅端: ")
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.user_name} '
            f'{self.pri_userdb_pub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host {self.pri_userdb_sub.db_name}  {self.user_name} '
            f'{self.pri_userdb_sub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)

        text = "--step1:创建用户，赋予所有权限 expect:成功--"
        self.log.info(text)
        sql = f"create user {self.user_name} password " \
            f"'{macro.COMMON_PASSWD}';" \
            f"grant all privileges to {self.user_name};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      '执行失败:' + text)

        text = '--step2:在两个集群中创建相同字段表 expect:成功--'
        self.log.info(text)
        create_sql = f'create database {self.db_name1};'
        result = self.commsh_pub.execut_db_sql(
            create_sql, sql_type=self.user_param_u)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS,
                      result, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(create_sql,
                                               self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS,
                      result, '执行失败:' + text)
        for i in range(3):
            create_sql = f'create table {self.tb_name[i]}' \
                f'(id int primary key,name text);'
            result = self.commsh_pub.execut_db_sql(
                create_sql, sql_type=self.user_param_u, dbname=self.db_name1)
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                          result, '执行失败:' + text)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)
            result = self.commsh_pub.execut_db_sql(
                create_sql, sql_type=self.user_param_u)
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                          result, '执行失败:' + text)
            result = self.commsh_sub.execut_db_sql(create_sql,
                                                   self.user_param_u, None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                          result, '执行失败:' + text)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)
            result = self.commsh_sub.execut_db_sql(create_sql,
                                                   self.user_param_u,
                                                   self.db_name1,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                          result, '执行失败:' + text)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)

        text = "--step3.1:创建发布端(集群A)    expect:成功--"
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname[0]} for all tables ;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_u)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = "--step3.1:创建发布端(集群A)    expect:成功--"
        self.log.info(text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        for i in range(3):
            sql = f"CREATE SUBSCRIPTION {self.subname[i]} CONNECTION " \
                f"'host={self.pri_userdb_pub.db_host} " \
                f"port={self.port} " \
                f"user={self.user_name} " \
                f"dbname={self.pri_userdb_pub.db_name} " \
                f"password={macro.COMMON_PASSWD}' " \
                f"PUBLICATION {self.pubname[0]};"
            result = self.commsh_sub.execut_db_sql(sql, self.user_param_u,
                                                   None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                          '执行失败:' + text)
            self.assertIn(self.constant.create_sub_succ_msg, result,
                          '执行失败:' + text)

        text = "--step3.3:向发布端表中插入数据   expect:成功--"
        self.log.info(text)
        sql_insert = f"insert into {self.tb_name[0]} " \
            f"values(generate_series(1,100),'a_'||generate_series(1,100));"
        result = self.commsh_pub.execut_db_sql(sql_insert,
                                               sql_type=self.user_param_u)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result, '执行失败' + text)

        text = "--step3.4:查询集群B中表中数据是否同步   expect:数据已同步--"
        self.log.info(text)
        sql_select = f"select count(*) from {self.tb_name[0]}"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_u,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('100', result, '执行失败' + text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_u,
                                               self.db_name1,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn('100', result, '执行失败' + text)

        text = "--step4.1:创建多个发布端（集群A不同数据库下，存在表关系）   expect:成功--"
        self.log.info(text)
        sql = f"drop PUBLICATION {self.pubname[0]};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_u)
        self.log.info(result)
        self.assertIn(self.constant.drop_pub_succ_msg, result,
                      '执行失败:' + text)
        db_list = [self.pri_userdb_pub.db_name, self.db_name1]
        for i in range(2):
            sql = f"select pg_sleep(10);" \
                f"CREATE PUBLICATION {self.pubname[i]} for all tables ;"
            result = self.commsh_pub.execut_db_sql(sql,
                                                   self.user_param_u,
                                                   db_list[i])
            self.log.info(result)
            self.assertIn(self.constant.create_pub_succ_msg, result,
                          '执行失败:' + text)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)

        text = "--step4.2:创建一个订阅，对应于不同的发布（集群B）   expect:创建订阅成功--"
        self.log.info(text)
        for i in range(3):
            sql = f"drop SUBSCRIPTION if exists {self.subname[i]};"
            result = self.commsh_sub.execut_db_sql(sql, self.user_param_u,
                                                   None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            self.assertIn(self.constant.drop_sub_succ_msg, result,
                             '执行失败:' + text)
        for i in range(2):
            sql = f"select pg_sleep(5);" \
                f"CREATE SUBSCRIPTION {self.subname[i]} CONNECTION " \
                f"'host={self.pri_userdb_pub.db_host} " \
                f"port={self.port} " \
                f"user={self.user_name} " \
                f"dbname={db_list[i]} " \
                f"password={macro.COMMON_PASSWD}' " \
                f"PUBLICATION {self.pubname[i]};"
            result = self.commsh_sub.execut_db_sql(sql, self.user_param_u,
                                                   None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)
            self.assertIn(self.constant.create_sub_succ_msg, result,
                             '执行失败:' + text)

        text = "--step4.3:向发布端表中插入数据   expect:成功--"
        self.log.info(text)
        sql_insert = f"select * from pg_replication_slots ;" \
            f"delete from {self.tb_name[0]}; select pg_sleep(5.5);"
        result = self.commsh_pub.execut_db_sql(sql_insert,
                                               sql_type=self.user_param_u)
        self.log.info(result)
        self.assertIn(self.constant.DELETE_SUCCESS_MSG, result, '执行失败' + text)
        sql_insert = f"insert into {self.tb_name[0]} values(1, 'a');"
        result = self.commsh_pub.execut_db_sql(sql_insert,
                                               sql_type=self.user_param_u,
                                               dbname=self.db_name1)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result, '执行失败' + text)

        text = "--step4.4:查询集群B中表中数据是否同步   expect:数据已同步(三个发布端涉及到的表数据" \
               " 全部订阅成功，订阅端需要在不同的库中创建同字段表)--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name[0]}"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_u,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('1 row', result, '执行失败' + text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_u,
                                               self.db_name1,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('0 rows', result, '执行失败' + text)

        text = "--step5.1:创建多个发布端（集群A同个库下）   expect:成功--"
        self.log.info(text)
        for i in range(3):
            sql = f"drop PUBLICATION if exists {self.pubname[i]};"
            result = self.commsh_pub.execut_db_sql(sql,
                                                   sql_type=self.user_param_u)
            self.log.info(result)
            self.assertIn(self.constant.drop_pub_succ_msg, result,
                          '执行失败:' + text)
            result = self.commsh_pub.execut_db_sql(sql,
                                                   sql_type=self.user_param_u,
                                                   dbname=self.db_name1)
            self.log.info(result)
            self.assertIn(self.constant.drop_pub_succ_msg, result,
                          '执行失败:' + text)
        for i in range(3):
            sql = f"CREATE PUBLICATION {self.pubname[i]} for " \
                f"table {self.tb_name[i]} ;"
            result = self.commsh_pub.execut_db_sql(sql,
                                                   sql_type=self.user_param_u)
            self.log.info(result)
            self.assertIn(self.constant.create_pub_succ_msg, result,
                          '执行失败:' + text)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)

        text = "--step5.2:创建一个订阅，对应于多个发布（集群B）   expect:创建订阅成功--"
        self.log.info(text)
        for i in range(3):
            sql = f"drop SUBSCRIPTION if exists {self.subname[i]};"
            result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            self.assertIn(self.constant.drop_sub_succ_msg, result,
                          '执行失败:' + text)
        sql = f"select pg_sleep(5);" \
            f"CREATE SUBSCRIPTION {self.subname[1]} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.user_name} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={macro.COMMON_PASSWD}' " \
            f"PUBLICATION {self.pubname[0]},{self.pubname[1]}," \
            f"{self.pubname[2]};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        self.assertIn(self.constant.create_sub_succ_msg, result,
                      '执行失败:' + text)

        text = "--step5.3:向发布端表中插入数据   expect:成功--"
        self.log.info(text)
        for i in range(3):
            sql_insert = f"insert into {self.tb_name[i]} values({i}, '{i}');" \
                f"select pg_sleep(5.5);"
            result = self.commsh_pub.execut_db_sql(sql_insert,
                                                   sql_type=self.user_param_u)
            self.log.info(result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                          result, '执行失败' + text)

        text = "--step5.4:查询集群B中表中数据是否同步   expect:数据已同步，同步数据为3个发布的内容--"
        self.log.info(text)
        for i in range(3):
            sql_select = f"select * from {self.tb_name[i]}"
            result = self.commsh_sub.execut_db_sql(sql_select,
                                                   self.user_param_u,
                                                   None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            if 0 == i:
                self.assertIn('2 rows', result, '执行失败' + text)
                self.assertIn('1 | a', result, '执行失败' + text)
            else:
                self.assertIn('1 row', result, '执行失败' + text)
            self.assertIn(f'{i} | {i}', result, '执行失败' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = "--环境清理--"
        self.log.info(text)
        for i in range(3):
            sql = f"DROP SUBSCRIPTION if exists {self.subname[i]};" \
                f"DROP table if exists {self.tb_name[i]};"
            drop_sub_result = self.commsh_sub.execut_db_sql(
                sql, self.user_param_u, None, macro.DB_ENV_PATH_REMOTE1)
            self.log.info(drop_sub_result)
            drop_sub_result = self.commsh_sub.execut_db_sql(
                sql, self.user_param_u, self.db_name1,
                macro.DB_ENV_PATH_REMOTE1)
            self.log.info(drop_sub_result)
        for i in range(3):
            sql = f"DROP PUBLICATION if exists {self.pubname[i]};" \
                f"DROP table if exists {self.tb_name[i]};"
            drop_pub_result = self.commsh_pub.execut_db_sql(
                sql, sql_type=self.user_param_u)
            self.log.info(drop_pub_result)
            drop_pub_result = self.commsh_pub.execut_db_sql(
                sql, self.user_param_u, self.db_name1)
            self.log.info(drop_pub_result)
        sql = f"drop database {self.db_name1};"
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_u)
        self.log.info(result)
        result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_u, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        sql = f"drop user {self.user_name};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.user_name} '
            f'{self.pri_userdb_sub.db_host}/32')
        self.log.info(guc_res)
        guc_res1 = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    {self.pri_userdb_pub.db_name}  {self.user_name} '
            f'{self.pri_userdb_sub.db_host}/32')
        self.log.info(guc_res1)
        guc_res2 = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.user_name} '
            f'{self.pri_userdb_pub.db_host}/32 ',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res2)
        guc_res3 = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host {self.pri_userdb_sub.db_name}  {self.user_name} '
            f'{self.pri_userdb_sub.db_host}/32',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res3)
        self.assertTrue(guc_res3 and guc_res2 and guc_res1 and guc_res,
                        '执行失败' + text)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

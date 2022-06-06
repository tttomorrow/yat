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
Case Name   : 双向订阅内容相同
Description :
    1.在两个集群创建表
    2.创建发布端订阅端
    3.修改表数据
    4.查询是否同步
    5.修改数据
    6.修改表数据
    7.修改集群A发布端
    8.修改数据
    9.查看数据是否更新
    10.修改数据
    11.查看数据是否更新
Expect      :
    1.成功
    2.成功
    3.成功
    4.集群B：tb_pubsub_case053_3未更新，其余更新
    5.成功
    6.集群A：tb_pubsub_case053_3未更新，其余更新
    7.成功
    8.成功
    9.tb_pubsub_case053_3未更新，其余更新
    10.成功
    11.集群A：tb_pubsub_case053_2更新，其余未更新
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
        self.log.info("-Opengauss_Function_Pub_Sub_Case0053 start-")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com_pub = Common()
        self.com_sub = Common('remote1_PrimaryDbUser')
        self.tb_name1 = 'tb_pubsub_case053_1'
        self.tb_name2 = 'tb_pubsub_case053_2'
        self.tb_name3 = 'tb_pubsub_case053_3'
        self.subname1 = "sub_case053_1"
        self.pubname1 = "pub_case053_1"
        self.parent_path_pub = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.parent_path_sub = os.path.dirname(macro.DB_INSTANCE_PATH_REMOTE1)
        self.pub_port = str(int(self.pri_userdb_pub.db_port) + 1)
        self.sub_port = str(int(self.pri_userdb_sub.db_port) + 1)
        self.wal_level_pub = self.com_pub.show_param("wal_level")
        self.wal_level_sub = self.com_sub.show_param("wal_level",
                                                     macro.DB_ENV_PATH_REMOTE1)
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
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'wal_level=logical',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.restart_db_cluster(
            True, env_path=macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step1:两个集群均创建表 expect:成功--'
        self.log.info(text)
        sql = f"CREATE TABLE {self.tb_name1}(id NUMBER(7) CONSTRAINT " \
            f"s_longtext_id_nn NOT NULL,  use_filename " \
            f"VARCHAR2(20) primary key, filename VARCHAR2(255), " \
            f"text VARCHAR2(2000)  );" \
            f"CREATE TABLE {self.tb_name2}" \
            f"(like {self.tb_name1} including all);" \
            f"CREATE TABLE {self.tb_name3}(i int primary key, " \
            f"text varchar(1024)) WITH " \
            f"(ORIENTATION = COLUMN, COMPRESSION=HIGH);"
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         6, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         6, '执行失败:' + text)

        text = '--step2:创建发布端订阅端 expect:成功--'
        self.log.info(text)        
        sql = f"CREATE PUBLICATION {self.pubname1} for all tables;"
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
        sql = f"CREATE PUBLICATION {self.pubname1} " \
            f"for table {self.tb_name2},{self.tb_name1};" \
            f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.pub_port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.ssh_password}' " \
            f"PUBLICATION {self.pubname1};"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        result = self.commsh_pub.execute_generate(macro.COMMON_PASSWD)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_sub.db_host} " \
            f"port={self.sub_port} " \
            f"user={self.pri_userdb_sub.db_user} " \
            f"dbname={self.pri_userdb_sub.db_name} " \
            f"password={self.pri_userdb_sub.ssh_password}' " \
            f"PUBLICATION {self.pubname1};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)

        text = '--step3:修改表数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} values(1, " \
            f"'1', '{self.tb_name1}', 'equal');" \
            f"insert into {self.tb_name2} values(1, " \
            f"'1', '{self.tb_name2}', 'equal');" \
            f"insert into {self.tb_name3} values(1, '1');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         3, '执行失败' + text)

        text = "--step4:查询是否同步 expect:集群B：tb_pubsub_case053_3未更新，其余更新--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1};" \
            f"select * from {self.tb_name2};" \
            f"select * from {self.tb_name3};"
        result = self.commsh_pub.execut_db_sql(sql_select,
                                               sql_type=self.user_param_pub)
        self.log.info("集群A查询结果:" + result)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info("集群B查询结果:" + result)
        self.assertEqual(result.count('1 row'), 2, '执行失败' + text)
        self.assertEqual(result.count('0 rows'), 1, '执行失败' + text)
        self.assertIn(f'1 | 1            | {self.tb_name1} | equal',
                      result, '执行失败' + text)
        self.assertIn(f'1 | 1            | {self.tb_name2} | equal',
                      result, '执行失败' + text)

        text = '--step5:修改表数据expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} values(2, " \
            f"'2', '{self.tb_name1}2', 'equal2');" \
            f"insert into {self.tb_name2} values(2, " \
            f"'2', '{self.tb_name2}2', 'equal2');" \
            f"insert into {self.tb_name3} values(2, '2');"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         3, '执行失败' + text)

        text = "--step6:查询是否同步 expect:集群A：tb_pubsub_case053_3未更新，其余更新--"
        self.log.info(text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info("集群B查询结果:" + result)

        result = self.commsh_pub.execut_db_sql(sql_select,
                                               sql_type=self.user_param_pub)
        self.log.info("集群A查询结果:" + result)
        self.assertEqual(result.count('1 row'), 1, '执行失败' + text)
        self.assertEqual(result.count('2 rows'), 2, '执行失败' + text)
        self.assertIn(f'2 | 2            | {self.tb_name2}2 | equal2',
                      result, '执行失败' + text)
        self.assertIn(f'2 | 2            | {self.tb_name1}2 | equal2',
                      result, '执行失败' + text)

        text = '--step7:修改集群B发布端 expect:成功--'
        self.log.info(text)
        sql = f"alter PUBLICATION {self.pubname1} drop table {self.tb_name1};"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.alter_pub_succ_msg,
                      result, '执行失败' + text)

        text = '--step8:修改表数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} values(3, " \
            f"'3', '{self.tb_name1}3', 'equal3');" \
            f"insert into {self.tb_name2} values(3, " \
            f"'3', '{self.tb_name2}3', 'equal3');" \
            f"insert into {self.tb_name3} values(3, '3');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         3, '执行失败' + text)

        text = "--step9:查询是否同步 expect:tb_pubsub_case053_3未更新，其余更新--"
        self.log.info(text)
        result = self.commsh_pub.execut_db_sql(sql_select,
                                               sql_type=self.user_param_pub)
        self.log.info("集群A查询结果:" + result)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info("集群B查询结果:" + result)
        self.assertEqual(result.count('1 row'), 1, '执行失败' + text)
        self.assertEqual(result.count('3 rows'), 2, '执行失败' + text)
        self.assertIn(f'3 | 3            | {self.tb_name1}3 | equal3',
                      result, '执行失败' + text)
        self.assertIn(f'3 | 3            | {self.tb_name2}3 | equal3',
                      result, '执行失败' + text)

        text = '--step10:修改表数据expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} values(4, " \
            f"'4', '{self.tb_name1}4', 'equal4');" \
            f"insert into {self.tb_name2} values(4, " \
            f"'4', '{self.tb_name2}4', 'equal4');" \
            f"insert into {self.tb_name3} values(4, '4');"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         3, '执行失败' + text)

        text = "--step11:查询是否同步 expect:集群A:tb_pubsub_case053_2更新，其余未更新--"
        self.log.info(text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info("集群B查询结果:" + result)
        result = self.commsh_pub.execut_db_sql(sql_select,
                                               sql_type=self.user_param_pub)
        self.log.info("集群A查询结果:" + result)
        self.assertEqual(result.count('2 rows'), 1, '执行失败' + text)
        self.assertEqual(result.count('3 rows'), 1, '执行失败' + text)
        self.assertEqual(result.count('4 rows'), 1, '执行失败' + text)
        self.assertIn(f'4 | 4            | {self.tb_name2}4 | equal4',
                      result, '执行失败' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"DROP PUBLICATION if exists {self.pubname1};" \
            f"DROP SUBSCRIPTION  {self.subname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP table if exists {self.tb_name2};" \
            f"DROP table if exists {self.tb_name1};"\
            f"DROP table if exists {self.tb_name3};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
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
        result_guc = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level_pub}')
        result_guc1 = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level_sub}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result_guc, '执行失败:' + text)
        self.assertTrue(result_guc1, '执行失败:' + text)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info("-Opengauss_Function_Pub_Sub_Case0053 end-")

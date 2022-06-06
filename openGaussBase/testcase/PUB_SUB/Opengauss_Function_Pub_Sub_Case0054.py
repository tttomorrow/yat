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
Case Name   : 先创建发布订阅再创建表
Description :
    1.创建发布端订阅端
    2.两个集群创建表
    3.创建发布订阅
    4.修改数据
    5.查看数据是否更新
    6.修改发布订阅
    7.修改表数据
    8.查看数据是否更新
Expect      :
    1.失败，提示表不存在
    2.成功
    3.成功
    4.成功
    5.集群B：tb_pubsub_case054_1更新(1, '1', 'tb_pubsub_case050_1', 'equal')，其余未更新
    6.成功
    7.成功
    8.集群B：未更新
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
        self.log.info("-Opengauss_Function_Pub_Sub_Case0054 start-")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com_pub = Common()
        self.tb_name1 = 'tb_pubsub_case054_1'
        self.tb_name2 = 'tb_pubsub_case054_2'
        self.subname1 = "sub_case054_1"
        self.subname2 = "sub_case054_2"
        self.pubname1 = "pub_case054_1"
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

        text = '--step1:创建发布端订阅端 expect:失败，提示表不存在--'
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname1}  " \
            f"FOR  TABLE  {self.tb_name1};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.NOT_EXIST, result,
                      '执行失败:' + text)
        self.assertIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = '--step2:两个集群均创建表 expect:成功--'
        self.log.info(text)
        sql = f"CREATE TABLE {self.tb_name1}(id NUMBER(7) CONSTRAINT " \
            f"s_longtext_id_nn NOT NULL, use_filename VARCHAR2(20) " \
            f"primary key, filename VARCHAR2(255), text VARCHAR2(2000) );" \
            f"CREATE TABLE {self.tb_name2}" \
            f"(like {self.tb_name1} including all);"
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         4, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         4, '执行失败:' + text)

        text = '--step3:创建发布订阅 expect:成功--'
        self.log.info(text)        
        sql = f"CREATE PUBLICATION {self.pubname1}  " \
            f"FOR  TABLE  {self.tb_name1}; "
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
            f"PUBLICATION {self.pubname1};"\
            f"CREATE SUBSCRIPTION {self.subname2} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.ssh_password}' " \
            f"PUBLICATION {self.pubname1};" \
            f"select pg_sleep(10);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.create_sub_succ_msg), 2,
                         '执行失败:' + text)

        text = '--step4:修改表数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} " \
            f"values(1, '1', '{self.tb_name1}', 'equal');" \
            f"insert into {self.tb_name2} " \
            f"values(1, '1', '{self.tb_name2}', 'equal');" \
            f"select pg_sleep(60);" \
            f"select slot_name from pg_replication_slots where active=true; "
        result_fliter = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result_fliter)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                      result_fliter, '执行失败' + text)

        text = "--step5:查询是否同步 " \
               "expect:集群B：tb_pubsub_case054_1更新" \
               "(1, '1', 'tb_pubsub_case050_1', 'equal')，其余未更新--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1};" \
            f"select * from {self.tb_name2};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('0 rows'), 1, '执行失败' + text)
        self.assertEqual(result.count('1 row'), 1, '执行失败' + text)
        self.assertIn(f'1 | 1            | {self.tb_name1} | equal',
                      result, '执行失败' + text)

        text = '--step6:修改发布订阅 expect:成功--'
        self.log.info(text)
        if self.subname1 in result_fliter:
            sql = f"drop SUBSCRIPTION {self.subname1};select pg_sleep(5);"
        else:
            sql = f"drop SUBSCRIPTION {self.subname2};select pg_sleep(5);"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.drop_sub_succ_msg,
                      result, '执行失败' + text)

        text = '--step7:修改表数据 expect:成功--'
        self.log.info(text)
        sql = f"select * from pg_replication_slots ;" \
            f"insert into {self.tb_name1} " \
            f"values(13, '13', '{self.tb_name1}3', 'equal3');" \
            f"insert into {self.tb_name2} " \
            f"values(13, '13', '{self.tb_name2}3', 'equal3');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         2, '执行失败' + text)

        text = "--step8:查询是否同步 expect:未更新--"
        self.log.info(text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('0 rows'), 1, '执行失败' + text)
        self.assertEqual(result.count('1 row'), 1, '执行失败' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"DROP PUBLICATION if exists {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP SUBSCRIPTION  {self.subname1};" \
            f"DROP SUBSCRIPTION  {self.subname2}"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP table if exists {self.tb_name2};" \
            f"DROP table {self.tb_name1};"
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
        self.log.info("-Opengauss_Function_Pub_Sub_Case0054 end-")

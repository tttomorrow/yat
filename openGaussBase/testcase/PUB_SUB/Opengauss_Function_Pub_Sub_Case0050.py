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
Case Name   : 级联订阅，中间发布端被订阅内容与其作为订阅端订阅内容相同
Description :
    1.三个集群创建表
    2.创建发布端订阅端
    3.修改数据
    4.查看数据是否更新
Expect      :
    1.成功
    2.成功
    3.成功
    4.集群B：tb_pubsub_case049_1/tb_pubsub_case049_2更新，其余未更新
    集群C：均未更新
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
        self.pri_userdb_node1 = Node(node='PrimaryDbUser')
        self.pri_userdb_node2 = Node(node='remote1_PrimaryDbUser')
        self.pri_userdb_node3 = Node(node='remote2_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_node1 = CommonSH('PrimaryDbUser')
        self.commsh_node2 = CommonSH('remote1_PrimaryDbUser')
        self.commsh_node3 = CommonSH('remote2_PrimaryDbUser')
        self.com_node1 = Common()
        self.com_node2 = Common('remote1_PrimaryDbUser')
        self.com_node3 = Common('remote2_PrimaryDbUser')
        self.tb_name1 = 'tb_pubsub_case050_1'
        self.tb_name2 = 'tb_pubsub_case050_2'
        self.tb_name3 = 'tb_pubsub_case050_3'
        self.sub_name = "sub_case050_1"
        self.pub_name = "pub_case050_1"
        self.parent_path_node1 = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.parent_path_node2 = \
            os.path.dirname(macro.DB_INSTANCE_PATH_REMOTE1)
        self.parent_path_node3 = \
            os.path.dirname(macro.DB_INSTANCE_PATH_REMOTE2)
        self.port_node1 = str(int(self.pri_userdb_node1.db_port) + 1)
        self.port_node2 = str(int(self.pri_userdb_node2.db_port) + 1)
        self.port_node3 = str(int(self.pri_userdb_node3.db_port) + 1)
        self.wal_level_node1 = self.com_node1.show_param("wal_level")
        self.wal_level_node2 = self.com_node2.show_param(
            "wal_level", macro.DB_ENV_PATH_REMOTE1)
        self.wal_level_node3 = self.com_node3.show_param(
            "wal_level", macro.DB_ENV_PATH_REMOTE2)
        self.user_param_node1 = f'-U {self.pri_userdb_node1.db_user} ' \
            f'-W {self.pri_userdb_node1.db_password}'
        self.user_param_node2 = f'-U {self.pri_userdb_node2.db_user} ' \
            f'-W {self.pri_userdb_node2.db_password}'
        self.user_param_node3 = f'-U {self.pri_userdb_node3.db_user} ' \
            f'-W {self.pri_userdb_node3.db_password}'

        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} " \
            f"{os.path.join(self.parent_path_node1, 'pg_hba.conf')};"
        self.log.info(cmd)
        result = self.pri_userdb_node1.sh(cmd).result()
        self.log.info(result)
        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')}" \
            f" {os.path.join(self.parent_path_node2, 'pg_hba.conf')};"
        self.log.info(cmd)
        result = self.pri_userdb_node2.sh(cmd).result()
        self.log.info(result)
        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE2, 'pg_hba.conf')}" \
            f" {os.path.join(self.parent_path_node3, 'pg_hba.conf')};"
        self.log.info(cmd)
        result = self.pri_userdb_node3.sh(cmd).result()
        self.log.info(result)

    def test_pubsub(self):
        text = '--step:预置条件,修改pg_hba expect:成功'
        self.log.info(text)
        self.log.info("#############node1：")
        guc_res = self.commsh_node1.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.pri_userdb_node2.db_user} '
            f'{self.pri_userdb_node2.db_host}/32 sha256')
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        guc_res = self.commsh_node1.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.pri_userdb_node3.db_user} '
            f'{self.pri_userdb_node3.db_host}/32 sha256')
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        result = self.commsh_node1.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'wal_level=logical')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_node1.restart_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        self.log.info("#############node2：")
        guc_res = self.commsh_node2.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_node1.db_user} '
            f'{self.pri_userdb_node1.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        guc_res = self.commsh_node2.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_node3.db_user} '
            f'{self.pri_userdb_node3.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        result = self.commsh_node2.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'wal_level=logical',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_node2.restart_db_cluster(
            True, env_path=macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        self.log.info("#############node3：")
        guc_res = self.commsh_node3.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE2,
            f'host    replication  {self.pri_userdb_node1.db_user} '
            f'{self.pri_userdb_node1.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE2)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        guc_res = self.commsh_node3.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE2,
            f'host    replication  {self.pri_userdb_node2.db_user} '
            f'{self.pri_userdb_node2.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE2)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        result = self.commsh_node3.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'wal_level=logical',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE2,
            env_path=macro.DB_ENV_PATH_REMOTE2)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_node3.restart_db_cluster(
            True, env_path=macro.DB_ENV_PATH_REMOTE2)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step1:三个集群创建表 expect:成功--'
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
        result = self.commsh_node1.execut_db_sql(
            sql, sql_type=self.user_param_node1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         6, '执行失败:' + text)
        result = self.commsh_node2.execut_db_sql(sql, self.user_param_node2,
                                                 None,
                                                 macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         6, '执行失败:' + text)
        result = self.commsh_node3.execut_db_sql(sql, self.user_param_node3,
                                                 None,
                                                 macro.DB_ENV_PATH_REMOTE2)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         6, '执行失败:' + text)

        text = '--step2:创建发布端订阅端 expect:成功--'
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pub_name} for all tables;"
        result = self.commsh_node1.execut_db_sql(sql,
                                                 sql_type=self.user_param_node1)
        self.log.info('node1: ' + result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        result = self.commsh_node2.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"CREATE PUBLICATION {self.pub_name} for all tables;" \
            f"CREATE SUBSCRIPTION {self.sub_name} CONNECTION " \
            f"'host={self.pri_userdb_node1.db_host} " \
            f"port={self.port_node1} " \
            f"user={self.pri_userdb_node1.db_user} " \
            f"dbname={self.pri_userdb_node1.db_name} " \
            f"password={self.pri_userdb_node1.ssh_password}' " \
            f"PUBLICATION {self.pub_name};"
        result = self.commsh_node2.execut_db_sql(sql,
                                                 self.user_param_node2, None,
                                                 macro.DB_ENV_PATH_REMOTE1)
        self.log.info('node2: ' + result)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        result = self.commsh_node3.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE2)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"CREATE SUBSCRIPTION {self.sub_name} CONNECTION " \
            f"'host={self.pri_userdb_node2.db_host} " \
            f"port={self.port_node2} " \
            f"user={self.pri_userdb_node2.db_user} " \
            f"dbname={self.pri_userdb_node2.db_name} " \
            f"password={self.pri_userdb_node2.ssh_password}' " \
            f"PUBLICATION {self.pub_name};"
        result = self.commsh_node3.execut_db_sql(sql,
                                                 self.user_param_node3, None,
                                                 macro.DB_ENV_PATH_REMOTE2)
        self.log.info('node3: ' + result)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = '--step3:修改数据 expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name1} values(1, " \
            f"'1', '{self.tb_name1}', 'equal');" \
            f"insert into {self.tb_name2} values(1, " \
            f"'1', '{self.tb_name2}', 'equal');" \
            f"insert into {self.tb_name3} values(1, '1');" \
            f"update {self.tb_name1} set use_filename='update';" \
            f"select pg_sleep(10);"
        result = self.commsh_node1.execut_db_sql(sql,
                                                 sql_type=self.user_param_node1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         3, '执行失败' + text)
        self.assertIn(self.constant.UPDATE_SUCCESS_MSG,
                      result, '执行失败:' + text)

        text = "--step4:查看数据是否更新 expect:集群B除tb3其余更新，集群C未更新"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1};" \
            f"select * from {self.tb_name2};" \
            f"select * from {self.tb_name3};"
        result_a = self.commsh_node1.execut_db_sql(sql_select,
                                                 self.user_param_node1)
        self.log.info("node1查询结果:" + result_a)
        self.assertNotIn('0 rows', result_a, '执行失败:' + text)
        result = self.commsh_node2.execut_db_sql(sql_select,
                                                 self.user_param_node2,
                                                 None,
                                                 macro.DB_ENV_PATH_REMOTE1)
        self.log.info("node2查询结果:" + result)
        self.assertEqual(result_a.splitlines()[:-5],
                         result.splitlines()[:-4], '执行失败:' + text)
        self.assertIn('0 rows', result, '执行失败:' + text)
        result = self.commsh_node3.execut_db_sql(sql_select,
                                                 self.user_param_node3,
                                                 None,
                                                 macro.DB_ENV_PATH_REMOTE2)
        self.log.info("node3查询结果:" + result)
        self.assertNotEqual(result_a, result, '执行失败:' + text)
        self.assertNotIn('1 row', result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"DROP PUBLICATION if exists {self.pub_name};" \
            f"DROP SUBSCRIPTION if exists {self.sub_name};"
        drop_pub_result = self.commsh_node1.execut_db_sql(
            sql, sql_type=self.user_param_node1)
        self.log.info(drop_pub_result)
        drop_sub_result = self.commsh_node2.execut_db_sql(
            sql, self.user_param_node2, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        drop_sub_result = self.commsh_node3.execut_db_sql(
            sql, self.user_param_node3, None, macro.DB_ENV_PATH_REMOTE2)
        self.log.info(drop_sub_result)
        sql = f"DROP table if exists {self.tb_name2};" \
            f"DROP table if exists {self.tb_name1};" \
            f"DROP table if exists {self.tb_name3};"
        result = self.commsh_node2.execut_db_sql(sql, self.user_param_node2,
                                                 None,
                                                 macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        result = self.commsh_node3.execut_db_sql(sql, self.user_param_node3,
                                                 None,
                                                 macro.DB_ENV_PATH_REMOTE2)
        self.log.info(result)
        result = self.commsh_node1.execut_db_sql(sql,
                                                 sql_type=self.user_param_node1)
        self.log.info(result)

        cmd = f"mv " \
            f"{os.path.join(self.parent_path_node1, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} "
        self.log.info(cmd)
        result = self.pri_userdb_node1.sh(cmd).result()
        self.log.info(result)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_node2, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')} "
        self.log.info(cmd)
        result = self.pri_userdb_node2.sh(cmd).result()
        self.log.info(result)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_node3, 'pg_hba.conf')} " \
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE2, 'pg_hba.conf')} "
        self.log.info(cmd)
        result = self.pri_userdb_node3.sh(cmd).result()
        self.log.info(result)
        result_guc = self.commsh_node1.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level_node1}')
        result_guc1 = self.commsh_node2.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level_node2}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        result_guc2 = self.commsh_node3.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level_node3}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE2,
            env_path=macro.DB_ENV_PATH_REMOTE2)
        self.commsh_node1.restart_db_cluster(True)
        self.commsh_node2.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.commsh_node3.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE2)
        self.assertTrue(result_guc, '执行失败:' + text)
        self.assertTrue(result_guc1 and result_guc2, '执行失败:' + text)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

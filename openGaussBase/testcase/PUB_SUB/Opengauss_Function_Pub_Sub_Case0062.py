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
Case Name   : 开启发布订阅后，订阅端主备切换
Description :
    1.两个集群创建表
    2.创建发布订阅
    3.更新数据
    4.查询数据是否更新
    5.订阅端主备切换
    6.更新数据
    7.查询数据是否更新
    8.恢复主备关系
    9.更新数据
    10.查询数据是否更新
Expect      :
    1.成功
    2.成功
    3.成功
    4.更新
    5.成功
    6.成功
    7.数据更新
    8.成功
    9.成功
    10.更新
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
        self.sta_userdb_pub = Node(node='Standby1DbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.sta_userdb_sub = Node(node='remote1_Standby1DbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.commsh_sub_sta = CommonSH('remote1_Standby1DbUser')
        self.com_pub = Common()
        self.com_sub = Common('remote1_PrimaryDbUser')
        self.tb_name1 = 'tb_pubsub_case062_1'
        self.tb_name2 = 'tb_pubsub_case062_2'
        self.subname = "sub_case062_1"
        self.pubname = "pub_case062_1"
        self.port = str(int(self.pri_userdb_pub.db_port) + 1)
        self.wal_level = self.com_pub.show_param("wal_level")
        self.enable_slot_log_pub = self.com_pub.show_param("enable_slot_log")
        self.enable_slot_log_sub = self.com_sub.show_param(
            "enable_slot_log", macro.DB_ENV_PATH_REMOTE1)
        self.user_param_pub = f'-U {self.pri_userdb_pub.db_user} ' \
            f'-W {self.pri_userdb_pub.db_password}'
        self.user_param_sub = f'-U {self.pri_userdb_sub.db_user} ' \
            f'-W {self.pri_userdb_sub.db_password}'
        self.hostname = self.com_pub.get_sh_result(self.pri_userdb_sub,
                                                   'hostname')

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
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.sta_userdb_sub.db_host}/32 sha256')
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
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.sta_userdb_pub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)

        text1 = '--step1:两个集群均创建表 expect:成功--'
        self.log.info(text1)
        sql = f"CREATE TABLE {self.tb_name1}(id1 INT primary key, " \
            f"id2 INT, id3 INT);" \
            f"CREATE TABLE {self.tb_name2}(id int primary key " \
            f"CONSTRAINT id_nn NOT NULL,use_filename VARCHAR2(20)," \
            f"filename VARCHAR2(255),text VARCHAR2(2000))" \
            f"PARTITION BY RANGE(id)(        " \
            f"PARTITION P1 VALUES LESS THAN(30),        " \
            f"PARTITION P2 VALUES LESS THAN(60),        " \
            f"PARTITION P3 VALUES LESS THAN(90),        " \
            f"PARTITION P4 VALUES LESS THAN(MAXVALUE));"
        result = self.commsh_pub.execut_db_sql(sql,
                                               self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.CREATE_TABLE_SUCCESS),
                      4, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.CREATE_TABLE_SUCCESS),
                      4, '执行失败:' + text)

        text = '--step2:创建发布订阅 expect:成功--'
        self.log.info(text)
        result = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, 'enable_slot_log=on')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            'enable_slot_log=on',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        sql = f"CREATE PUBLICATION {self.pubname} FOR ALL TABLES;"
        result = self.commsh_pub.execut_db_sql(sql, 
                                               self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        result = self.commsh_sub_sta.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"CREATE SUBSCRIPTION {self.subname} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.ssh_password}' " \
            f"PUBLICATION {self.pubname};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)

        text = '--step3:更新数据 expect:成功--'
        self.log.info(text)
        sql_modify = f"insert into {self.tb_name1} values(1, 1, 1),(2,2,2);" \
            f"select pg_sleep(5.5);" \
            f"insert into {self.tb_name2} values(1, 'first', '%一', '')," \
            f"(60, 'first', '%二', ''),(90, 'first', '%三', ''); "
        result = self.commsh_pub.execut_db_sql(sql_modify, self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         2, '执行失败:' + text)

        text = '--step4:查询数据是否更新  expect:更新'
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1};" \
            f"select * from {self.tb_name2};"
        result = self.commsh_sub.execut_db_sql(
            sql_select, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('2 rows'), 1, '执行失败:' + text)
        self.assertEqual(result.count('3 rows'), 1, '执行失败:' + text)

        text = '--step5:订阅端备升主  expect:成功'
        self.log.info(text)
        result = self.commsh_sub.stop_db_instance(
            env_path=macro.DB_ENV_PATH_REMOTE1,
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1)
        self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG,
                      result, '执行失败:' + text)
        result = self.commsh_sub_sta.execute_gsctl(
            'failover', self.constant.FAILOVER_SUCCESS_MSG,
            env_path=macro.DB_ENV_PATH_REMOTE1,
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub_sta.exec_refresh_conf(
            macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)

        text = '--step6:更新数据 expect:成功--'
        self.log.info(text)
        sql_modify = f"delete from {self.tb_name1} where id1=1;" \
            f"delete from {self.tb_name2} where id=1; "
        result = self.commsh_pub.execut_db_sql(sql_modify, self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.DELETE_SUCCESS_MSG),
                         2, '执行失败:' + text)

        text = '--step7:查询数据是否更新  expect:数据更新--'
        self.log.info(text)
        result = self.commsh_sub_sta.execut_db_sql(
            sql_select, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('2 rows'), 1, '执行失败:' + text)
        self.assertEqual(result.count('1 row'), 1, '执行失败:' + text)
        self.assertNotIn('1 |   1 |   1', result, '执行失败:' + text)
        self.assertNotIn('1 | first        | %一     |', result, '执行失败:' + text)

        text = '--step8:恢复主备关系  expect:成功'
        self.log.info(text)
        result = self.commsh_sub.start_db_instance(
            'standby',
            macro.DB_ENV_PATH_REMOTE1,
            macro.DB_INSTANCE_PATH_REMOTE1)
        self.assertIn(self.constant.BUILD_SUCCESS_MSG, result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsctl(
            'switchover', self.constant.SWITCHOVER_SUCCESS_MSG,
            env_path=macro.DB_ENV_PATH_REMOTE1,
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.exec_refresh_conf(macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)

        text = '--step9:更新数据 expect:成功--'
        self.log.info(text)
        sql_modify = f"update {self.tb_name1} set id3=999;" \
            f"update {self.tb_name2} set id=999 where id=90;"
        result = self.commsh_pub.execut_db_sql(sql_modify, self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.UPDATE_SUCCESS_MSG),
                         2, '执行失败:' + text)

        text = '--step10:查询数据是否更新  expect:更新--'
        self.log.info(text)
        result = self.commsh_sub.execut_db_sql(
            sql_select, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('1 row'), 1, '执行失败:' + text)
        self.assertEqual(result.count('2 rows'), 1, '执行失败:' + text)
        self.assertIn('2 |   2 | 999', result, '执行失败:' + text)
        self.assertIn('999 | first        | %三     |',
                      result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        result = self.commsh_sub.check_whether_need_switch(
            self.hostname, envpath=macro.DB_ENV_PATH_REMOTE1)
        result_switch = True
        result_refresh = True
        if result:
            self.commsh_sub.start_db_instance(
                'standby',
                macro.DB_ENV_PATH_REMOTE1,
                macro.DB_INSTANCE_PATH_REMOTE1)
            result_switch = self.commsh_sub.execute_gsctl(
                'switchover', self.constant.SWITCHOVER_SUCCESS_MSG,
                env_path=macro.DB_ENV_PATH_REMOTE1,
                dn_path=macro.DB_INSTANCE_PATH_REMOTE1)
            self.log.info(result_switch)
            result_refresh = self.commsh_sub.exec_refresh_conf(
                macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result_refresh)
        sql = f"DROP SUBSCRIPTION  {self.subname};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP PUBLICATION if exists {self.pubname};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP table if exists {self.tb_name1} CASCADE;" \
            f"DROP table if exists {self.tb_name2} CASCADE;"
        result_drop1 = self.commsh_sub.execut_db_sql(sql, self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result_drop1)
        result_drop2 = self.commsh_pub.execut_db_sql(sql, self.user_param_pub)
        self.log.info(result_drop2)
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result)
        result2 = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            f'enable_slot_log={self.enable_slot_log_pub}')
        result3 = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            f'enable_slot_log={self.enable_slot_log_sub}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        guc_res1 = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_sub.db_host}/32')
        self.log.info(guc_res1)
        guc_res2 = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.sta_userdb_sub.db_host}/32 ')
        self.log.info(guc_res2)
        guc_res3 = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_pub.db_host}/32',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res3)
        guc_res4 = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.sta_userdb_pub.db_host}/32',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res4)
        self.assertTrue(guc_res2 and guc_res1 and guc_res3 and guc_res4,
                        '执行失败:' + text)
        self.assertTrue(result2 and result3, '执行失败:' + text)
        self.assertTrue(result_refresh and result_switch, '执行失败:' + text)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS,
                      result_drop2, '执行失败:' + text)
        self.assertIn(self.constant.DROP_TABLE_SUCCESS,
                      result_drop1, '执行失败:' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

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
Case Name   : 发布行迁移分区表
Description :
    1.发布端创建表
    2.订阅端创建表
    3.创建发布端
    4.创建订阅
    5.修改表数据
    6.查询是否同步
    7.修改表数据
    8.查询是否同步
    9.修改表数据
    10.查询是否同步
    11.修改表数据
    12.查询是否同步
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.更新
    7.成功
    8.更新为(90, 'en_dis', 'insert')
    9.insert成功update失败
    10.(1, 'en_dis', 'insert')
    11.insert成功update失败
    12.(1, 'en_dis', 'insert')
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
        self.tb_name_en_dis = 'tb_pubsub_case012_en_dis'
        self.tb_name_en_en = 'tb_pubsub_case012_en_en'
        self.tb_name_dis_en = 'tb_pubsub_case012_dis_en'
        self.tb_name_dis_dis = 'tb_pubsub_case012_dis_dis'
        self.subname = "sub_case012"
        self.pubname = "pub_case012"
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

        text = '--step1:发布端创建表 expect:成功--'
        self.log.info(text)
        sql = f"CREATE TABLE {self.tb_name_en_dis}(id int primary key " \
            f"CONSTRAINT id_nn NOT NULL, use_filename VARCHAR2(20)," \
            f"filename VARCHAR2(255),text VARCHAR2(2000))" \
            f"PARTITION BY RANGE(id)(PARTITION P1 VALUES LESS THAN(30)," \
            f"PARTITION P2 VALUES LESS THAN(60)," \
            f"PARTITION P3 VALUES LESS THAN(90)," \
            f"PARTITION P4 VALUES LESS THAN(MAXVALUE))  ENABLE ROW MOVEMENT;" \
            f"CREATE TABLE {self.tb_name_en_en}(id int " \
            f"primary key CONSTRAINT id_nn NOT NULL," \
            f"use_filename VARCHAR2(20),filename VARCHAR2(255)," \
            f"text VARCHAR2(2000))PARTITION BY RANGE(id)(" \
            f"PARTITION P1 VALUES LESS THAN(30)," \
            f"PARTITION P2 VALUES LESS THAN(60)," \
            f"PARTITION P3 VALUES LESS THAN(90)," \
            f"PARTITION P4 VALUES LESS THAN(MAXVALUE)" \
            f")ENABLE ROW MOVEMENT;" \
            f"CREATE TABLE {self.tb_name_dis_en}(id int " \
            f"primary key CONSTRAINT id_nn NOT NULL," \
            f"use_filename VARCHAR2(20),filename VARCHAR2(255)," \
            f"text VARCHAR2(2000))PARTITION BY RANGE(id)(" \
            f"PARTITION P1 VALUES LESS THAN(30)," \
            f"PARTITION P2 VALUES LESS THAN(60)," \
            f"PARTITION P3 VALUES LESS THAN(90)," \
            f"PARTITION P4 VALUES LESS THAN(MAXVALUE)" \
            f")DISABLE ROW MOVEMENT;" \
            f"CREATE TABLE {self.tb_name_dis_dis}(id int primary key " \
            f"CONSTRAINT id_nn NOT NULL,use_filename VARCHAR2(20)," \
            f"filename VARCHAR2(255),text VARCHAR2(2000))" \
            f"PARTITION BY RANGE(id)(" \
            f"PARTITION P1 VALUES LESS THAN(30)," \
            f"PARTITION P2 VALUES LESS THAN(60)," \
            f"PARTITION P3 VALUES LESS THAN(90)," \
            f"PARTITION P4 VALUES LESS THAN(MAXVALUE)" \
            f")DISABLE ROW MOVEMENT;"
        result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         8, '执行失败:' + text)

        text = '--step2:订阅端创建表 expect:成功--'
        self.log.info(text)
        sql = f"CREATE TABLE {self.tb_name_en_dis}(id int primary key " \
            f"CONSTRAINT id_nn NOT NULL, use_filename VARCHAR2(20)," \
            f"filename VARCHAR2(255),text VARCHAR2(2000))" \
            f"PARTITION BY RANGE(id)(PARTITION P1 VALUES LESS THAN(30)," \
            f"PARTITION P2 VALUES LESS THAN(60)," \
            f"PARTITION P3 VALUES LESS THAN(90)," \
            f"PARTITION P4 VALUES LESS THAN(MAXVALUE)) " \
            f"DISABLE ROW MOVEMENT;" \
            f"CREATE TABLE {self.tb_name_en_en}(id int " \
            f"primary key CONSTRAINT id_nn NOT NULL," \
            f"use_filename VARCHAR2(20),filename VARCHAR2(255)," \
            f"text VARCHAR2(2000))PARTITION BY RANGE(id)(" \
            f"PARTITION P1 VALUES LESS THAN(30)," \
            f"PARTITION P2 VALUES LESS THAN(60)," \
            f"PARTITION P3 VALUES LESS THAN(90)," \
            f"PARTITION P4 VALUES LESS THAN(MAXVALUE)" \
            f")ENABLE ROW MOVEMENT;" \
            f"CREATE TABLE {self.tb_name_dis_en}(id int " \
            f"primary key CONSTRAINT id_nn NOT NULL," \
            f"use_filename VARCHAR2(20),filename VARCHAR2(255)," \
            f"text VARCHAR2(2000))PARTITION BY RANGE(id)(" \
            f"PARTITION P1 VALUES LESS THAN(30)," \
            f"PARTITION P2 VALUES LESS THAN(60)," \
            f"PARTITION P3 VALUES LESS THAN(90)," \
            f"PARTITION P4 VALUES LESS THAN(MAXVALUE)" \
            f")ENABLE ROW MOVEMENT;" \
            f"CREATE TABLE {self.tb_name_dis_dis}(id int primary key " \
            f"CONSTRAINT id_nn NOT NULL,use_filename VARCHAR2(20)," \
            f"filename VARCHAR2(255),text VARCHAR2(2000))" \
            f"PARTITION BY RANGE(id)(" \
            f"PARTITION P1 VALUES LESS THAN(30)," \
            f"PARTITION P2 VALUES LESS THAN(60)," \
            f"PARTITION P3 VALUES LESS THAN(90)," \
            f"PARTITION P4 VALUES LESS THAN(MAXVALUE)" \
            f")DISABLE ROW MOVEMENT;"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         8, '执行失败:' + text)

        text = '--step3:创建发布端 expect:成功--'
        self.log.info(text)        
        sql = f"CREATE PUBLICATION {self.pubname} " \
            f"FOR all TABLEs;"
        result = self.commsh_pub.execut_db_sql(sql, 
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = '--step4:创建订阅 expect:成功--'
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
            f"PUBLICATION {self.pubname}"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)

        text = '--step5:修改表数据expect:成功--'
        self.log.info(text)
        flg_insert = '  1 | en_dis       | insert   |'
        flg_update = ' 90 | en_dis       | insert   |'
        sql = f"insert into {self.tb_name_en_dis} " \
            f"values(1, 'en_dis', 'insert');select pg_sleep(5.5);"
        result = self.commsh_pub.execut_db_sql(sql, 
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         1, '执行失败'+text)
        sql = f"select * from {self.tb_name_en_dis};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(flg_insert, result, '执行失败' + text)

        text = '--step6:查询是否同步 expect:更新'
        self.log.info(text)
        sql = f"update {self.tb_name_en_dis} set id=90 where id=1; "
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.UPDATE_SUCCESS_MSG, result,
                      '执行失败' + text)
        sql = f"select * from {self.tb_name_en_dis};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(flg_update, result, '执行失败' + text)

        text = '--step7:修改表数据expect:成功--'
        self.log.info(text)
        sql = f"insert into {self.tb_name_en_en} " \
            f"values(1, 'en_dis', 'insert');"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         1, '执行失败' + text)
        sql = f"select * from {self.tb_name_en_en};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(flg_insert, result, '执行失败' + text)

        text = '--step6:查询是否同步 ' \
               'expect:更新为(90, \'en_dis\', \'insert\')'
        self.log.info(text)
        sql = f"update {self.tb_name_en_en} set id=90 where id=1; "
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.UPDATE_SUCCESS_MSG, result,
                      '执行失败' + text)
        sql = f"select * from {self.tb_name_en_en};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(flg_update, result, '执行失败' + text)

        text = '--step9:修改表数据expect:insert成功update失败--'
        self.log.info(text)
        sql = f"insert into {self.tb_name_dis_en} values" \
            f"(1, 'en_dis', 'insert');" \
            f"update {self.tb_name_dis_en} set id=90 where id=1;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         1, '执行失败' + text)
        self.assertIn(self.constant.update_partition_fail_msg, result,
                      '执行失败' + text)

        text = '--step10:查询是否同步 ' \
               'expect:更新为(1, \'en_dis\', \'insert\')'
        self.log.info(text)
        sql = f"select * from {self.tb_name_dis_en};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(flg_insert, result, '执行失败' + text)

        text = '--step11:修改表数据expect:insert成功update失败--'
        self.log.info(text)
        sql = f"insert into {self.tb_name_dis_dis} values" \
            f"(1, 'en_dis', 'insert');" \
            f"update {self.tb_name_dis_dis} set id=90 where id=1;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         1, '执行失败' + text)
        self.assertIn(self.constant.update_partition_fail_msg, result,
                      '执行失败' + text)

        text = '--step11:查询是否同步 ' \
               'expect:更新为(1, \'en_dis\', \'insert\')'
        self.log.info(text)
        sql = f"select * from {self.tb_name_dis_dis};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(flg_insert, result, '执行失败' + text)

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
        sql = f"DROP table  {self.tb_name_dis_dis},{self.tb_name_en_dis}," \
            f"{self.tb_name_en_en},{self.tb_name_dis_en};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
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
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_pub.db_host}/32',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        self.assertTrue(guc_res1, '执行失败:' + text)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

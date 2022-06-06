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
Case Name   : 订阅端使用gs_basebackup备份后并恢复
Description :
    1.在两个集群创建表
    2.发布端打开增量备份开关
    3.订阅端远程备份
    4.更新数据
    5.查询数据是否更新
    6.使用备份文件恢复集群B
    7.更新数据
    8.查询数据是否更新
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.更新
    6.成功
    7.成功
    8.更新
History     :
"""
import unittest
import os
import time
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
        self.log.info("-Opengauss_Function_Pub_Sub_Case0069 start-")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.com_pub = Common()
        self.tb_name1 = 'tb_pubsub_case069_1'
        self.tb_name2 = 'tb_pubsub_case069_2'
        self.tbs_name = 'tps_pubsub_case069'
        self.schema_name1 = 's_pubsub_case069_1'
        self.subname1 = "sub_case069_1"
        self.pubname1 = "pub_case069_1"
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
        self.backup_path = os.path.join(self.parent_path_sub,
                                        'back_pubsub_case069')
        self.comsh_sta_sub = []
        self.nodelist = ['remote1_Standby1DbUser', 'remote1_Standby2DbUser']
        for i in range(2):
            self.comsh_sta_sub.append(CommonSH(self.nodelist[i]))
        self.tbs_path = os.path.join(self.parent_path_pub, self.tbs_name)
        self.tbs_path1 = os.path.join(self.parent_path_sub, self.tbs_name)

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

        text = '--step1:两个集群均创建表 expect:成功--'
        self.log.info(text)
        sql1 = f"create tablespace {self.tbs_name} " \
            f" LOCATION '{self.tbs_path}';"
        sql2 = f"create tablespace {self.tbs_name} " \
            f" LOCATION '{self.tbs_path1}';"
        sql = f"create schema {self.schema_name1};" \
            f"create table {self.schema_name1}.{self.tb_name1}" \
            f"(id1 INT primary key, id2 INT, id3 INT) " \
            f"tablespace {self.tbs_name};" \
            f"create table {self.tb_name2}(id int primary key " \
            f"CONSTRAINT id_nn NOT NULL,use_filename VARCHAR2(20)," \
            f"filename VARCHAR2(255),text VARCHAR2(2000))" \
            f"PARTITION BY RANGE(id)" \
            f"(PARTITION P1 VALUES LESS THAN(30), " \
            f"PARTITION P2 VALUES LESS THAN(60)," \
            f"PARTITION P3 VALUES LESS THAN(90)," \
            f" PARTITION P4 VALUES LESS THAN(MAXVALUE));"
        result = self.commsh_pub.execut_db_sql(
            sql1+sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         5, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql2+sql, self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         5, '执行失败:' + text)

        text = '--step2:创建发布订阅 expect:成功--'
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname1}  " \
            f"FOR  TABLE  {self.tb_name2}," \
            f"{self.schema_name1}.{self.tb_name1} ;"
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
            f"PUBLICATION {self.pubname1};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.create_sub_succ_msg), 1,
                         '执行失败:' + text)

        text = '--step3:订阅端远程备份 expect:成功--'
        self.log.info(text)
        cmd = f"mkdir {self.backup_path};"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        result = self.commsh_sub.exec_gs_basebackup(
            self.backup_path, self.pri_userdb_sub.ssh_host,
            self.pri_userdb_sub.db_port,
            cmd=f'-T {self.tbs_path1}={self.tbs_path1}_new',
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        cmd = f"chmod -R 700 {self.backup_path}"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)

        text = '--step4:更新数据 expect:成功--'
        self.log.info(text)
        sql_insert = f"insert into {self.schema_name1}.{self.tb_name1} " \
            f"values(generate_series(1,100), 1, 1);" \
            f"insert into {self.tb_name2} values(1, 'first', '%一', '')," \
            f"(60, 'first', '%二', ''),(90, 'first', '%三', ''); "
        result = self.commsh_pub.execut_db_sql(sql_insert,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         2, '执行失败' + text)

        text = "--step5:查询数据是否更新 expect:更新--"
        self.log.info(text)
        sql_select = f"select count(*) from " \
            f"{self.schema_name1}.{self.tb_name1};" \
            f"select * from {self.tb_name2};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('3 rows', result, '执行失败' + text)
        self.assertIn('1 | first        | %一     |', result, '执行失败' + text)
        result_a = self.commsh_pub.execut_db_sql(sql_select,
                                               sql_type=self.user_param_pub)
        self.log.info(result_a)
        self.assertEqual(result_a, result, '执行失败' + text)

        text = "--step6:使用备份文件恢复集群B expect:更新--"
        self.log.info(text)
        result = self.commsh_sub.stop_db_cluster(
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        cmd = f"mv {macro.DB_INSTANCE_PATH_REMOTE1} " \
            f"{macro.DB_INSTANCE_PATH_REMOTE1}_bak;" \
            f"mv {self.backup_path} {macro.DB_INSTANCE_PATH_REMOTE1}"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        result = self.commsh_sub.start_db_cluster(
            True, env_path=macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        time.sleep(5)
        for i in range(2):
            result = self.comsh_sta_sub[i].build_standby(
                "-t 3600", macro.DB_ENV_PATH_REMOTE1,
                macro.DB_INSTANCE_PATH_REMOTE1)
            self.assertIn(self.constant.BUILD_SUCCESS_MSG,
                          result, '执行失败:' + text)

        text = '--step7:更新数据 expect:成功--'
        self.log.info(text)
        sql_insert = f"insert into {self.schema_name1}.{self.tb_name1} " \
            f"values(201, 1, 1);" \
            f"insert into {self.tb_name2} values(2, 'first', '%一', 'new');"
        result = self.commsh_pub.execut_db_sql(sql_insert,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         2, '执行失败' + text)

        text = "--step8:查询数据是否更新 expect:更新--"
        self.log.info(text)
        sql_select = f"select * from {self.schema_name1}.{self.tb_name1};" \
            f"select * from {self.tb_name2};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('1 row'), 2, '执行失败' + text)
        self.assertIn('2 | first        | %一     | new',
                      result, '执行失败' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        result = self.commsh_sub.get_db_cluster_status(
            'status', env_path=macro.DB_ENV_PATH_REMOTE1)
        if not result:
            cmd = f"mv {macro.DB_INSTANCE_PATH_REMOTE1}_bak " \
                f"{macro.DB_INSTANCE_PATH_REMOTE1};"
            self.log.info(cmd)
            result = self.pri_userdb_sub.sh(cmd).result()
            self.log.info(result)
            self.commsh_sub.restart_db_cluster(True,
                                               macro.DB_ENV_PATH_REMOTE1)
            for i in range(2):
                result = self.comsh_sta_sub[i].build_standby(
                    "-t 3600", macro.DB_ENV_PATH_REMOTE1,
                    macro.DB_INSTANCE_PATH_REMOTE1)
                self.assertIn(self.constant.BUILD_SUCCESS_MSG,
                              result, '执行失败:' + text)
        sql = f"DROP PUBLICATION if exists {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP SUBSCRIPTION  {self.subname1};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP table if exists {self.schema_name1}.{self.tb_name1};" \
            f"DROP table if exists {self.tb_name2};" \
            f"drop schema {self.schema_name1};" \
            f"drop tablespace {self.tbs_name};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        result = self.commsh_pub.execut_db_sql(sql, 
                                               sql_type=self.user_param_pub)
        self.log.info(result)

        cmd = f"mv " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};"\
            f"rm -rf {self.tbs_path};"
        self.log.info(cmd)
        result = self.pri_userdb_pub.sh(cmd).result()
        self.log.info(result)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_sub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')};" \
            f"rm -rf {self.tbs_path1};" \
            f"rm -rf {self.backup_path};" \
            f"rm -rf {macro.DB_INSTANCE_PATH_REMOTE1}_bak;" \
            f"rm -rf {self.tbs_path1}_new"
        self.log.info(cmd)
        result = self.pri_userdb_sub.sh(cmd).result()
        self.log.info(result)
        result_wal = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level}')
        self.assertTrue(result_wal, '执行失败:' + text)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info("-Opengauss_Function_Pub_Sub_Case0069 end-")

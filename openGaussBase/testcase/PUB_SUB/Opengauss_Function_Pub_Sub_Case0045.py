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
Case Name   : 修改max_wal_senders
Description :
    1.发布端修改max_wal_senders
    2.在两个集群创建表
    3.创建发布端
    4.创建订阅
    5.修改数据
    6.查询同步
Expect      :
    1.成功
    2.成功
    3.成功
    4.sub4失败
    5.成功
    6.tb_pubsub_case045_3,tb_pubsub_case045_4未更新，其余更新(发布端为1主1备，
    若发布端为1主2备则仅1更新)。订阅端pg_log提示WARNING:
    apply worker could not connect to the remote server : FATAL:
    number of requested standby connections
    exceeds max_wal_senders (currently 5)
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
        self.com = Common()
        self.com_sub = Common('remote1_PrimaryDbUser')
        self.tb_name = ['tb_pubsub_case045_1', 'tb_pubsub_case045_2',
                        'tb_pubsub_case045_3', 'tb_pubsub_case045_4']
        self.subname = ["sub_case045_1", "sub_case045_2",
                        "sub_case045_3", "sub_case045_4"]
        self.pubname = ["pub_case045_1", "pub_case045_2",
                        "pub_case045_3", "pub_case045_4"]
        self.parent_path_pub = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.parent_path_sub = os.path.dirname(macro.DB_INSTANCE_PATH_REMOTE1)
        self.port = str(int(self.pri_userdb_pub.db_port) + 1)
        self.wal_level = self.com.show_param("wal_level")
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
        self.max_wal_senders = self.com.show_param("max_wal_senders")

        self.case_no = os.path.basename(__file__)[-6:-3]
        self.dir_new = os.path.join(macro.PG_LOG_PATH, 'pg_bak',
                                    f'pub_sub_case{self.case_no}')
        self.dir_new_sub = os.path.join('$GAUSSLOG', 'pg_log', 'pg_bak',
                                    f'pub_sub_case{self.case_no}')
        self.log_directory_p = self.com.show_param("log_directory")
        self.log_directory_s = self.com_sub.show_param(
            "log_directory", macro.DB_ENV_PATH_REMOTE1)
        self.hostname_s = self.pri_userdb_sub.sh('hostname').result().strip()
        self.hostname_p = self.pri_userdb_pub.sh('hostname').result().strip()

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
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f"log_directory='{self.dir_new}'",
            self.hostname_p, True)
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
            f"log_directory='{self.dir_new_sub}'",
            self.hostname_s, False, False,
            macro.DB_INSTANCE_PATH_REMOTE1, '',
            macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.restart_db_cluster(True,
                                                    macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step1:发布端修改max_wal_senders expect:成功--'
        self.log.info(text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'max_wal_senders=5')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.restart_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step2:两个集群均创建表 expect:成功--'
        self.log.info(text)
        for i in range(4):
            sql_table = f"CREATE TABLE {self.tb_name[i]}(" \
                f"id NUMBER(7) primary key, use_filename VARCHAR2(20) , " \
                f"filename VARCHAR2(255), text VARCHAR2(2000));"
            result = self.commsh_pub.execut_db_sql(
                sql_table, sql_type=self.user_param_pub)
            self.log.info(result)
            self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                             2, '执行失败:' + text)
            result = self.commsh_sub.execut_db_sql(sql_table,
                                                   self.user_param_sub, None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                             2, '执行失败:' + text)

        text = '--step3:创建发布端 expect:成功--'
        self.log.info(text)
        for i in range(4):
            sql = f"CREATE PUBLICATION {self.pubname[i]} " \
                f"for table {self.tb_name[i]};"
            result = self.commsh_pub.execut_db_sql(
                sql, sql_type=self.user_param_pub)
            self.log.info(result)
            self.assertIn(self.constant.create_pub_succ_msg, result,
                          '执行失败:' + text)
            self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                             '执行失败:' + text)

        text = '--step4:创建订阅 expect:sub4失败--'
        self.log.info(text)
        result = self.commsh_sub.execute_generate(
        macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        for i in range(4):
            sql = f"CREATE SUBSCRIPTION {self.subname[i]} CONNECTION " \
                f"'host={self.pri_userdb_pub.db_host} " \
                f"port={self.port} " \
                f"user={self.pri_userdb_pub.db_user} " \
                f"dbname={self.pri_userdb_pub.db_name} " \
                f"password={self.pri_userdb_pub.ssh_password}' " \
                f"PUBLICATION {self.pubname[i]};" \
                f"select pg_sleep(20);"
            result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub,
                                                   None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            if i < 3:
                self.assertIn(self.constant.create_sub_succ_msg,
                              result, '执行失败:' + text)
            else:
                self.assertNotIn(self.constant.create_sub_succ_msg,
                                 result, '执行失败:' + text)

        text = '--step5:修改数据 expect:成功--'
        self.log.info(text)
        for i in range(4):
            sql = f"insert into {self.tb_name[i]} " \
                f"values({i}, '66^^&', '中文', 'test');select pg_sleep(2);"
            result = self.commsh_pub.execut_db_sql(
                sql, sql_type=self.user_param_pub)
            self.log.info(result)
            self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                          result, '执行失败' + text)

        text = "--step6:查询同步  expect:tb_pubsub_case045_3," \
               "tb_pubsub_case045_4未更新，其余更新(发布端为1主1备，若发布端为1主2备则仅1更新)。" \
               "订阅端pg_log提示WARNING:  apply worker could not connect " \
               "to the remote server : FATAL:  number of requested standby " \
               "connections exceeds max_wal_senders (currently 5)--"
        self.log.info(text)
        for i in range(4):
            sql_select = f"select * from {self.tb_name[i]};"
            result = self.commsh_sub.execut_db_sql(sql_select,
                                                   self.user_param_sub,
                                                   None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            if i < 3:
                self.assertIn('1 row', result, '执行失败' + text)
                self.assertIn(f'{i} | 66^^&        | 中文   | test',
                              result, '执行失败' + text)
            else:
                self.assertIn('0 rows', result, '执行失败' + text)
                log_flg = f'FATAL:  number of requested standby ' \
                    f'connections exceeds max_wal_senders (currently 5)'
                result = self.com.find_pglog_content(
                    node=self.pri_userdb_pub,
                    content=log_flg,
                    env_path=macro.DB_ENV_PATH,
                    path=self.dir_new)
                self.assertTrue(result, '执行失败' + text)
                log_flg = [self.constant.can_not_connect_pub_msg,
                           self.pri_userdb_pub.ssh_password]
                for jdx in range(2):
                    result = self.com.find_pglog_content(
                        node=self.pri_userdb_sub,
                        content=log_flg[jdx],
                        env_path=macro.DB_ENV_PATH_REMOTE1,
                        path=self.dir_new_sub)
                    if 0 == jdx:
                        self.assertTrue(result, '执行失败' + text)
                    else:
                        self.assertFalse(result, '执行失败' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        for i in range(4):
            sql = f"DROP PUBLICATION if exists {self.pubname[i]};"
            drop_pub_result = self.commsh_pub.execut_db_sql(
                sql, sql_type=self.user_param_pub)
            self.log.info(drop_pub_result)
            sql = f"DROP SUBSCRIPTION if exists {self.subname[i]};"
            drop_sub_result = self.commsh_sub.execut_db_sql(
                sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
            self.log.info(drop_sub_result)
            sql = f"DROP table if exists {self.tb_name[i]};"
            result = self.commsh_sub.execut_db_sql(sql,
                                                   self.user_param_sub, None,
                                                   macro.DB_ENV_PATH_REMOTE1)
            self.log.info(result)
            result = self.commsh_pub.execut_db_sql(
                sql, sql_type=self.user_param_pub)
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
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'max_wal_senders={self.max_wal_senders}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        result1 = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f"log_directory='{self.log_directory_s}'",
            self.hostname_s, False, False,
            macro.DB_INSTANCE_PATH_REMOTE1, '',
            macro.DB_ENV_PATH_REMOTE1)
        result2 = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f"log_directory='{self.log_directory_p}'",
            self.hostname_p, True)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.assertTrue(result and result1 and result2, '执行失败:' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

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
Case Name   : 发布订阅--pg_subscription
Description :
    1.创建发布订阅
    2.查看 pg_subscription
    3.修改订阅端信息
    4.查询系统表内容
Expect      :
    1.成功
    2.类型与资料一致且内容正确,表中存在2条记录,数据库oid正确
    3.成功
    4.内容正确
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
        self.subname = "sub_case130"
        self.pubname = "pub_case130"
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
        self.database_name = "db_pub_sub_case130"

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

        text = '--step1:创建发布订阅 expect:成功--'
        self.log.info(text)        
        sql = f"CREATE PUBLICATION {self.pubname}  FOR all tables;"
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
        sql1 = f"create database {self.database_name};"
        sql = f"CREATE SUBSCRIPTION {self.subname} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.ssh_password}' " \
            f"PUBLICATION {self.pubname}"
        result = self.commsh_sub.execut_db_sql(sql1+sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)
        self.assertIn(self.constant.CREATE_DATABASE_SUCCESS,
                      result, '执行失败:' + text)
        sql2 = f" with (slot_name={self.subname}1);"
        result = self.commsh_sub.execut_db_sql(sql + sql2,
                                               self.user_param_sub,
                                               self.database_name,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)

        text = '--step2:查看 pg_subscription ' \
               'expect:类型与资料一致且内容正确,表中存在2条记录,数据库oid正确d--'
        self.log.info(text)
        sql = "\d+ pg_subscription"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('subdbid         | oid     | not null  | plain',
                      result, '执行失败:' + text)
        self.assertIn('subname         | name    | not null  | plain',
                      result, '执行失败:' + text)
        self.assertIn('subowner        | oid     | not null  | plain',
                      result, '执行失败:' + text)
        self.assertIn('subenabled      | boolean | not null  | plain',
                      result, '执行失败:' + text)
        self.assertIn('subconninfo     | text    |           | extended',
                      result, '执行失败:' + text)
        self.assertIn('subslotname     | name    |           | plain',
                      result, '执行失败:' + text)
        self.assertIn('subsynccommit   | text    |           | extended',
                      result, '执行失败:' + text)
        self.assertIn('subpublications | text[]  |           | extended',
                      result, '执行失败:' + text)

        sql = f"select oid,* from PG_DATABASE where " \
            f"datname='{self.pri_userdb_sub.db_name}';" \
            f"select oid,* from PG_DATABASE where " \
            f"datname='{self.database_name}';" \
              "select * from pg_subscription;"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(f"{result.splitlines()[2].split()[0].strip()}",
                      result, '执行失败:' + text)
        self.assertIn(f"{result.splitlines()[3].split()[0].strip()}",
                      result, '执行失败:' + text)
        self.assertIn('2 rows', result, '执行失败:' + text)
        self.assertNotIn(self.pri_userdb_pub.db_password,
                         result, '执行失败:' + text)
        self.assertNotIn(self.pri_userdb_sub.db_password,
                         result, '执行失败:' + text)

        text = '--step3:修改订阅端信息 expect:成功--'
        self.log.info(text)
        sql = f"alter subscription {self.subname} " \
            f"set (synchronous_commit=on);"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.alter_sub_succ_msg,
                      result, '执行失败:' + text)

        text = '--step4:查询系统表内容  expect:内容正确--'
        self.log.info(text)
        sql = "select * from pg_subscription;"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('on', result, '执行失败:' + text)

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
                sql, self.user_param_sub,
                self.database_name, macro.DB_ENV_PATH_REMOTE1)
            self.log.info(drop_sub_result)
            sql1 = f"drop database {self.database_name};"
            drop_sub_result = self.commsh_sub.execut_db_sql(
                sql+sql1, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
            self.log.info(drop_sub_result)
            cmd = f"mv " \
                f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')} "\
                f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} "
            self.log.info(cmd)
            result = self.pri_userdb_pub.sh(cmd).result()
            self.log.info(result)
            path = os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')
            cmd = f"mv " \
                f"{os.path.join(self.parent_path_sub, 'pg_hba.conf')} {path} "
            self.log.info(cmd)
            result = self.pri_userdb_sub.sh(cmd).result()
            self.log.info(result)
            result = self.commsh_pub.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG,
                f'wal_level={self.wal_level}')
            self.assertTrue(result, '执行失败:' + text)
            self.commsh_pub.restart_db_cluster(True)
            self.commsh_sub.restart_db_cluster(True,
                                               macro.DB_ENV_PATH_REMOTE1)
            self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                          '执行失败' + text)
            self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                          '执行失败' + text)
            self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

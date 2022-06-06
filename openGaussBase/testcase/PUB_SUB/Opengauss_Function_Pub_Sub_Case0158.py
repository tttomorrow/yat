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
Case Name   : 审计文件中，无明文密码
Description :
    1.两个集群审计开关打开audit_system_object
    2.两个集群创建用户
    3.创建发布(发布端执行)
    4.生成加密密码(订阅端执行)
    5.创建订阅(订阅端执行，端口只能是DN端口+1)
    6.查询审计日志
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.发布端订阅端审计日志中均无明文密码
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
        self.com_sub = Common('remote1_PrimaryDbUser')
        self.subname1 = "sub_case158_1"
        self.pubname1 = "pub_case158_1"
        self.parent_path_pub = os.path.dirname(macro.DB_INSTANCE_PATH)
        self.parent_path_sub = os.path.dirname(macro.DB_INSTANCE_PATH_REMOTE1)
        self.port = str(int(self.pri_userdb_pub.db_port) + 1)
        self.wal_level = self.com_pub.show_param("wal_level")
        self.user_name1 = "u_case158_1"
        self.user_name2 = "u_case158_2"
        self.passwd = "openGauss_1234567890123456789012"
        self.user_param_u = f'-U {self.user_name1} ' \
            f'-W {macro.COMMON_PASSWD}'

        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')} " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')};"
        self.log.info(cmd)
        self.com_pub.get_sh_result(self.pri_userdb_pub, cmd)
        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')}" \
            f" {os.path.join(self.parent_path_sub, 'pg_hba.conf')};"
        self.log.info(cmd)
        self.com_pub.get_sh_result(self.pri_userdb_sub, cmd)
        self.audit_system_object_pub = self.com_pub.show_param(
            "audit_system_object")
        self.audit_system_object_sub = self.com_sub.show_param(
            "audit_system_object", macro.DB_ENV_PATH_REMOTE1)

    def test_pubsub(self):
        text = '--step:预置条件,修改pg_hba expect:成功'
        self.log.info(text)
        self.log.info("#######发布端: ")
        guc_res = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, '',
            f'host    replication  all '
            f'{self.pri_userdb_sub.db_host}/32 sha256')
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'wal_level=logical')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.restart_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        self.log.info("#######订阅端: ")
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  all '
            f'{self.pri_userdb_pub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        result = self.commsh_sub.restart_db_cluster(True,
                                                    macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = "--step1:两个集群审计开关打开audit_system_object expect:成功--"
        self.log.info(text)
        result = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            'audit_system_object=33554431')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            'audit_system_object=33554431',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)

        text = "--step2:两个集群创建用户 expect:成功--"
        self.log.info(text)
        sql = f"create user {self.user_name1} with sysadmin " \
            f"identified by '{macro.COMMON_PASSWD}';"
        result = self.commsh_pub.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql, '', None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      '执行失败:' + text)

        text = "--step3:创建发布(发布端执行) expect:成功--"
        self.log.info(text)
        sql = f"create user {self.user_name2} with sysadmin " \
            f"identified by '{self.passwd}';" \
            f"create publication {self.pubname1} for all tables;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_u)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, result,
                      '执行失败:' + text)

        text = "--step4:生成加密密码(订阅端执行) expect:成功--"
        self.log.info(text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)

        text = "--step5:创建订阅(订阅端执行，端口只能是DN端口+1) expect:成功--"
        self.log.info(text)
        sql = f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.user_name2} " \
            f"password={self.passwd} " \
            f"dbname={self.pri_userdb_pub.db_name}' " \
            f"PUBLICATION {self.pubname1};"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_u, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(macro.COMMON_PASSWD, result, '执行失败:' + text)
        self.assertNotIn(self.passwd, result, '执行失败:' + text)
        self.assertIn(self.constant.create_sub_succ_msg,
                      result, '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = "--step6:查询审计日志 expect:发布端订阅端审计日志中均无明文密码--"
        self.log.info(text)
        sql_time = f"SELECT sysdate + interval ' 5 minutes' AS RESULT;" \
            f"SELECT sysdate - interval ' 10 minutes' AS RESULT;"
        result = self.commsh_pub.execut_db_sql(sql_time)
        time_start = result.splitlines()[-2].strip()
        time_end = result.splitlines()[2].strip()
        sql = f"select * from pg_query_audit('{time_start}','{time_end}')" \
            f"where type like '%subscription%';"
        result = self.commsh_pub.execut_db_sql(sql)
        self.log.info(result)
        self.assertIn(self.pubname1, result, '执行失败:' + text)
        self.assertNotIn(self.passwd, result, '执行失败:' + text)
        self.assertNotIn(macro.COMMON_PASSWD, result, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql_time, self.user_param_u,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        time_start = result.splitlines()[-2].strip()
        time_end = result.splitlines()[2].strip()
        sql = f"select * from pg_query_audit('{time_start}','{time_end}')" \
            f"where type like '%subscription%';"
        result = self.commsh_sub.execut_db_sql(sql, '',
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.pubname1, result, '执行失败:' + text)
        self.assertIn(self.subname1, result, '执行失败:' + text)
        self.assertNotIn(self.passwd, result, '执行失败:' + text)
        self.assertNotIn(macro.COMMON_PASSWD, result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = "--环境清理--"
        self.log.info(text)
        sql = f"DROP SUBSCRIPTION if exists {self.subname1};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_u, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP PUBLICATION  {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_u)
        self.log.info(drop_pub_result)
        sql = f"drop user {self.user_name1};" \
            f"drop user {self.user_name2};"
        result = self.commsh_pub.execut_db_sql(sql)
        self.log.info(result)
        result = self.commsh_sub.execut_db_sql(sql, '', None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};"
        self.log.info(cmd)
        self.com_pub.get_sh_result(self.pri_userdb_pub, cmd)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_sub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')} "
        self.log.info(cmd)
        self.com_pub.get_sh_result(self.pri_userdb_sub, cmd)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level}')
        result1 = self.commsh_pub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            f'audit_system_object={self.audit_system_object_pub}')
        result2 = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            f'audit_system_object={self.audit_system_object_sub}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result and result1 and result2, '执行失败:' + text)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

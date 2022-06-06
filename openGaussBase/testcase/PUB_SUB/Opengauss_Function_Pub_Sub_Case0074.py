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
Case Name   : 创建发布订阅并对发布表进行闪回操作（发布订阅均存在闪回表）
Description :
    1.设置闪回参数
    2.两个集群创建表
    3.创建函数获取csn及timecapsule
    4.创建发布订阅
    5.更新数据,并查询更新
    6.闪回查询
    7.闪回表
    8.订阅端闪回表
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.插入数据成功，订阅端按顺序进行更新成功
    6.集群A查询结果为空，集群B查询结果不变为1,99,3
    7.t1查询内容为空，第二次闪回后查询结果为1,2,3
    8.集群B更新数据成功，且闪回后数据内容为1,3,99.集群Aupdate成功，集群B数据同步为100,3,99
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
        self.tb_name1 = 'tb_pubsub_074_1'
        self.tb_name2 = 'tb_pubsub_074_2'
        self.subname1 = "sub_074_1"
        self.pubname1 = "pub_074_1"
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

        self.undo_retention_time = self.com_pub.show_param(
            "undo_retention_time")
        self.recyclebin_retention_time = self.com_pub.show_param(
            "recyclebin_retention_time")
        self.enable_recyclebin = self.com_pub.show_param("enable_recyclebin")
        self.enable_default_ustore_table = self.com_pub.show_param(
            "enable_default_ustore_table")

        self.undo_retention_time_sub = self.com_sub.show_param(
            "undo_retention_time", macro.DB_ENV_PATH_REMOTE1)
        self.recyclebin_retention_time_sub = self.com_sub.show_param(
            "recyclebin_retention_time", macro.DB_ENV_PATH_REMOTE1)
        self.enable_recyclebin_sub = self.com_sub.show_param(
            "enable_recyclebin", macro.DB_ENV_PATH_REMOTE1)
        self.enable_default_ustore_table_sub = self.com_sub.show_param(
            "enable_default_ustore_table", macro.DB_ENV_PATH_REMOTE1)

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
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG, 'wal_level=logical')
        self.assertTrue(result, '执行失败:' + text)
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_pub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)

        text = '--step1:设置闪回参数 expect:成功--'
        self.log.info(text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'undo_retention_time=3h')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'recyclebin_retention_time=3h')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'enable_recyclebin=on')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'enable_default_ustore_table=on')
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_pub.restart_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'undo_retention_time=3h',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'recyclebin_retention_time=10000',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'enable_recyclebin=on',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'enable_default_ustore_table=on',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.restart_db_cluster(
            True, macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = '--step2:两个集群创建表 expect:成功--'
        self.log.info(text)
        create_sql = f"create table {self.tb_name1}(a int primary key) ;" \
            f"create table {self.tb_name2}(id int  primary key, snaptime " \
            f"timestamptz, snapcsn bigint);"
        result = self.commsh_pub.execut_db_sql(
            create_sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         4, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(create_sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.TABLE_CREATE_SUCCESS),
                         4, '执行失败:' + text)

        text = '--step3:创建函数获取csn及timecapsule expect:成功--'
        self.log.info(text)
        sql = f"CREATE OR REPLACE FUNCTION findCsn(int8)  " \
            f"RETURNS INTEGER  LANGUAGE plpgsql " \
            f"AS \$BODY\$ declare  count integer;" \
            f"begin" \
            f"  count = (select snapcsn from {self.tb_name2} " \
            f"where id =  \$1);  return count;end;\$BODY\$;" \
            f"CREATE OR REPLACE FUNCTION findTime(int8)  " \
            f"RETURNS timestamptz" \
            f"  LANGUAGE plpgsql AS \$BODY\$ declare  " \
            f"count timestamptz;begin" \
            f"  count = (select snaptime from " \
            f"{self.tb_name2} where id=\$1);  " \
            f"return count;end;\$BODY\$;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(
            2, result.count(self.constant.CREATE_FUNCTION_SUCCESS_MSG),
            '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = "--step4:创建发布订阅 expect:成功--"
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname1} for all tables ;"
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

        text = "--step5:更新数据,并查询更新 expect:插入数据成功，订阅端按顺序进行更新成功--"
        self.log.info(text)
        sql = f"select pg_sleep(10);insert into {self.tb_name2} " \
            f"select 1, now(), int8in(xidout(next_csn)) " \
            f"from gs_get_next_xid_csn();" \
            f"insert into {self.tb_name1} values(1),(2),(3);" \
            f"select pg_sleep(10);" \
            f"insert into {self.tb_name2} select 2, now(), " \
            f"int8in(xidout(next_csn)) from gs_get_next_xid_csn();" \
            f"update {self.tb_name1} set a = 99 where a = 2;" \
            f"select pg_sleep(10);" \
            f"insert into {self.tb_name2} select 3, " \
            f"now(), int8in(xidout(next_csn)) from gs_get_next_xid_csn();"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(result.count(self.constant.INSERT_SUCCESS_MSG),
                         4, '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1],
                      result, '执行失败:' + text)
        sql_select = f"select * from {self.tb_name1} order by a;" \
            f"select * from {self.tb_name2};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('3 rows'), 2, '执行失败:' + text)
        self.assertIn('99', result, '执行失败:' + text)
        self.assertIn('1', result, '执行失败:' + text)
        self.assertIn('3', result, '执行失败:' + text)
        result_a = self.commsh_pub.execut_db_sql(sql_select,
                                               sql_type=self.user_param_pub)
        self.log.info(result_a)
        self.assertEqual(result, result_a, '执行失败:' + text)

        text = "--step6:闪回查询 expect:集群A查询结果为空，集群B查询结果不变为1,99,3--"
        self.log.info(text)
        sql = f"select * from {self.tb_name1} timecapsule " \
            f"csn findCsn(1) order by a;" \
            f"select * from {self.tb_name1} timecapsule " \
            f"timestamp findTime(1) order by a;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn('0 rows', result, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('3 rows', result, '执行失败:' + text)
        self.log.info(result)

        text = "--step7:闪回表 expect:t1查询内容为空，第二次闪回后查询结果为1,2,3--"
        self.log.info(text)
        sql = f"timecapsule table {self.tb_name1} to csn findCsn(1);"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.timecapsule_table_succ_msg,
                      result, '执行失败:' + text)
        result_a = self.commsh_pub.execut_db_sql(sql_select,
                                               sql_type=self.user_param_pub)
        self.log.info(result_a)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('0 rows', result, '执行失败:' + text)
        self.assertEqual(result, result_a, '执行失败:' + text)
        sql = f"timecapsule table {self.tb_name1} to timestamp findTime(2);"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.timecapsule_table_succ_msg,
                      result, '执行失败:' + text)
        result_a = self.commsh_pub.execut_db_sql(sql_select,
                                                 sql_type=self.user_param_pub)
        self.log.info(result_a)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('3 rows', result, '执行失败:' + text)
        self.assertIn('1', result.splitlines()[2], '执行失败:' + text)
        self.assertIn('2', result.splitlines()[3], '执行失败:' + text)
        self.assertIn('3', result.splitlines()[4], '执行失败:' + text)
        self.assertEqual(result, result_a, '执行失败:' + text)

        text = "--step8:订阅端闪回表 expect:集群B更新数据成功，且闪回后数据内容为1,3,99." \
               "集群Aupdate成功，集群B数据同步为100,3,99--"
        self.log.info(text)
        sql = f"update {self.tb_name1} set a = 99 where a = 2;" \
            f"insert into {self.tb_name2} select 4, now(), " \
            f"int8in(xidout(next_csn)) from gs_get_next_xid_csn();" \
            f"insert into {self.tb_name1} values(4);" \
            f"timecapsule table {self.tb_name1} to csn findCsn(4);"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('3 rows', result, '执行失败:' + text)
        self.assertIn('1', result.splitlines()[2], '执行失败:' + text)
        self.assertIn('3', result.splitlines()[3], '执行失败:' + text)
        self.assertIn('99', result.splitlines()[4], '执行失败:' + text)
        sql = f"update {self.tb_name1} set a=100 where a=1;"
        result_a = self.commsh_pub.execut_db_sql(sql,
                                                 sql_type=self.user_param_pub)
        self.log.info(result_a)
        result_a = self.commsh_pub.execut_db_sql(sql_select,
                                                 sql_type=self.user_param_pub)
        self.log.info(result_a)
        self.assertIn('2', result_a.splitlines()[2], '执行失败:' + text)
        self.assertIn('3', result_a.splitlines()[3], '执行失败:' + text)
        self.assertIn('100', result_a.splitlines()[4], '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('3', result.splitlines()[2], '执行失败:' + text)
        self.assertIn('99', result.splitlines()[3], '执行失败:' + text)
        self.assertIn('100', result.splitlines()[4], '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = '--清理环境--'
        self.log.info(text)
        sql = f"DROP PUBLICATION if exists {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP SUBSCRIPTION  {self.subname1};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP table if exists {self.tb_name2};" \
            f"DROP table if exists {self.tb_name1};" \
            f"drop function if exists findCsn;" \
            f"drop function if exists findTime;"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)

        cmd = f"mv " \
            f"{os.path.join(self.parent_path_pub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH, 'pg_hba.conf')};"
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
        result1 = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'undo_retention_time={self.undo_retention_time}')
        result2 = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'recyclebin_retention_time={self.recyclebin_retention_time}')
        result3 = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'enable_recyclebin={self.enable_recyclebin}')
        result4 = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'enable_default_ustore_table={self.enable_default_ustore_table}')
        result5 = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'undo_retention_time={self.undo_retention_time_sub}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        result6 = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'recyclebin_retention_time={self.recyclebin_retention_time_sub}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        result7 = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'enable_recyclebin={self.enable_recyclebin_sub}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        result8 = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'enable_default_ustore_table='
            f'{self.enable_default_ustore_table_sub}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result and result1 and result2 and
                        result3 and result4 and result5 and result6
                        and result7 and result8, '执行失败:' + text)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")

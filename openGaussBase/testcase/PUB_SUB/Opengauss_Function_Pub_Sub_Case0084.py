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
Case Name   : 发布内容_HLL类型（场景2）
Description :
    1.两个集群均创建表
    2.创建表并指定列为hll_集群A
    3.创建发布订阅
    4.插入数据_集群A（场景2）:
    5.根据日期把数据分组，并把数据插入到hll中_集群A
    6.查询数据_集群B:订阅端计算每一天访问网站不同用户数量
    7.删除订阅 集群B：
    8.删除发布 集群A
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.数据显示正确，与集群A同步
    7.成功
    8.成功
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
        self.tb_name1 = 'tb_pubsub_case084_1'
        self.tb_name2 = 'tb_pubsub_case084_2'
        self.subname1 = "sub_case084_1"
        self.pubname1 = "pub_case084_1"
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

        text = '--step1:集群A均创建表 expect:成功--'
        self.log.info(text)
        create_sql = f'CREATE TABLE {self.tb_name1}' \
            f'(date date,user_id integer);'
        result = self.commsh_pub.execut_db_sql(
            create_sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                      result, '执行失败:' + text)

        text = '--step2:创建表并指定列为hll expect:成功--'
        self.log.info(text)
        create_sql = f'CREATE TABLE {self.tb_name2}' \
            f'(date            date UNIQUE,users           hll);'
        result = self.commsh_pub.execut_db_sql(
            create_sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                      result, '执行失败:' + text)
        result = self.commsh_sub.execut_db_sql(create_sql,
                                               self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS,
                      result, '执行失败:' + text)

        text = "--step3:创建发布订阅 expect:成功--"
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname1} for table {self.tb_name2};"
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

        text = "--step4:插入数据_集群A（场景2）: expect:成功--"
        self.log.info(text)
        sql = f"insert into {self.tb_name1} " \
            f"values('2019-02-20',generate_series(1,100));" \
            f"insert into {self.tb_name1} " \
            f"values('2019-02-21',generate_series(1,200));" \
            f"insert into {self.tb_name1} " \
            f"values('2019-02-22',generate_series(1,300));" \
            f"insert into {self.tb_name1} " \
            f"values('2019-02-23',generate_series(1,400));" \
            f"insert into {self.tb_name1} " \
            f"values('2019-02-24',generate_series(1,500));" \
            f"insert into {self.tb_name1} " \
            f"values('2019-02-25',generate_series(1,600));" \
            f"insert into {self.tb_name1} " \
            f"values('2019-02-26',generate_series(1,700));" \
            f"insert into {self.tb_name1} " \
            f"values('2019-02-27',generate_series(1,800));" \
            f"select pg_sleep(5.5);"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                      result, '执行失败:' + text)

        text = '--step5:根据日期把数据分组，并把数据插入到hll中_集群A expect:成功--'
        self.log.info(text)
        create_sql = f'insert into {self.tb_name2}(date, users) select ' \
            f'date, hll_add_agg(hll_hash_integer(user_id)) ' \
            f'from {self.tb_name1} group by 1;'
        result = self.commsh_pub.execut_db_sql(
            create_sql, sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                      result, '执行失败:' + text)

        text = "--step6:查询数据_集群B expect:数据显示正确，与集群A同步--"
        self.log.info(text)
        sql_select = f"select date, hll_cardinality(users) " \
            f"from {self.tb_name2} order by date;" \
            f"select hll_cardinality(hll_union_agg(users)) " \
            f"from {self.tb_name2} where " \
            f"date >= '2019-02-20'::date and date <= '2021-02-26'::date;" \
            f"SELECT date, (#hll_union_agg(users) OVER two_days) - " \
            f"#users AS lost_uniques FROM {self.tb_name2} WINDOW " \
            f"two_days AS (ORDER BY date ASC ROWS 1 PRECEDING);"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('1 row', result, '执行失败:' + text)
        self.assertEqual(result.count('8 rows'), 2, '执行失败:' + text)
        result_a = self.commsh_pub.execut_db_sql(sql_select,
                                               sql_type=self.user_param_pub)
        self.log.info(result_a)
        self.assertEqual(result_a, result, '执行失败:' + text)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = "--step7:删除订阅 集群B： expect:成功--"
        self.log.info(text)
        sql = f"DROP SUBSCRIPTION  {self.subname1};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)

        text = "--step8:删除发布 集群A expect:成功--"
        self.log.info(text)
        sql = f"DROP PUBLICATION  {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)

        sql = f"DROP table if exists {self.tb_name1};" \
            f"DROP table if exists {self.tb_name2};"
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

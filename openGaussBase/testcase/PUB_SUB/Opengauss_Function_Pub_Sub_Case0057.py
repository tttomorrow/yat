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
Case Name   : 发布触发器
Description :
    1.两个集群创建表
    2.创建触发器
    3.创建发布订阅
    4.更新数据
    5.查询数据是否更新
    6.修改数据
    7.查询数据是否更新
    8.修改数据
    9.查询数据是否更新
    10.修改数据
    11.查询数据是否更新
    12.手动同步数据
    13.创建UPDATE OF trigger
    14.查询数据是否更新
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.更新
    6.成功
    7.更新
    8.成功
    9.test_trigger_src_tbl更新 test_trigger_des_tbl未更新
    10.成功
    11.不更新
    12.成功
    13.成功
    14.更新
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
        self.tb_name_src = 'tb_pubsub_case057_1'
        self.tb_name_des = 'tb_pubsub_case057_2'
        self.subname1 = "sub_case057_1"
        self.pubname1 = "pub_case057_1"
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

        text = '--step1:两个集群创建表 expect:成功--'
        self.log.info(text)
        create_sql = f"CREATE TABLE {self.tb_name_src}" \
            f"(id1 INT primary key, id2 INT, id3 INT);" \
            f"CREATE TABLE {self.tb_name_des}" \
            f"(id1 INT primary key, id2 INT, id3 INT);"
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

        text = '--step2:创建触发器 expect:成功--'
        self.log.info(text)
        sql = f"CREATE OR REPLACE FUNCTION tri_insert_func() " \
            f"RETURNS TRIGGER AS \$\$ " \
            f"DECLARE BEGIN" \
            f"    INSERT INTO {self.tb_name_des}  " \
            f"VALUES(NEW.id1, NEW.id2, NEW.id3);" \
            f"     RETURN NEW;" \
            f"END" \
            f"\$\$ LANGUAGE PLPGSQL;" \
            f"CREATE TRIGGER insert_trigger " \
            f"BEFORE INSERT ON {self.tb_name_src} " \
            f"FOR EACH ROW EXECUTE PROCEDURE tri_insert_func();" \
            f"CREATE OR REPLACE FUNCTION TRI_DELETE_FUNC() " \
            f"RETURNS TRIGGER AS \$\$ DECLARE BEGIN " \
            f"DELETE FROM {self.tb_name_des} WHERE id1=OLD.id1;" \
            f"                   RETURN OLD; " \
            f"END " \
            f" \$\$ LANGUAGE PLPGSQL;" \
            f"CREATE TRIGGER delete_trigger after DELETE ON " \
            f"{self.tb_name_src}  FOR EACH row   " \
            f"EXECUTE PROCEDURE tri_delete_func();" \
            f"CREATE OR REPLACE FUNCTION tri_update_func() " \
            f"RETURNS TRIGGER AS \$\$ DECLARE " \
            f"BEGIN UPDATE {self.tb_name_des} " \
            f"SET id3 = NEW.id3 WHERE id1=OLD.id1; " \
            f"RETURN OLD; END \$\$ LANGUAGE PLPGSQL;" \
            f"CREATE TRIGGER update_trigger  " \
            f"AFTER UPDATE ON {self.tb_name_src} FOR EACH ROW " \
            f"EXECUTE PROCEDURE tri_update_func();" \
            f"CREATE OR REPLACE FUNCTION tri_truncate_func() " \
            f"RETURNS TRIGGER AS \$\$ DECLARE BEGIN" \
            f" truncate table {self.tb_name_des};RETURN NEW;" \
            f"END \$\$ LANGUAGE PLPGSQL;CREATE TRIGGER truncate_trigger " \
            f"BEFORE truncate ON {self.tb_name_src} FOR EACH STATEMENT " \
            f"EXECUTE PROCEDURE tri_truncate_func();"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertEqual(
            result.count(self.constant.TRIGGER_CREATE_SUCCESS_MSG),
            4, '执行失败:' + text)
        self.assertEqual(
            result.count(self.constant.CREATE_FUNCTION_SUCCESS_MSG),
            4, '执行失败:' + text)

        text = "--step3:创建发布订阅 expect:成功--"
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

        text = "--step4:更新数据 expect:成功--"
        self.log.info(text)
        sql = f"insert into {self.tb_name_src} values(1, 1, 1);" \
            f"select pg_sleep(5.5);" \
            f"insert into {self.tb_name_src} values(2, 2, 2);" \
            f"insert into {self.tb_name_src} values(3, 3, 3);"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                      result, '执行失败:' + text)

        text = "--step5:查询数据是否更新 expect:更新--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name_src};" \
            f"select * from {self.tb_name_des};"
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('3 rows'), 2, '执行失败:' + text)

        text = "--step6:更新数据 expect:成功--"
        self.log.info(text)
        sql = f"delete from {self.tb_name_src}  where id1=1;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.DELETE_SUCCESS_MSG,
                      result, '执行失败:' + text)

        text = "--step7:查询数据是否更新 expect:更新--"
        self.log.info(text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('2 rows'), 2, '执行失败:' + text)
        self.assertNotIn('1 |   1 |   1', result, '执行失败:' + text)

        text = "--step8:更新数据 expect:成功--"
        self.log.info(text)
        sql = f"UPDATE {self.tb_name_src} SET id3=400 WHERE id1=2;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.UPDATE_SUCCESS_MSG,
                      result, '执行失败:' + text)

        text = "--step9:查询数据是否更新 " \
               "expect:test_trigger_src_tbl更新 test_trigger_des_tbl未更新--"
        self.log.info(text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('2 |   2 | 400', result, '执行失败:' + text)

        text = "--step10:更新数据 expect:成功--"
        self.log.info(text)
        sql = f"truncate table {self.tb_name_src};"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.TRUNCATE_SUCCESS_MSG,
                      result, '执行失败:' + text)

        text = "--step11:查询数据是否更新 expect:不更新--"
        self.log.info(text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertEqual(result.count('2 rows'), 2, '执行失败:' + text)

        text = "--step12:手动同步数据 expect:不更新--"
        self.log.info(text)
        sql = f"truncate table {self.tb_name_des};" \
            f"truncate table {self.tb_name_src};"
        result = self.commsh_sub.execut_db_sql(sql,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn(self.constant.TRUNCATE_SUCCESS_MSG,
                      result, '执行失败:' + text)

        text = "--step13:创建UPDATE OF trigger expect:成功--"
        self.log.info(text)
        sql = f"drop trigger update_trigger on  {self.tb_name_src};" \
            f"drop function tri_update_func();" \
            f"CREATE OR REPLACE FUNCTION tri_update_func() " \
            f"RETURNS TRIGGER AS \$\$  " \
            f"DECLARE  BEGIN " \
            f" UPDATE {self.tb_name_des} SET id2 = NEW.id2;" \
            f" RETURN OLD;  END  \$\$ LANGUAGE PLPGSQL;" \
            f"CREATE TRIGGER update_of_trigger " \
            f"after update of id2 ON {self.tb_name_src} " \
            f"FOR EACH row EXECUTE PROCEDURE tri_update_func();" \
            f"insert into {self.tb_name_src} values(3, 3, 3);" \
            f"update {self.tb_name_src} set id2=50;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.CREATE_FUNCTION_SUCCESS_MSG,
                      result, '执行失败:' + text)
        self.assertIn(self.constant.TRIGGER_CREATE_SUCCESS_MSG,
                      result, '执行失败:' + text)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG,
                      result, '执行失败:' + text)
        self.assertIn(self.constant.UPDATE_SUCCESS_MSG,
                      result, '执行失败:' + text)

        text = "--step14:查询数据是否更新 expect:更新--"
        self.log.info(text)
        result = self.commsh_sub.execut_db_sql(sql_select,
                                               self.user_param_sub,
                                               None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertIn('3 |  50 |   3', result, '执行失败:' + text)

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
        sql = f"DROP table if exists {self.tb_name_src};" \
            f"DROP table if exists {self.tb_name_des};"
        sql_func = f"drop function if exists tri_insert_func;" \
            f"drop function if exists TRI_DELETE_FUNC;" \
            f"drop function if exists  tri_update_func;" \
            f"drop function if exists  tri_truncate_func;"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        result = self.commsh_pub.execut_db_sql(sql+sql_func,
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

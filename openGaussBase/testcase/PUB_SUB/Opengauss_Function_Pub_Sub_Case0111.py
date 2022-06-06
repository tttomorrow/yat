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
Case Name   : 修改订阅，验证subscription_parameter参数synchronous_commit
Description :
    1.在两个集群中创建相同字段表
    2.创建发布端(集群A)
    3.创建订阅，指定synchronous_commit为on 
    4.订阅端设置synchronous_commit为on
    5.修改订阅，设置synchronous_commit为off 
    6.停止订阅端备节点
    7.发布端插入数据
    8.订阅端检查数据
    9.订阅端设置synchronous_commit为off
    10.修改订阅，设置synchronous_commit为on
    11.停止订阅端备节点
    12.发布端插入数据
    13.订阅端检查数据
    14.重启订阅端备节点
    15.订阅端检查数据
Expect      :
    1.成功
    2.成功
    3.成功
    4.成功
    5.成功
    6.成功
    7.成功
    8.数据同步
    9.成功
    10.成功
    11.成功
    12.成功
    13.数据未同步，查询阻塞
    14.成功
    15.阻塞，此时数据库不存在同步备
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
from testcase.utils.ComThread import ComThread

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class Pubsubclass(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info("-----------this is setup-----------")
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} start-----")
        self.pri_userdb_pub = Node(node='PrimaryDbUser')
        self.pri_userdb_sub = Node(node='remote1_PrimaryDbUser')
        self.pri_root_sub = Node(node='remote1_PrimaryRoot')
        self.constant = Constant()
        self.commsh_pub = CommonSH('PrimaryDbUser')
        self.commsh_sub = CommonSH('remote1_PrimaryDbUser')
        self.commsh_sub_sta = [CommonSH('remote1_Standby1DbUser'),
                               CommonSH('remote1_Standby2DbUser')]
        self.com_pub = Common()
        self.com_sub = Common('remote1_PrimaryDbUser')
        self.subname1 = "sub_case111_1"
        self.pubname1 = "pub_case111_1"
        self.tb_name1 = "t_case111_1"
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
        self.com_pub.get_sh_result(self.pri_userdb_pub, cmd)
        cmd = f"cp " \
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')}" \
            f" {os.path.join(self.parent_path_sub, 'pg_hba.conf')};"
        self.log.info(cmd)
        self.com_pub.get_sh_result(self.pri_userdb_sub, cmd)
        self.synchronous_commit = self.com_sub.show_param(
            "synchronous_commit", macro.DB_ENV_PATH_REMOTE1)
        self.most_available_sync = self.com_sub.show_param(
            "most_available_sync", macro.DB_ENV_PATH_REMOTE1)
        self.sub_num = self.commsh_sub.get_node_num(macro.DB_ENV_PATH_REMOTE1)

    def test_pubsub(self):
        text = '--step:预置条件,修改pg_hba expect:成功'
        self.log.info(text)
        self.log.info("#######发布端: ")
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
        result = self.commsh_pub.restart_db_cluster(True)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)
        self.log.info("#######订阅端: ")
        guc_res = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG, '',
            'all', False, False, macro.DB_INSTANCE_PATH_REMOTE1,
            f'host    replication  {self.pri_userdb_pub.db_user} '
            f'{self.pri_userdb_pub.db_host}/32 sha256',
            macro.DB_ENV_PATH_REMOTE1)
        self.log.info(guc_res)
        self.assertTrue(guc_res, '执行失败:' + text)
        if "off" != self.most_available_sync:
            result = self.commsh_sub.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                'most_available_sync=off',
                dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
                env_path=macro.DB_ENV_PATH_REMOTE1)
            self.assertTrue(result, '执行失败:' + text)

        text = '--step1:在两个集群中创建相同字段表 expect:成功--'
        self.log.info(text)
        create_sql = f'create table {self.tb_name1}' \
            f'(id int primary key,t text);'
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

        text = "--step2:创建发布端(集群A) expect:成功--"
        self.log.info(text)
        sql = f"CREATE PUBLICATION {self.pubname1} for table {self.tb_name1} ;"
        result = self.commsh_pub.execut_db_sql(sql,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.create_pub_succ_msg, result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1], result,
                         '执行失败:' + text)

        text = "--step3:创建订阅synchronous_commit为on   expect:创建订阅成功--"
        self.log.info(text)
        result = self.commsh_sub.execute_generate(
            macro.COMMON_PASSWD, env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertIn('', result, '执行失败:' + text)
        sql = f"CREATE SUBSCRIPTION {self.subname1} CONNECTION " \
            f"'host={self.pri_userdb_pub.db_host} " \
            f"port={self.port} " \
            f"user={self.pri_userdb_pub.db_user} " \
            f"dbname={self.pri_userdb_pub.db_name} " \
            f"password={self.pri_userdb_pub.db_password}' " \
            f"PUBLICATION {self.pubname1} with (synchronous_commit=on);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1],
                         result, '执行失败:' + text)
        self.assertIn(self.constant.create_sub_succ_msg, result,
                      '执行失败:' + text)

        text = "--step4:订阅端设置synchronous_commit为on  expect:成功--"
        self.log.info(text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'synchronous_commit=on',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.restart_db_cluster(True,
                                                    macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = "--step5:修改订阅，设置synchronous_commit为off   expect:成功--"
        self.log.info(text)
        sql = f"alter subscription {self.subname1} " \
            f"set (synchronous_commit=off);"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1],
                         result, '执行失败:' + text)
        self.assertIn(self.constant.alter_sub_succ_msg, result,
                      '执行失败:' + text)

        text = "--step6:停止订阅端备节点  expect:成功--"
        self.log.info(text)
        for i in range(int(self.sub_num)-1):
            result = self.commsh_sub_sta[i].stop_db_instance(
                macro.DB_ENV_PATH_REMOTE1, macro.DB_INSTANCE_PATH_REMOTE1)
            self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG,
                          result, '执行失败:' + text)

        text = "--step7:发布端插入数据  expect:成功--"
        self.log.info(text)
        sql_insert = f"insert into {self.tb_name1} values(1, 'first');"
        result = self.commsh_pub.execut_db_sql(sql_insert,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result, '执行失败' + text)

        text = "--step8:查询是否同步  expect:成功--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1}"
        select_thread = ComThread(self.commsh_sub.execut_db_sql,
                                      args=(sql_select,
                                        self.user_param_sub,
                                        None, macro.DB_ENV_PATH_REMOTE1))
        select_thread.setDaemon(True)
        select_thread.start()
        select_thread.join(10)
        result = select_thread.get_result()
        self.log.info(result)
        self.assertIn('1 row', result, '执行失败' + text)
        self.assertIn('1 | first', result, '执行失败' + text)

        text = "--step9:订阅端设置synchronous_commit为off  expect:成功--"
        self.log.info(text)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            'synchronous_commit=off',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        result = self.commsh_sub.restart_db_cluster(True,
                                                    macro.DB_ENV_PATH_REMOTE1)
        flg = self.constant.START_SUCCESS_MSG in result or 'Degrade' in result
        self.assertTrue(flg, '执行失败:' + text)

        text = "--step10:停止订阅端备节点  expect:成功--"
        self.log.info(text)
        for i in range(int(self.sub_num)-1):
            result = self.commsh_sub_sta[i].stop_db_instance(
                macro.DB_ENV_PATH_REMOTE1, macro.DB_INSTANCE_PATH_REMOTE1)
            self.assertIn(self.constant.GS_CTL_STOP_SUCCESS_MSG,
                          result, '执行失败:' + text)

        text = "--step11:修改订阅，设置synchronous_commit为on   expect:成功--"
        self.log.info(text)
        sql = f"alter subscription {self.subname1} " \
            f"set (synchronous_commit=on);" \
            f"select pg_sleep(15);" \
            f"select * from pg_subscription;"
        result = self.commsh_sub.execut_db_sql(sql, self.user_param_sub, None,
                                               macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        self.assertNotIn(self.constant.SQL_WRONG_MSG[1],
                         result, '执行失败:' + text)
        self.assertIn(self.constant.alter_sub_succ_msg, result,
                      '执行失败:' + text)

        text = "--step12:发布端插入数据  expect:成功--"
        self.log.info(text)
        sql_insert = f"insert into {self.tb_name1} values(2, 'f2irst');"
        result = self.commsh_pub.execut_db_sql(sql_insert,
                                               sql_type=self.user_param_pub)
        self.log.info(result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, result, '执行失败' + text)

        text = "--step13:查询是否同步  expect:数据未同步，查询阻塞--"
        self.log.info(text)
        sql_select = f"select * from {self.tb_name1}"
        select_thread = ComThread(self.commsh_sub.execut_db_sql,
                                  args=(sql_select,
                                        self.user_param_sub,
                                        None, macro.DB_ENV_PATH_REMOTE1))
        select_thread.setDaemon(True)
        select_thread.start()
        select_thread.join(10)
        result = select_thread.get_result()
        self.log.info(result)
        self.assertEqual(None, result, '执行失败' + text)
        time.sleep(30)

        text = "--step14:恢复订阅端备节点  expect:成功--"
        self.log.info(text)
        result = self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            'most_available_sync=on',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        self.log.info(result)
        for i in range(int(self.sub_num)-1):
            result = self.commsh_sub_sta[i].start_db_instance('standby',
                macro.DB_ENV_PATH_REMOTE1, macro.DB_INSTANCE_PATH_REMOTE1)
            self.assertIn(self.constant.REBUILD_SUCCESS_MSG,
                          result, '执行失败:' + text)

        text = "--step15:查询是否同步  expect:阻塞，此时数据库不存在同步备--"
        self.log.info(text)
        time.sleep(5)
        select_thread = ComThread(self.commsh_sub.execut_db_sql,
                                  args=(sql_select,
                                        self.user_param_sub,
                                        None, macro.DB_ENV_PATH_REMOTE1))
        select_thread.setDaemon(True)
        select_thread.start()
        select_thread.join(30)
        result = select_thread.get_result()
        self.log.info(result)
        self.assertEqual(None, result, '执行失败' + text)
        time.sleep(30)

    def tearDown(self):
        self.log.info('------------this is tearDown-------------')
        text = "--环境清理--"
        self.log.info(text)
        for i in range(int(self.sub_num)-1):
            result = self.commsh_sub_sta[i].start_db_instance('standby',
                macro.DB_ENV_PATH_REMOTE1, macro.DB_INSTANCE_PATH_REMOTE1)
            self.log.info(result)
        self.commsh_sub.execute_gsguc(
            'reload', self.constant.GSGUC_SUCCESS_MSG,
            f'synchronous_commit=on',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        sql = f"DROP SUBSCRIPTION  {self.subname1};"
        drop_sub_result = self.commsh_sub.execut_db_sql(
            sql, self.user_param_sub, None, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(drop_sub_result)
        sql = f"DROP PUBLICATION  {self.pubname1};"
        drop_pub_result = self.commsh_pub.execut_db_sql(
            sql, sql_type=self.user_param_pub)
        self.log.info(drop_pub_result)
        sql = f"DROP table if exists {self.tb_name1};"
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
        self.com_pub.get_sh_result(self.pri_userdb_pub, cmd)
        cmd = f"mv " \
            f"{os.path.join(self.parent_path_sub, 'pg_hba.conf')} "\
            f"{os.path.join(macro.DB_INSTANCE_PATH_REMOTE1, 'pg_hba.conf')} "
        self.log.info(cmd)
        self.com_pub.get_sh_result(self.pri_userdb_sub, cmd)
        result = self.commsh_pub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'wal_level={self.wal_level}')
        self.assertTrue(result, '执行失败:' + text)
        self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'synchronous_commit={self.synchronous_commit}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        result = self.commsh_sub.execute_gsguc(
            'set', self.constant.GSGUC_SUCCESS_MSG,
            f'most_available_sync={self.most_available_sync}',
            dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
            env_path=macro.DB_ENV_PATH_REMOTE1)
        sync = self.com_sub.show_param(
            "most_available_sync", macro.DB_ENV_PATH_REMOTE1)
        if self.most_available_sync != sync:
            self.commsh_sub.execute_gsguc(
                'reload', self.constant.GSGUC_SUCCESS_MSG,
                f'most_available_sync={self.most_available_sync}',
                dn_path=macro.DB_INSTANCE_PATH_REMOTE1,
                env_path=macro.DB_ENV_PATH_REMOTE1)
        self.assertTrue(result, '执行失败:' + text)
        self.commsh_pub.restart_db_cluster(True)
        self.commsh_sub.restart_db_cluster(True, macro.DB_ENV_PATH_REMOTE1)
        self.log.info(f"-----{os.path.basename(__file__)[:-3]} end-----")
        self.assertIn(self.constant.drop_pub_succ_msg, drop_pub_result,
                      '执行失败' + text)
        self.assertIn(self.constant.drop_sub_succ_msg, drop_sub_result,
                      '执行失败' + text)

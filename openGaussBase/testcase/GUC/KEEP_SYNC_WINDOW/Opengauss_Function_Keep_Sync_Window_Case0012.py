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
Case Type   : keep_sync_window
Case Name   : 1主2备环境下，1主1同步1异步，同步备异常，时间窗口参数等于0，
               验证是否进入最大可用模式
Description :
        1.设置以下四个guc参数
        1.1设置synchronous_standby_names='dn_6002'
        1.2.设置synchronous_commit=on
        1.3.设置most_available_sync=on
        1.4设置keep_sync_window=0
        2.查询集群同步方式
        3.建表
        4.停止备1节点
        5.插入数据
        6.启动备1节点
        7.查看备机数据是否同步
        8.清理环境
Expect      :
        1.设置成功
        2.备1同步，备2异步
        3.建表成功
        4.停止备1节点成功
        5.主节点插入数据，主节点立即进入最大可用模式，数据插入成功
        6.启动成功
        7.同步成功
        8.清理环境完成
"""
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class GucParameters(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0012 start-')
        self.constant = Constant()
        self.common = Common()
        self.standby_sh1 = CommonSH('Standby1DbUser')
        self.standby_sh2 = CommonSH('Standby2DbUser')
        self.db_primary_user_node = Node(node='PrimaryDbUser')
        self.default_value1 = self.common.show_param('keep_sync_window')
        self.default_value2 = self.common.show_param(
            'synchronous_standby_names')
        self.default_value3 = self.common.show_param('synchronous_commit')
        self.default_value4 = self.common.show_param('most_available_sync')
        self.tb_name = "tb_keep_sync_window_0012"

    def test_keep_sync_window(self):
        text = '--step1:设置以下guc参数;expect:设置成功--'
        self.log.info(text)
        result = Primary_SH.execute_gsguc("reload",
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"synchronous_standby_names"
                                          f"='dn_6002'",
                                          single=True)

        self.assertTrue(result, '执行失败' + text)
        self.log.info('设置synchronous_commit=on')
        result = Primary_SH.execute_gsguc("reload",
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"synchronous_commit=on")

        self.assertTrue(result, '执行失败' + text)
        self.log.info('设置most_available_sync=on')
        result = Primary_SH.execute_gsguc("reload",
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"most_available_sync=on")

        self.assertTrue(result, '执行失败' + text)
        self.log.info('设置keep_sync_window=0')
        result = Primary_SH.execute_gsguc("reload",
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"keep_sync_window=0")

        self.assertTrue(result, '执行失败' + text)
        result = Primary_SH.stop_db_cluster()
        self.assertTrue(result, '执行失败' + text)
        result = Primary_SH.restart_db_cluster()
        self.assertTrue(result, '执行失败' + text)

        text = '--step2:查询集群同步方式;expect:备1同步，备2异步--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql("select * from "
                                           "pg_stat_replication;")
        self.log.info(sql_cmd)
        self.assertIn('Sync', sql_cmd, '执行失败' + text)
        self.assertIn('Async', sql_cmd, '执行失败' + text)

        text = '--step3:建表;expect:建表成功--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f"drop table if exists "
                                           f"{self.tb_name};"
                                           f"create table {self.tb_name}"
                                           f"(id int,name text);")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败' + text)

        text = '--step4:停止备1;expect:停止成功--'
        self.log.info(text)
        stop_cmd = self.standby_sh1.stop_db_instance()
        self.log.info(stop_cmd)
        self.assertTrue(stop_cmd, '执行失败' + text)

        text = '--step5:插入数据;expect:主节点立即进入最大可用模式，' \
               '数据插入成功，时间参数生效--'
        self.log.info(text)
        sql_cmd = f"insert into {self.tb_name} values" \
                  f"(generate_series(1,10),'column_'|| generate_series(1,10));"
        insert_thread = ComThread(Primary_SH.execut_db_sql,
                                  args=(sql_cmd, ''))
        insert_thread.setDaemon(True)
        insert_thread.start()
        insert_thread.join(10 * 60)
        insert_thread_result = insert_thread.get_result()
        self.log.info(insert_thread_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_thread_result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.keep_sync_window_msg,
                         insert_thread_result, '执行失败:' + text)

        text = '--step6:gs_ctl方式启动备1节点;expect:启动成功--'
        self.log.info(text)
        start_cmd = self.standby_sh1.start_db_instance(mode="standby")
        self.log.info(start_cmd)
        self.assertTrue(start_cmd, '执行失败' + text)

        text = '----step7:查看备机数据是否同步;expect:同步成功----'
        self.log.info(text)
        sql_cmd = f"select * from {self.tb_name};"
        msg_primary = Primary_SH.execut_db_sql(sql_cmd)
        self.log.info(msg_primary)
        msg_standby1 = self.standby_sh1.execut_db_sql(sql_cmd)
        self.log.info(msg_standby1)
        msg_standby2 = self.standby_sh2.execut_db_sql(sql_cmd)
        self.log.info(msg_standby2)
        self.assertEqual(msg_primary, msg_standby1, '执行失败:' + text)
        self.assertEqual(msg_primary, msg_standby2, '执行失败:' + text)

    def tearDown(self):
        text = '--step8:清理环境;expect:清理环境完成--'
        self.log.info(text)
        self.log.info('删表')
        drop_cmd = Primary_SH.execut_db_sql(f"drop table if exists "
                                            f"{self.tb_name};")
        self.log.info(drop_cmd)
        self.log.info('恢复参数默认值')
        result1 = Primary_SH.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"synchronous_commit="
                                           f"{self.default_value3}")

        result2 = Primary_SH.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"most_available_sync="
                                           f"{self.default_value4}")

        result3 = Primary_SH.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"keep_sync_window="
                                           f"{self.default_value1}")
        result4 = Primary_SH.execute_gsguc("reload",
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"synchronous_standby_names"
                                           f"='{self.default_value2}'",
                                           single=True)
        result = Primary_SH.stop_db_cluster()
        self.assertTrue(result, '执行失败' + text)
        result = Primary_SH.restart_db_cluster()
        self.assertTrue(result, '执行失败' + text)
        self.log.info('断言teardown成功')
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_cmd,
                      '执行失败' + text)
        self.assertEqual(True, result1, '执行失败' + text)
        self.assertEqual(True, result2, '执行失败' + text)
        self.assertEqual(True, result3, '执行失败' + text)
        self.assertEqual(True, result4, '执行失败' + text)
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0012 finish-')

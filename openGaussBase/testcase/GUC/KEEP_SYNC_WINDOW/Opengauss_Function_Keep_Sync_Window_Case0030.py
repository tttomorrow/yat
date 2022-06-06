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
Case Name   : 1主2备环境下(1个同步，1个潜在同步)，1主2同步备，2备机均正常，
              测试keep_sync_window
              参数不生效
Description :
        1.设置以下guc参数
        1.1设置synchronous_standby_names为'dn_6002,dn_6003'
        1.2设置synchronous_commit=on
        1.3设置most_available_sync=on
        1.4设置keep_sync_window=120
        2.查询修改后的参数值
        3.查询集群同步方式
        4.建表
        5.主节点执行DML操作
        6.查看数据是否同步
        7.清理环境
Expect      :
        1.设置成功
        2.修改成功
        3.集群状态为2同步
        4.建表成功
        5.事务提交成功,不会进入最大可用模式
        6.数据同步完成
        7.清理环境完成
"""
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class GucParameters(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0030 start-')
        self.constant = Constant()
        self.common = Common()
        self.standby_sh1 = CommonSH('Standby1DbUser')
        self.standby_sh2 = CommonSH('Standby2DbUser')
        self.db_primary_user_node = Node(node='PrimaryDbUser')
        self.standby_root_node1 = Node(node='Standby1Root')
        self.pri_root_node = Node(node='PrimaryRoot')
        self.default_value1 = self.common.show_param('keep_sync_window')
        self.default_value2 = self.common.show_param(
            'synchronous_standby_names')
        self.default_value3 = self.common.show_param('synchronous_commit')
        self.default_value4 = self.common.show_param('most_available_sync')
        self.tb_name = "tb_keep_sync_window_0030"

    def test_keep_sync_window(self):
        text = '--step1:设置guc参数;expect:设置成功--'
        self.log.info(text)
        self.log.info('设置synchronous_standby_names=dn_6002,dn_6003')
        result = Primary_SH.execute_gsguc("reload",
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"synchronous_standby_names"
                                          f"='dn_6002,dn_6003'",
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
        self.log.info('设置keep_sync_window=120')
        result = Primary_SH.execute_gsguc("reload",
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"keep_sync_window=120")

        self.assertTrue(result, '执行失败' + text)
        result = Primary_SH.restart_db_cluster()
        self.assertTrue(result, '执行失败' + text)

        text = '--step2:查询修改后的参数值;expect:修改成功--'
        self.log.info(text)
        result1 = self.common.show_param('synchronous_standby_names')
        self.assertIn(f"{macro.DN_NODE_NAME.split('/')[1]},"
                      f"{macro.DN_NODE_NAME.split('/')[2]}", result1,
                      '执行失败' + text)
        result2 = self.common.show_param('synchronous_commit')
        self.assertEqual('on', result2, '执行失败' + text)
        result3 = self.common.show_param('most_available_sync')
        self.assertEqual('on', result3, '执行失败' + text)
        result4 = self.common.show_param('keep_sync_window')
        self.assertEqual('2min', result4, '执行失败' + text)

        text = '--step3:查询集群同步方式;expect:集群状态为2同步--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql("select * from "
                                           "pg_stat_replication;")
        self.log.info(sql_cmd)
        self.assertIn('Sync', sql_cmd, '执行失败' + text)
        self.assertIn('Potential', sql_cmd, '执行失败' + text)

        text = '--step4:建表;expect:建表成功--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f"drop table if exists "
                                           f"{self.tb_name};"
                                           f"create table {self.tb_name}"
                                           f"(id int,name text);")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败' + text)

        text = '--step5:主节点执行DML操作;expect:事务提交成功--'
        self.log.info(text)
        sql_cmd = f"insert into {self.tb_name} values(generate_series(1,10)," \
                  f"'column_'|| generate_series(1,10));" \
                  f"update {self.tb_name} set id = id+1;" \
                  f"delete from {self.tb_name};"
        self.log.info(sql_cmd)
        insert_thread = ComThread(Primary_SH.execut_db_sql, args=(sql_cmd,))
        insert_thread.setDaemon(True)
        insert_thread.start()
        self.log.info('获取step6结果，DML操作成功')
        insert_thread.join(10 * 600)
        insert_thread_result = insert_thread.get_result()
        self.log.info(insert_thread_result)
        self.assertTrue(self.constant.INSERT_SUCCESS_MSG in
                        insert_thread_result and
                        self.constant.UPDATE_SUCCESS_MSG in
                        insert_thread_result and
                        self.constant.DELETE_SUCCESS_MSG, '执行失败:' + text)

        text = '----step6:查看数据是否同步;expect:数据同步完成----'
        self.log.info(text)
        sql_cmd = f"select * from {self.tb_name};"
        msg_primary = Primary_SH.execut_db_sql(sql_cmd)
        self.log.info(msg_primary)
        msg_standby1 = self.standby_sh1.execut_db_sql(sql_cmd)
        self.log.info(msg_standby1)
        self.assertEqual(msg_primary, msg_standby1, '执行失败:' + text)
        msg_standby2 = self.standby_sh2.execut_db_sql(sql_cmd)
        self.log.info(msg_standby2)
        self.assertEqual(msg_primary, msg_standby2, '执行失败:' + text)

    def tearDown(self):
        text = '--step7:清理环境;expect:清理环境完成--'
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
        result = Primary_SH.restart_db_cluster()
        self.assertTrue(result, '执行失败' + text)
        self.log.info('断言teardown成功')
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_cmd,
                      '执行失败' + text)
        self.assertEqual(True, result1, '执行失败' + text)
        self.assertEqual(True, result2, '执行失败' + text)
        self.assertEqual(True, result3, '执行失败' + text)
        self.assertEqual(True, result4, '执行失败' + text)
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0030 finish-')

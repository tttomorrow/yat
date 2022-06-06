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
Case Name   : 1主2备下，1同步备1异步备，同步备异常，列存表验证
              keep_sync_window参数
Description :
        1.设置以下guc参数
        1.1设置synchronous_standby_names为'dn_6003'
        1.2设置synchronous_commit=on
        1.3设置most_available_sync=on
        1.4设置keep_sync_window=180
        2.查询修改后的参数值
        3.查询集群同步方式
        4.建表
        5.kill -9备2节点
        6.插入数据
        7.进入最大可用模式后再次插入数据
        8.gs_ctl方式启动同步备
        9.查看数据是否丢失
        10.清理环境
Expect      :
        1.设置成功
        2.修改成功
        3.集群状态为1同步1异步
        4.建表成功
        5.kill成功
        6.主节点阻塞，同步时间窗口内，同步备未恢复连接，进入最大可用模式
        7.插入成功
        8.启动成功
        9.数据未丢失
        10.清理环境完成
"""
import time
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
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0038 start-')
        self.constant = Constant()
        self.common = Common()
        self.standby_sh1 = CommonSH('Standby1DbUser')
        self.standby_sh2 = CommonSH('Standby2DbUser')
        self.db_primary_user_node = Node(node='PrimaryDbUser')
        self.standby_root_node2 = Node(node='Standby2Root')
        self.pri_root_node = Node(node='PrimaryRoot')
        self.default_value1 = self.common.show_param('keep_sync_window')
        self.default_value2 = self.common.show_param(
            'synchronous_standby_names')
        self.default_value3 = self.common.show_param('synchronous_commit')
        self.default_value4 = self.common.show_param('most_available_sync')
        self.tb_name = "tb_keep_sync_window_0038"

    def test_keep_sync_window(self):
        text = '--step1:设置guc参数;expect:设置成功--'
        self.log.info(text)
        self.log.info('设置synchronous_standby_names=dn_6003')
        result = Primary_SH.execute_gsguc("reload",
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"synchronous_standby_names"
                                          f"='dn_6003'",
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
        self.log.info('设置keep_sync_window=180')
        result = Primary_SH.execute_gsguc("reload",
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"keep_sync_window=180")
        self.assertTrue(result, '执行失败' + text)
        self.assertTrue(result, '执行失败' + text)
        result = Primary_SH.restart_db_cluster()
        self.assertTrue(result, '执行失败' + text)

        text = '--step2:查询修改后的参数值;expect:修改成功--'
        self.log.info(text)
        result1 = self.common.show_param('synchronous_standby_names')
        self.assertEqual(macro.DN_NODE_NAME.split('/')[2], result1,
                         '执行失败' + text)
        result2 = self.common.show_param('synchronous_commit')
        self.assertEqual('on', result2, '执行失败' + text)
        result3 = self.common.show_param('most_available_sync')
        self.assertEqual('on', result3, '执行失败' + text)
        result4 = self.common.show_param('keep_sync_window')
        self.assertEqual('3min', result4, '执行失败' + text)

        text = '--step3:查询集群同步方式;expect:集群状态为1同步1异步--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql("select * from "
                                           "pg_stat_replication;")
        self.log.info(sql_cmd)
        self.assertIn('Sync', sql_cmd, '执行失败' + text)
        self.assertIn('Async', sql_cmd, '执行失败' + text)

        text = '--step4:建表;expect:建表成功--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f"drop table if exists "
                                           f"{self.tb_name};"
                                           f"create table {self.tb_name}"
                                           f"(id int,name text)with "
                                           f"(orientation=column);")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败' + text)

        text = '--step5:kill -9同步备;expect:成功--'
        self.log.info(text)
        msg = self.common.kill_pid(self.standby_root_node2, '9')
        self.assertEqual('', msg, '执行失败:' + text)

        text = '--step6:主节点插入数据;expect:主节点阻塞--'
        self.log.info(text)
        sql_cmd = f"select timenow();" \
                  f"insert into {self.tb_name} values(generate_series(1,10)," \
                  f"'column_'|| generate_series(1,10));" \
                  f"select timenow();"
        self.log.info(sql_cmd)
        insert_thread1 = ComThread(Primary_SH.execut_db_sql, args=(sql_cmd,))
        insert_thread1.setDaemon(True)
        insert_thread1.start()
        time.sleep(180)

        self.log.info('获取step6结果,同步时间窗口内，同步备未恢复连接，'
                      '进入最大可用模式，事务自动提交成功')
        insert_thread1.join(10 * 600)
        insert_thread_result1 = insert_thread1.get_result()
        self.log.info(insert_thread_result1)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_thread_result1,
                      '执行失败:' + text)

        text = '--step7:主节点再次插入数据;expect:插入成功--'
        self.log.info(text)
        sql_cmd = f"insert into {self.tb_name} values(generate_series(1,10)," \
                  f"'column_'|| generate_series(1,10));"
        self.log.info(sql_cmd)
        insert_thread2 = ComThread(Primary_SH.execut_db_sql, args=(sql_cmd,))
        insert_thread2.setDaemon(True)
        insert_thread2.start()
        self.log.info('获取step7结果')
        insert_thread2.join(10 * 600)
        insert_thread_result2 = insert_thread2.get_result()
        self.log.info(insert_thread_result2)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_thread_result2,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.keep_sync_window_msg,
                         insert_thread_result2,
                         '执行失败:' + text)
        time.sleep(180)
        text = '--step8:重启同步备;expect:成功--'
        self.log.info(text)
        start_cmd = self.standby_sh2.start_db_instance(mode="standby")
        self.log.info(start_cmd)
        self.assertTrue(start_cmd, '执行失败' + text)

        text = '----step9:查看备机数据是否同步;expect:同步成功----'
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
        text = '--step10:清理环境;expect:清理环境完成--'
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
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0038 finish-')

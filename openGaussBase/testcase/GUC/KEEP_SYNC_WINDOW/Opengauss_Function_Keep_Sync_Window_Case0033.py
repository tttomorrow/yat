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
Case Name   : 1主1备环境下，1主1同步备，测试时间窗口参数
Description :
        1.设置以下三个guc参数
        1.1.设置synchronous_commit=off
        1.2.设置most_available_sync=on
        1.3设置keep_sync_window=120
        2.查询修改后的参数值
        3.建表
        4.kill -9同步备
        5.插入数据
        6.启动同步备
        7.查看备机数据是否同步
        8.清理环境
Expect      :
        1.设置成功
        2.修改成功
        3.建表成功
        4.成功
        5.主节点阻塞，在时间窗口内，同步备未恢复，120s后，主节点插入数据成功，
        进入最大可用模式
        6.启动成功
        7.同步成功
        8.清理环境完成
History     :
"""

import datetime
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(2 != Primary_SH.get_node_num(), '非1主1备环境不执行')
class GucParameters(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0033 start-')
        self.constant = Constant()
        self.common = Common()
        self.standby_sh = CommonSH('Standby1DbUser')
        self.standby_root_node1 = Node(node='Standby1Root')
        self.default_value1 = self.common.show_param('keep_sync_window')
        self.default_value2 = self.common.show_param(
            'synchronous_standby_names')
        self.default_value3 = self.common.show_param('synchronous_commit')
        self.default_value4 = self.common.show_param('most_available_sync')
        self.tb_name = "tb_keep_sync_window_0033"

    def test_keep_sync_window(self):
        text = '--step1:设置以下三个guc参数;expect:设置成功--'
        self.log.info(text)
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
        result1 = self.common.show_param('synchronous_commit')
        self.assertEqual('on', result1, '执行失败' + text)
        result2 = self.common.show_param('most_available_sync')
        self.assertEqual('on', result2, '执行失败' + text)
        result3 = self.common.show_param('keep_sync_window')
        self.assertEqual('2min', result3, '执行失败' + text)

        text = '--step3:建表;expect:建表成功--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f"drop table if exists "
                                           f"{self.tb_name};"
                                           f"create table {self.tb_name}"
                                           f"(id int,name text);")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败' + text)

        text = '--step4:kill -9同步备;expect:成功--'
        self.log.info(text)
        msg = self.common.kill_pid(self.standby_root_node1, '9')
        self.assertEqual('', msg, '执行失败:' + text)

        text = '--step5:插入数据;expect:主节点阻塞，在时间窗口内，' \
               '同步备未恢复，120s后，主节点插入数据成功，进入最大可用模式--'
        self.log.info(text)
        sql_cmd = f"select timenow();" \
                  f"insert into {self.tb_name} values" \
                  f"(generate_series(1,10),'column_'|| " \
                  f"generate_series(1,10));" \
                  f"select timenow();"
        insert_thread = ComThread(Primary_SH.execut_db_sql, args=(sql_cmd,))
        insert_thread.setDaemon(True)
        insert_thread.start()
        time.sleep(120)

        self.log.info('获取step6插入前以及插入成功后阻塞时间;'
                      '阻塞时间近似于keep_sync_window参数时间')
        self.log.info(text)
        insert_thread.join(10 * 600)
        insert_thread_result = insert_thread.get_result()
        self.log.info(insert_thread_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_thread_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.keep_sync_window_msg,
                      insert_thread_result, '执行失败:' + text)
        msg = insert_thread_result.splitlines()
        self.log.info(msg)
        start_time = insert_thread_result.splitlines()[2].strip()[:-3]
        self.log.info(start_time)
        trans_to_dtime1 = datetime.datetime.strptime(start_time,
                                                     '%Y-%m-%d %H:%M:%S')
        end_time = insert_thread_result.splitlines()[-2].strip()[:-3]
        self.log.info(end_time)
        trans_to_dtime2 = datetime.datetime.strptime(end_time,
                                                     '%Y-%m-%d %H:%M:%S')
        time_diff = trans_to_dtime2 - trans_to_dtime1
        self.log.info(time_diff)
        num = str(time_diff).split(':', 1)[-1]
        self.log.info(f'阻塞时间为{num}min')
        self.assertGreaterEqual(f'{num}', '01:30', '执行失败:' + text)

        text = '--step6:gs_ctl方式启动备节点;expect:启动成功--'
        self.log.info(text)
        start_cmd = self.standby_sh.start_db_instance(mode="standby")
        self.log.info(start_cmd)
        self.assertTrue(start_cmd, '执行失败' + text)

        text = '----step7:查看备机数据是否同步;expect:同步成功----'
        self.log.info(text)
        sql_cmd = f"select * from {self.tb_name};"
        msg_primary = Primary_SH.execut_db_sql(sql_cmd)
        self.log.info(msg_primary)
        msg_standby = self.standby_sh.execut_db_sql(sql_cmd)
        self.log.info(msg_standby)
        self.assertEqual(msg_primary, msg_standby, '执行失败:' + text)

    def tearDown(self):
        text = '--step9:清理环境;expect:清理环境完成--'
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
        restart_cmd = Primary_SH.restart_db_cluster()
        self.log.info(restart_cmd)
        self.log.info('断言teardown成功')
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_cmd,
                      '执行失败' + text)
        self.assertEqual(True, result1, '执行失败' + text)
        self.assertEqual(True, result2, '执行失败' + text)
        self.assertEqual(True, result3, '执行失败' + text)
        self.assertTrue(restart_cmd, '执行失败' + text)
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0033 finish-')

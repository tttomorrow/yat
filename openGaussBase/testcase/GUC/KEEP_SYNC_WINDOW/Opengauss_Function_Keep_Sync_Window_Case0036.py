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
Case Name   : 1主2备下，1同步备1异步备，同步备异常，时间窗内一个session
              插入数据，另一个session查询数据
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
        7.另一session查询系统表
        8.另一session查询step6的表
        9.获取step6插入前以及插入成功后阻塞时间
        10.获取step8查询前以及查询成功后阻塞时间
        11.gs_ctl方式启动备2节点
        12.查看数据是否丢失
        13.清理环境
Expect      :
        1.设置成功
        2.修改成功
        3.集群状态为1同步1异步
        4.建表成功
        5.kill成功
        6.主节点阻塞
        7.查询成功，不阻塞
        8.同步时间窗内同步备未恢复，主机插入成功，进入最大可用模式；
        此session查询成功
        9.获取成功，阻塞时间近似于keep_sync_window的时间
        10.获取成功，阻塞时间近似于keep_sync_window的时间
        11.启动成功
        12.数据未丢失
        13.清理环境完成
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
from yat.test import macro

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class GucParameters(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0036 start-')
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
        self.tb_name = "tb_keep_sync_window_0036"

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
                                           f"(id int,name text);")
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
        insert_thread = ComThread(Primary_SH.execut_db_sql, args=(sql_cmd,))
        insert_thread.setDaemon(True)
        insert_thread.start()

        text = '--step7:另一session查询系统表;expect:查询成功,不阻塞--'
        self.log.info(text)
        sql_cmd = f"select count(*) from pg_settings;"
        self.log.info(sql_cmd)
        select_thread = ComThread(Primary_SH.execut_db_sql, args=(sql_cmd,))
        select_thread.setDaemon(True)
        select_thread.start()
        select_thread.join(10 * 600)
        select_thread_result = select_thread.get_result()
        self.log.info(select_thread_result)
        self.assertIn('1 row', select_thread_result, '执行失败:' + text)

        text = '--step8:另一session查询step6的表;' \
               'expect:同步时间窗内同步备未恢复，超过keep_sync_window时间，' \
               '进入最大可用模式,step6插入成功;此session查询成功--'
        self.log.info(text)
        sql_cmd = f"select timenow();" \
                  f"select count(*) from {self.tb_name};" \
                  f"select timenow();"
        self.log.info(sql_cmd)
        query_thread = ComThread(Primary_SH.execut_db_sql, args=(sql_cmd,))
        query_thread.setDaemon(True)
        query_thread.start()
        time.sleep(185)

        text = '--step9:超过keep_sync_window的时间，获取step6结果;' \
               'expect:插入成功--'
        self.log.info(text)
        insert_thread.join(10 * 600)
        insert_thread_result = insert_thread.get_result()
        self.log.info(insert_thread_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_thread_result,
                      '执行失败:' + text)

        text = '--step10:获取step8查询前以及查询成功后阻塞时间;' \
               'expect:获取成功,阻塞时间接近keep_sync_window的时间--'
        self.log.info(text)
        query_thread.join(10 * 600)
        query_thread_result = query_thread.get_result()
        self.log.info(query_thread_result)
        msg = query_thread_result.splitlines()
        self.log.info(msg)
        start_time = query_thread_result.splitlines()[2].strip()[:-3]
        self.log.info(start_time)
        trans_to_dtime1 = datetime.datetime.strptime(start_time,
                                                     '%Y-%m-%d %H:%M:%S')
        end_time = query_thread_result.splitlines()[-2].strip()[:-3]
        self.log.info(end_time)
        trans_to_dtime2 = datetime.datetime.strptime(end_time,
                                                     '%Y-%m-%d %H:%M:%S')
        time_diff = trans_to_dtime2 - trans_to_dtime1
        self.log.info(time_diff)
        num = str(time_diff).split(':', 1)[-1]
        self.log.info(f'阻塞时间为{num}min')
        self.assertGreaterEqual(f'{num}min', '02:59', '执行失败:' + text)
        self.assertIn('10', query_thread_result, '执行失败:' + text)

        time.sleep(200)
        text = '--step11:重启同步备;expect:成功--'
        self.log.info(text)
        start_cmd = self.standby_sh2.start_db_instance(mode="standby")
        self.log.info(start_cmd)
        self.assertTrue(start_cmd, '执行失败' + text)

        text = '----step12:查看备机数据是否同步;expect:同步成功----'
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
        text = '--step13:清理环境;expect:清理环境完成--'
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
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0036 finish-')

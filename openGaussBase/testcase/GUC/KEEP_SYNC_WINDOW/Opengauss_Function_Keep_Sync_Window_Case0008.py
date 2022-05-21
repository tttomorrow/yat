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
Case Name   : synchronous_commit参数为on，most_available_sync为off，
              keep_sync_window等于0，测试时间窗口参数是否有效
Description :
        1.设置以下三个guc参数
        1.1.设置synchronous_commit=on
        1.2.设置most_available_sync=off
        1.3设置keep_sync_window=0
        2.查询修改后的参数值
        3.建表
        4.停止集群
        5.gs_ctl方式启动主节点
        6.插入数据
        7.启动同步备
        8.查看备机数据是否同步
        9.清理环境
Expect      :
        1.设置成功
        2.修改成功
        3.建表成功
        4.停止集群成功
        5.启动成功
        6.主节点阻塞，不会进入最大可用模式
        7.启动成功，同步备恢复连接，主节点插入成功
        8.同步成功
        9.清理环境完成
History     :
"""
import time
import unittest

from testcase.utils.ComThread import ComThread
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger

Primary_SH = CommonSH('PrimaryDbUser')


@unittest.skipIf(3 != Primary_SH.get_node_num(), '非1+2环境不执行')
class GucParameters(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0008 start-')
        self.constant = Constant()
        self.common = Common()
        self.standby_sh1 = CommonSH('Standby1DbUser')
        self.standby_sh2 = CommonSH('Standby2DbUser')
        self.default_value1 = self.common.show_param('keep_sync_window')
        self.default_value2 = self.common.show_param(
            'synchronous_standby_names')
        self.default_value3 = self.common.show_param('synchronous_commit')
        self.default_value4 = self.common.show_param('most_available_sync')
        self.tb_name = "tb_keep_sync_window_0008"

    def test_keep_sync_window(self):
        text = '--step1:设置以下三个guc参数;expect:设置成功--'
        self.log.info(text)
        self.log.info('设置synchronous_commit=on')
        result = Primary_SH.execute_gsguc("reload",
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"synchronous_commit=on")

        self.assertTrue(result, '执行失败' + text)
        self.log.info('设置most_available_sync=off')
        result = Primary_SH.execute_gsguc("reload",
                                          self.constant.GSGUC_SUCCESS_MSG,
                                          f"most_available_sync=off")

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

        text = '--step2:查询修改后的参数值;expect:修改成功--'
        self.log.info(text)
        result1 = self.common.show_param('synchronous_commit')
        self.assertEqual('on', result1, '执行失败' + text)
        result2 = self.common.show_param('most_available_sync')
        self.assertEqual('off', result2, '执行失败' + text)
        result3 = self.common.show_param('keep_sync_window')
        self.assertEqual('0', result3, '执行失败' + text)

        text = '--step3:建表;expect:建表成功--'
        self.log.info(text)
        sql_cmd = Primary_SH.execut_db_sql(f"drop table if exists "
                                           f"{self.tb_name};"
                                           f"create table {self.tb_name}"
                                           f"(id int,name text);")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败' + text)

        text = '--step4:停止集群;expect:停止成功--'
        self.log.info(text)
        stop_cmd = Primary_SH.stop_db_cluster()
        self.log.info(stop_cmd)
        self.assertTrue(stop_cmd, '执行失败' + text)

        text = '--step5:gs_ctl方式启动主节点;expect:启动成功--'
        self.log.info(text)
        start_cmd = Primary_SH.start_db_instance(mode="primary")
        self.log.info(start_cmd)
        self.assertTrue(start_cmd, '执行失败' + text)

        text = '--step6:插入数据;expect:主节点阻塞, 不会进入最大可用模式--'
        self.log.info(text)
        sql_cmd = f"insert into {self.tb_name} values" \
                  f"(generate_series(1,10),'column_'|| generate_series(1,10));"
        insert_thread = ComThread(Primary_SH.execut_db_sql,
                                  args=(sql_cmd,))
        insert_thread.setDaemon(True)
        insert_thread.start()
        time.sleep(60)

        text = '--step7:启动同步备;expect:启动成功--'
        self.log.info(text)
        start_cmd = self.standby_sh1.start_db_instance(mode="standby")
        self.log.info(start_cmd)
        self.assertTrue(start_cmd, '执行失败' + text)
        start_cmd = self.standby_sh2.start_db_instance(mode="standby")
        self.log.info(start_cmd)
        self.assertTrue(start_cmd, '执行失败' + text)
        self.log.info('获取step6结果，同步备启动后，主节点插入成功')
        insert_thread.join(10 * 60)
        insert_thread_result = insert_thread.get_result()
        self.log.info(insert_thread_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_thread_result,
                      '执行失败:' + text)
        self.assertNotIn(self.constant.keep_sync_window_msg,
                         insert_thread_result, '执行失败:' + text)

        text = '----step8:查看备机数据是否同步;expect:同步成功----'
        self.log.info(text)
        sql_cmd = f"select * from {self.tb_name};"
        msg_primary = Primary_SH.execut_db_sql(sql_cmd)
        self.log.info(msg_primary)
        msg_standby = self.standby_sh1.execut_db_sql(sql_cmd)
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
        self.log.info('断言teardown成功')
        restart_cmd = Primary_SH.restart_db_cluster()
        self.log.info(restart_cmd)
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_cmd,
                      '执行失败' + text)
        self.assertEqual(True, result1, '执行失败' + text)
        self.assertEqual(True, result2, '执行失败' + text)
        self.assertEqual(True, result3, '执行失败' + text)
        self.assertTrue(restart_cmd, '执行失败' + text)
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0008 finish-')

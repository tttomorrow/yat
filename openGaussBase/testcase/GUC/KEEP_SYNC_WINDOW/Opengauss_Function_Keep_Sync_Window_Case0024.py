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
Case Name   : switchover后，同步备异常，验证时间窗口参数是否生效
Description :
        1.执行switchover
        2.switchover后查询参数默认值
        3.设置guc参数
        3.1设置synchronous_standby_names为'dn_6001'
        3.2设置synchronous_commit=on
        3.3设置most_available_sync=on
        3.4设置keep_sync_window=180
        4.查询修改后的参数值
        5.查询集群同步方式
        6.建表
        7.kill -9备1节点
        8.插入数据
        9.gs_ctl方式启动备1节点
        10.查看备机数据是否同步
        11.清理环境
Expect      :
        1.成功
        2.和switchover前一致
        3.设置成功
        4.设置成功
        5.集群状态为1同步1异步
        6.成功
        7.kill成功
        8.时间窗内同步备未恢复连接;180s后进入最大可用模式，数据插入成功
        9.启动成功
        10.同步成功
        11.清理环境完成
History     :
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
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0024 start-')
        self.constant = Constant()
        self.common = Common()
        self.standby_sh1 = CommonSH('Standby1DbUser')
        self.standby_sh2 = CommonSH('Standby2DbUser')
        self.db_primary_user_node = Node(node='PrimaryDbUser')
        self.db_standby1_user_node = Node(node='Standby1DbUser')
        self.standby_root_node1 = Node(node='Standby1Root')
        self.log.info('switchover前查询参数默认值')
        self.default_value1 = self.common.show_param('keep_sync_window')
        self.default_value2 = self.common.show_param(
            'synchronous_standby_names')
        self.default_value3 = self.common.show_param('synchronous_commit')
        self.default_value4 = self.common.show_param('most_available_sync')
        self.stand_value = self.standby_sh1.execut_db_sql(
            'show synchronous_standby_names;')
        self.tb_name = "tb_keep_sync_window_0024"

    def test_keep_sync_window(self):
        text = '--step1:执行switchover;expect:成功--'
        self.log.info(text)
        excute_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_ctl switchover -D {macro.DB_INSTANCE_PATH} -m fast ;"
        self.log.info(excute_cmd)
        excute_msg = self.db_standby1_user_node.sh(excute_cmd).result()
        self.log.info(excute_msg)
        self.assertIn(self.constant.SWITCHOVER_SUCCESS_MSG, excute_msg,
                      '执行失败' + text)
        text = '--step1.1:进行refreshconf;expect:成功--'
        self.log.info(text)
        excute_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_om -t refreshconf;"
        self.log.info(excute_cmd)
        excute_msg = self.db_standby1_user_node.sh(excute_cmd).result()
        self.log.info(excute_msg)
        self.assertIn(self.constant.REFRESHCONF_SUCCESS_MSG, excute_msg,
                      '执行失败' + text)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)

        text = '--step2:switchover后查询参数默认值;expect:和switchover前一致--'
        self.log.info(text)
        new_value1 = self.standby_sh1.execut_db_sql('show keep_sync_window;')
        self.log.info(new_value1)
        self.assertEqual(self.default_value1,
                         new_value1.splitlines()[2].strip(), '执行失败' + text)
        new_value2 = self.standby_sh1.execut_db_sql(
            'show synchronous_standby_names;')
        self.log.info(new_value2)
        self.assertEqual(self.stand_value.splitlines()[2].strip(),
                         new_value2.splitlines()[2].strip(), '执行失败' + text)
        new_value3 = self.standby_sh1.execut_db_sql('show synchronous_commit;')
        self.log.info(new_value3)
        self.assertEqual(self.default_value3,
                         new_value3.splitlines()[2].strip(), '执行失败' + text)
        new_value4 = self.standby_sh1.execut_db_sql(
            'show most_available_sync;')
        self.log.info(new_value4)
        self.assertEqual(self.default_value4,
                         new_value4.splitlines()[2].strip(), '执行失败' + text)

        text = '--step3:设置guc参数;expect:设置成功--'
        self.log.info(text)
        self.log.info('设置synchronous_commit=on')
        result = self.standby_sh1.execute_gsguc("reload",
                                                self.constant.GSGUC_SUCCESS_MSG,
                                                f"synchronous_commit=on")

        self.assertTrue(result, '执行失败' + text)
        self.log.info('设置most_available_sync=on')
        result = self.standby_sh1.execute_gsguc("reload",
                                                self.constant.GSGUC_SUCCESS_MSG,
                                                f"most_available_sync=on")

        self.assertTrue(result, '执行失败' + text)
        self.log.info('设置keep_sync_window=180')
        result = self.standby_sh1.execute_gsguc("reload",
                                                self.constant.GSGUC_SUCCESS_MSG,
                                                f"keep_sync_window=180")

        self.assertTrue(result, '执行失败' + text)
        result = self.standby_sh1.restart_db_cluster()
        self.assertTrue(result, '执行失败' + text)

        text = '--step4:查询修改后的参数值;expect:修改成功--'
        self.log.info(text)
        result1 = self.standby_sh1.execut_db_sql('show synchronous_commit;')
        self.log.info(result1)
        self.assertIn('on', result1, '执行失败' + text)
        result2 = self.standby_sh1.execut_db_sql('show most_available_sync;')
        self.log.info(result2)
        self.assertIn('on', result2, '执行失败' + text)
        result3 = self.standby_sh1.execut_db_sql('show keep_sync_window;')
        self.log.info(result3)
        self.assertIn('3min', result3, '执行失败' + text)

        text = '--step5:建表;expect:成功--'
        self.log.info(text)
        sql_cmd = self.standby_sh1.execut_db_sql(f"drop table if exists "
                                                 f"{self.tb_name};"
                                                 f"create table {self.tb_name}"
                                                 f"(id int,name text);")
        self.log.info(sql_cmd)
        self.assertIn(self.constant.TABLE_CREATE_SUCCESS, sql_cmd,
                      '执行失败' + text)

        text = '--step6:停止集群;expect:停止成功--'
        self.log.info(text)
        stop_cmd = self.standby_sh1.stop_db_cluster()
        self.log.info(stop_cmd)
        self.assertTrue(stop_cmd, '执行失败' + text)

        text = '--step7:gs_ctl方式启动主节点;expect:启动成功--'
        self.log.info(text)
        start_cmd = self.standby_sh1.start_db_instance(mode="primary")
        self.log.info(start_cmd)
        self.assertTrue(start_cmd, '执行失败' + text)

        text = '--step8:主节点插入数据;expect:时间窗内同步备未恢复连接；' \
               '180s后进入最大可用模式，数据插入成功--'
        self.log.info(text)
        sql_cmd = f"insert into {self.tb_name} values(generate_series(1,10)," \
                  f"'column_'|| generate_series(1,10));"
        self.log.info(sql_cmd)
        insert_thread = ComThread(self.standby_sh1.execut_db_sql,
                                  args=(sql_cmd,))
        insert_thread.setDaemon(True)
        insert_thread.start()

        self.log.info('获取step6结果')
        insert_thread.join(10 * 600)
        insert_thread_result = insert_thread.get_result()
        self.log.info(insert_thread_result)
        self.assertIn(self.constant.INSERT_SUCCESS_MSG, insert_thread_result,
                      '执行失败:' + text)
        self.assertIn(self.constant.keep_sync_window_msg, insert_thread_result,
                      '执行失败:' + text)

        time.sleep(180)

        text = '--step9:启动集群;expect:启动成功--'
        self.log.info(text)
        start_cmd = self.standby_sh1.restart_db_cluster()
        self.log.info(start_cmd)
        self.assertTrue(start_cmd, '执行失败' + text)

        text = '----step10:查看备机数据是否同步;expect:同步成功----'
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
        text = '--step11:清理环境;expect:清理环境完成--'
        self.log.info(text)
        self.log.info('删表')
        drop_cmd = self.standby_sh1.execut_db_sql(f"drop table if exists "
                                                  f"{self.tb_name};")
        self.log.info(drop_cmd)
        self.log.info('恢复参数默认值')
        res1 = self.standby_sh1.execute_gsguc("reload",
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"synchronous_commit="
                                              f"{self.default_value3}")

        res2 = self.standby_sh1.execute_gsguc("reload",
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"most_available_sync="
                                              f"{self.default_value4}")

        res3 = self.standby_sh1.execute_gsguc("reload",
                                              self.constant.GSGUC_SUCCESS_MSG,
                                              f"keep_sync_window="
                                              f"{self.default_value1}")
        result = self.standby_sh1.stop_db_cluster()
        self.assertTrue(result, '执行失败' + text)
        result = self.standby_sh1.restart_db_cluster()
        self.assertTrue(result, '执行失败' + text)

        self.log.info('恢复原主备关系')
        excute_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_ctl switchover -D {macro.DB_INSTANCE_PATH} -m fast ;"
        self.log.info(excute_cmd)
        excute_msg = self.db_primary_user_node.sh(excute_cmd).result()
        self.log.info(excute_msg)
        self.assertIn(self.constant.SWITCHOVER_SUCCESS_MSG, excute_msg,
                      '执行失败' + text)
        excute_cmd = f"source {macro.DB_ENV_PATH};" \
                     f"gs_om -t refreshconf;"
        self.log.info(excute_cmd)
        excute_msg = self.db_primary_user_node.sh(excute_cmd).result()
        self.log.info(excute_msg)
        self.assertIn(self.constant.REFRESHCONF_SUCCESS_MSG, excute_msg,
                      '执行失败' + text)
        restart_msg = Primary_SH.restart_db_cluster()
        self.log.info(restart_msg)
        status = Primary_SH.get_db_cluster_status()
        self.assertTrue("Degraded" in status or "Normal" in status)
        self.log.info('断言teardown成功')
        self.assertIn(self.constant.TABLE_DROP_SUCCESS, drop_cmd,
                      '执行失败' + text)
        self.assertEqual(True, res1, '执行失败' + text)
        self.assertEqual(True, res2, '执行失败' + text)
        self.assertEqual(True, res3, '执行失败' + text)
        self.log.info('-Opengauss_Function_Keep_Sync_Window_Case0024 finish-')

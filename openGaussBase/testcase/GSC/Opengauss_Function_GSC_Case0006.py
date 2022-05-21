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
Case Type   : GSC功能模块
Case Name   : enable_global_syscache参数打开关闭来回切换，枚举参数值验证
Description :
    0、查看enable_global_syscache初始配置值;
    1、修改参数enable_global_syscache为0;
    2、重启数据库，使参数生效;
    3、alter system方式修改参数enable_global_syscache为1;
    4、重启数据库，使参数生效;
    5、修改参数enable_global_syscache为false;
    6、重启数据库，使参数生效;
    7、修改参数enable_global_syscache为true;
    8、重启数据库，使参数生效;
    9、guc修改enable_global_syscache为默认值;
    10、重启数据库，使参数生效;
    11、查询数据库状态;
Expect      :
    0、查看enable_global_syscache初始配置值;
    1、修改参数enable_global_syscache为0; 成功
    2、重启数据库，重启成功，参数生效;
    3、alter system方式修改参数enable_global_syscache为1; 成功
    4、重启数据库，重启成功，参数生效;
    5、修改参数enable_global_syscache为false; 成功
    6、重启数据库，重启成功，参数生效;
    7、修改参数enable_global_syscache为true; 成功
    8、重启数据库，重启成功，参数生效;
    9、guc修改enable_global_syscache为默认值; 成功
    10、重启数据库，重启成功，参数生效;
    11、查询数据库状态; 状态正常
History     :
"""
import os
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class GscTestCase(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'----{os.path.basename(__file__)}:start----')
        self.sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()
        step_txt = '----step0:查看enable_global_syscache初始配置值;----'
        self.log.info(step_txt)
        self.init_para = self.com.show_param("enable_global_syscache")

    def test_main(self):
        step_txt = '----step1:修改参数enable_global_syscache为0; expect:成功----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache= 0")
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step2:重启数据库，使参数生效; expect:重启成功----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster()
        self.assertTrue(restart_result)
        self.log.info('----查询参数----')
        self.new_para = self.com.show_param("enable_global_syscache")
        self.assertEqual(self.new_para, 'off', '执行失败:' + step_txt)

        step_txt = '----step3:alter system方式修改参数enable_global_syscache为1; ' \
                   'expect:成功----'
        self.log.info(step_txt)
        alter_sql = 'alter system set enable_global_syscache to 1;'
        result = self.sh.execut_db_sql(alter_sql)
        self.log.info(result)
        self.assertIn(self.constant.alter_system_success_msg, result,
                      '执行失败:' + step_txt)

        step_txt = '----step4:重启数据库，使参数生效; expect:重启成功，参数生效;----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster()
        self.assertTrue(restart_result)
        self.log.info('----查询参数----')
        self.new_para = self.com.show_param("enable_global_syscache")
        self.assertEqual(self.new_para, 'on', '执行失败:' + step_txt)

        step_txt = '----step5:修改参数enable_global_syscache为false; expect:成功----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache= false")
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step6:重启数据库，使参数生效; expect:重启成功，参数生效;----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster()
        self.assertTrue(restart_result)
        self.log.info('----查询参数----')
        self.new_para = self.com.show_param("enable_global_syscache")
        self.assertEqual(self.new_para, 'off', '执行失败:' + step_txt)

        step_txt = '----step7:修改参数enable_global_syscache为true; expect:成功----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache= 1")
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step8:重启数据库，使参数生效; expect:重启成功，参数生效;----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster()
        self.assertTrue(restart_result)
        self.log.info('----查询参数----')
        self.new_para = self.com.show_param("enable_global_syscache")
        self.assertEqual(self.new_para, 'on', '执行失败:' + step_txt)

        step_txt = '----step9:guc修改enable_global_syscache为默认值; expect:成功----'
        self.log.info(step_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache")
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step10:重启数据库，使参数生效; expect:重启成功，参数生效;----'
        self.log.info(step_txt)
        restart_result = self.sh.restart_db_cluster()
        self.assertTrue(restart_result, '执行失败:' + step_txt)
        self.log.info('----查询参数----')
        self.new_para = self.com.show_param("enable_global_syscache")
        self.assertEqual(self.new_para, 'on', '执行失败:' + step_txt)

        step_txt = '----step11:查询数据库状态; expect:状态正常----'
        self.log.info(step_txt)
        status_result = self.sh.get_db_cluster_status('status')
        self.assertTrue(status_result, '执行失败:' + step_txt)

    def tearDown(self):
        step_txt = '----this is teardown----'
        self.log.info(step_txt)
        step1_txt = '----teardown:还原参数enable_global_syscache为初始值; ' \
                    'expect:修改成功----'
        self.log.info(step1_txt)
        msg = self.sh.execute_gsguc('set',
                                    self.constant.GSGUC_SUCCESS_MSG,
                                    f"enable_global_syscache="
                                    f"{self.init_para}")
        step2_txt = '----teardown:重启数据库，使参数生效; expect:重启成功----'
        self.log.info(step2_txt)
        restart_result = self.sh.restart_db_cluster()

        self.log.info(f'----{os.path.basename(__file__)}:end----')
        self.assertTrue(msg, '执行失败:' + step_txt + step1_txt)
        self.assertTrue(restart_result, '执行失败:' + step_txt + step2_txt)

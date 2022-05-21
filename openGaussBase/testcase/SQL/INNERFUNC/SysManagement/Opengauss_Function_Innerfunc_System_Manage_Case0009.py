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
Case Type   : 系统管理函数-其他函数
Case Name   : 使用函数local_double_write_stat()显示本实例的双写文件的情况
Description :
    1.查看并设置参数默认值
    2.使用函数local_double_write_stat()显示本实例的双写文件的情况
    3.恢复参数默认值
Expect      :
    1.执行成功
    2.使用函数local_double_write_stat()显示本实例的双写文件的情况成功
    3.恢复参数默认值成功
History     :
    modified by hsl5321994 2022/3/9 新增查看参数enable_incremental_checkpoint默认值操作
"""

import unittest
import os
from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.commonsh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.com = Common()

        text = '-----step1 查看并设置参数默认值;expect:执行成功-----'
        self.default_value = self.com.show_param(
            "enable_incremental_checkpoint")
        self.log.info(f'self.default_value ={self.default_value}')
        self.config_item = 'enable_incremental_checkpoint=on'
        check_res = self.commonsh.execut_db_sql(
            f'checkpoint;')
        self.log.info(check_res)
        self.assertIn(self.constant.CHECKPOINT_SUCCESS_MSG, check_res,
                      '执行失败:' + text)
        if 'on' != self.default_value:
            self.commonsh.execute_gsguc(
                'set', self.constant.GSGUC_SUCCESS_MSG, self.config_item)
            self.commonsh.restart_db_cluster()
            result = self.commonsh.get_db_cluster_status()
            self.assertTrue('Degraded' in result or 'Normal' in result,
                            '执行失败:' + text)

    def test_func_sys_manage(self):
        text = '-----step2 使用函数local_double_write_stat()显示本实例的双写文件的情况' \
               ';expect:显示成功-----'
        sql_cmd = self.commonsh.execut_db_sql(f'select '
                                              f'local_double_write_stat();')
        self.log.info(sql_cmd)
        self.assertIn('1 row', sql_cmd)
        list1 = sql_cmd.split('\n')[2]
        list2 = list1.split(',')
        self.log.info(len(list2))
        self.assertEqual(len(list2), 12, '执行失败:' + text)

    def tearDown(self):
        text = '-----step3 恢复参数默认值;expect:恢复成功-----'
        self.log.info(text)
        check_res = self.commonsh.execut_db_sql(f'checkpoint;')
        self.log.info(check_res)
        self.assertIn(self.constant.CHECKPOINT_SUCCESS_MSG, check_res,
                      '执行失败:' + text)
        msg8 = self.commonsh.execute_gsguc('set',
                                           self.constant.GSGUC_SUCCESS_MSG,
                                           f"enable_incremental_checkpoint="
                                           f"{self.default_value}")
        self.log.info(msg8)
        restart_msg = self.commonsh.restart_db_cluster()
        self.log.info(restart_msg)
        status = self.commonsh.get_db_cluster_status('detail')
        self.log.info(status)
        self.recovery_value = self.com.show_param(
            "enable_incremental_checkpoint")
        self.assertTrue("Degraded" in status or "Normal" in status,
                        '执行失败' + text)
        self.assertEqual(self.recovery_value, self.default_value,
                         '执行失败:' + text)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

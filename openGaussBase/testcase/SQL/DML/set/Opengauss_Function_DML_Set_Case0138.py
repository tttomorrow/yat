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
Case Type   : 功能测试
Case Name   : 对外表进行analyse
Description :
    1.设置参数enable_incremental_checkpoint为off并重启检查生效
    2.创建外表并对其进行analyse
    3.删除表,恢复参数enable_incremental_checkpoint为默认值并重启检查生效
Expect      : 
    1.默认值是off,设置成功
    2.外表创建成功,analyse执行成功
    3.删除成功,设置成功,恢复为默认值
History     :
"""
import os
import unittest

from testcase.utils.Logger import Logger
from testcase.utils.Constant import Constant
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Common import Common


class Function(unittest.TestCase):

    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.common = Common()
        self.t_name = 't_dml_set_0138'
        self.default_value = self.common.show_param(
            'enable_incremental_checkpoint')

    def test_test_directory(self):
        text = '-----step1:设置参数enable_incremental_checkpoint为off并重启检查生效 ' \
               'expect:成功-----'
        self.log.info(text)
        mod_msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            'enable_incremental_checkpoint='
                                            'off')
        self.assertTrue(mod_msg, '执行失败:' + text)
        restart_res = self.pri_sh.restart_db_cluster()
        self.assertTrue(restart_res, '执行失败' + text)
        param_value = self.common.show_param('enable_incremental_checkpoint')
        self.assertEqual('off', param_value, '执行失败:' + text)

        text = '-----step2：创建外表并对其进行analyse; expect:成功-----'
        self.log.info(text)
        sql_cmd = f'drop foreign table if exists {self.t_name};' \
            f'create foreign table {self.t_name}(x int);' \
            f'analyze verbose {self.t_name};'
        sql_res = self.pri_sh.execut_db_sql(sql_cmd)
        self.log.info(sql_res)
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG and
                      self.constant.CREATE_FOREIGN_SUCCESS_MSG and
                      f'INFO:  analyzing "public.{self.t_name}"', sql_res,
                      '执行失败:' + text)

    def tearDown(self):
        self.log.info('-----step3：清理环境-----')
        text = '-----删除外表; expect:成功-----'
        self.log.info(text)
        drop_cmd = f'drop foreign table if exists {self.t_name};'
        drop_res = self.pri_sh.execut_db_sql(drop_cmd)
        self.log.info(drop_res)

        text1 = '-----恢复参数enable_incremental_checkpoint默认值并重启; expect:成功-----'
        self.log.info(text1)
        check_res = self.pri_sh.execut_db_sql(f'checkpoint;')
        self.log.info(check_res)
        self.assertIn(self.constant.CHECKPOINT_SUCCESS_MSG, check_res,
                      '执行失败:' + text1)
        mod_msg = self.pri_sh.execute_gsguc('set',
                                            self.constant.GSGUC_SUCCESS_MSG,
                                            f'enable_incremental_checkpoint='
                                            f'{self.default_value}')
        restart_res = self.pri_sh.restart_db_cluster()

        text2 = '-----查看参数值; expect:成功-----'
        self.log.info(text2)
        value1 = self.common.show_param('enable_incremental_checkpoint')

        self.log.info('-----断言tearDown执行成功-----')
        self.assertIn(self.constant.DROP_FOREIGN_SUCCESS_MSG, drop_res,
                      '执行失败:' + text)
        self.assertTrue(mod_msg and restart_res, '执行失败:' + text1)
        self.assertEqual(self.default_value, value1, '执行失败:' + text2)
        self.log.info(f'-----{os.path.basename(__file__)} end-----')

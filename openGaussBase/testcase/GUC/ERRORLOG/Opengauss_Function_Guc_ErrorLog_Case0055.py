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
Case Type   : GUC_ErrorLog
Case Name   : 设置参数client_min_messages的值为panic，系统默认将级别转为error
Description :
    1.修改参数client_min_messages值为panic
    2.查看修改后参数
Expect      :
    1.修改参数client_min_messages值为panic成功
    2.查看修改后参数为error
History     :
"""
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class ErrorLog(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Guc_ErrorLog_Case0055 start--')
        self.userNode = Node('PrimaryDbUser')
        self.pri_root = Node('PrimaryRoot')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()

    def test_main(self):
        step_txt = '----查询原client_min_messages参数配置值; ----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show client_min_messages;')
        self.log.info(f"client_min_messages is {result}")
        self.para1 = result.strip().splitlines()[-2]

        step_txt = '----step1:修改参数client_min_messages值为panic; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'client_min_messages=panic')
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step2:查看修改后参数; expect:查看修改后的参数为error----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show client_min_messages;')
        self.log.info(f"client_min_messages is {result}")
        new_para = result.strip().splitlines()[-2].strip()
        self.assertEqual(new_para, 'error', '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        self.log.info('----恢复参数client_min_messages值为初始值----')
        self.pri_sh.execute_gsguc('reload',
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f'client_min_messages={self.para1}')
        result = self.pri_sh.execut_db_sql('show client_min_messages;')
        self.log.info(f"client_min_messages is {result}")

        self.log.info('--Opengauss_Function_Guc_ErrorLog_Case0055 finish--')

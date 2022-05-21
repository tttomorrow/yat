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
Case Name   : 参数log_rotation_age的值设置为1，验证新日志文件的创建时间间隔是否为1min
Description :
    1.修改参数log_rotation_age的值为1;
    2.查看返回值：show log_rotation_age;
    3.进入log_directory目录，验证1min后是否生成新的pglog文件
Expect      :
    1.修改参数log_rotation_age的值为1;修改成功
    2.查看返回值：show log_rotation_age，为1
    3.进入log_directory目录，验证1min后生成新的pglog文件
History     :
        等待61s，可能生成2个日志文件；增加断言
"""
import time
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node


class ErrorLog(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Guc_ErrorLog_Case0032 start--')
        self.userNode = Node('PrimaryDbUser')
        self.pri_root = Node('PrimaryRoot')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()

    def test_main(self):
        step_txt = '----查询原log_rotation_age参数配置值----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show log_rotation_age;')
        self.log.info(f"log_rotation_age is {result}")
        self.para1 = result.strip().splitlines()[-2]
        result = self.pri_sh.execut_db_sql('show log_directory;')
        self.log.info(f"log_directory is {result}")
        self.para2 = result.strip().splitlines()[-2]

        step_txt = '----step1:修改参数log_rotation_age值为1; expect:修改成功----'
        self.log.info(step_txt)
        msg = self.pri_sh.execute_gsguc('reload',
                                        self.constant.GSGUC_SUCCESS_MSG,
                                        'log_rotation_age=1')
        self.assertTrue(msg, '执行失败:' + step_txt)

        step_txt = '----step2:查看返回值：show log_rotation_age; expect:查询成功----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show log_rotation_age;')
        self.log.info(f"log_rotation_age is {result}")
        new_para = result.strip().splitlines()[-2].strip()
        self.assertEqual('1min', new_para, '执行失败:' + step_txt)

        step_txt = '----step3:进入log_directory目录，查询pglog文件数量; ' \
                   'expect:验证1min后生成新的pglog文件----'
        self.log.info(step_txt)
        ls_cmd = f'ls {self.para2}| wc -l'
        self.log.info(ls_cmd)
        log_num1 = int(self.pri_root.sh(ls_cmd).result())
        self.log.info('当前pglog数量为：' + str(log_num1))
        time.sleep(61)
        log_num2 = int(self.pri_root.sh(ls_cmd).result())
        self.log.info('1min后，pglog数量为：' + str(log_num2))
        self.assertLessEqual(log_num2 - log_num1, 2, '执行失败:' + step_txt)
        self.assertGreaterEqual(log_num2 - log_num1, 1, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        self.log.info('----恢复参数log_rotation_age值为初始值----')
        self.pri_sh.execute_gsguc('reload',
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f'log_rotation_age={self.para1}')
        result = self.pri_sh.execut_db_sql('show log_rotation_age;')
        self.log.info(f"log_rotation_age is {result}")

        self.log.info(
            '--Opengauss_Function_Guc_ErrorLog_Case0032 finish--')

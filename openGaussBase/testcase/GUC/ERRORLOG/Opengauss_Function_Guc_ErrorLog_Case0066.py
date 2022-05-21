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
Case Name   : 普通用户修改参数log_min_error_statement的参数值为panic不生效
Description :
    1.创建普通用户
    2.普通用户连接数据库执行set log_min_error_statement to panic;
    3.普通用户连接数据库执行alter system set log_min_error_statement to panic;
    4.查看参数值：show log_min_error_statement;
Expect      :
    1.创建普通用户成功
    2.普通用户连接数据库执行set log_min_error_statement to panic;执行失败
    3.普通用户连接数据库执行alter system set log_min_error_statement to panic;执行失败
    4.查看参数值：show log_min_error_statement 未发生变化;
History     :
"""
import unittest

from testcase.utils.Common import Common
from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import Node
from yat.test import macro


class ErrorLog(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info('--Opengauss_Function_Guc_ErrorLog_Case0066 start--')
        self.pri_dbuser = Node('PrimaryDbUser')
        self.pri_root = Node('PrimaryRoot')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.common = Common()
        self.constant = Constant()
        self.common_user = 'u_guc_errorlog_case0066'
        self.password = macro.PASSWD_INITIAL
        self.connect_info = f'-U {self.common_user} -W {self.password}'

    def test_main(self):
        step_txt = '----查看log_min_error_statement初始配置值----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show log_min_error_statement;')
        self.log.info(f"log_min_error_statement is {result}")
        self.para1 = result.strip().splitlines()[-2]

        step_txt = '----step1:创建普通用户;expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"DROP USER IF EXISTS {self.common_user} cascade; " \
            f"CREATE USER {self.common_user} PASSWORD '{self.password}';"
        self.log.info(create_sql)
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        self.assertIn(self.constant.CREATE_ROLE_SUCCESS_MSG, create_result,
                      '执行失败:' + step_txt)

        step_txt = '----step2:普通用户连接数据库执行set设置' \
                   'expect:执行失败----'
        self.log.info(step_txt)
        sql = f'set log_min_error_statement to panic;'
        result = self.pri_sh.execut_db_sql(sql, sql_type=self.connect_info)
        self.log.info(result)
        self.assertIn(self.constant.PERMISSION_DENIED, result,
                      '执行失败:' + step_txt)

        step_txt = '----step3:普通用户连接数据库执行alter设置' \
                   'expect:执行失败----'
        self.log.info(step_txt)
        sql = f'alter system set log_min_error_statement to panic;'
        result = self.pri_sh.execut_db_sql(sql, sql_type=self.connect_info)
        self.log.info(result)
        self.assertIn(self.constant.PERMISSION_DENY_MSG, result,
                      '执行失败:' + step_txt)

        step_txt = '----step4: 查看参数值；expect:未发生变化;----'
        self.log.info(step_txt)
        result = self.pri_sh.execut_db_sql('show log_min_error_statement;')
        self.log.info(f"log_min_error_statement is {result}")
        self.para2 = result.strip().splitlines()[-2]
        self.assertEqual(self.para1, self.para2, '执行失败:' + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        self.log.info('----恢复参数log_min_error_statement值为初始值----')
        self.pri_sh.execute_gsguc('reload',
                                  self.constant.GSGUC_SUCCESS_MSG,
                                  f'log_min_error_statement={self.para1}')
        result = self.pri_sh.execut_db_sql('show log_min_error_statement;')
        self.log.info(f"log_min_error_statement is {result}")

        self.log.info('----清理测试用户----')
        drop_sql = f"DROP USER IF EXISTS {self.common_user} cascade; "
        self.log.info(drop_sql)
        drop_result = self.pri_sh.execut_db_sql(drop_sql)
        self.log.info(drop_result)

        self.log.info('--Opengauss_Function_Guc_ErrorLog_Case0066 finish--')

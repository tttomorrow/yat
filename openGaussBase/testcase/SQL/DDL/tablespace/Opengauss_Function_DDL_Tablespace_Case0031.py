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
Case Type   : 功能测试-表空间
Case Name   : 表空间删除用户限制
Description :
    1、创建系统管理员用户和普通用户
    2、创建表空间，未指定普通用户为owner
    3、非表空间owner及系统管理员进行表空间删除
    4、变更表空间所有者为普通用户
    5、表空间的owner进行表空间删除
    6、创建表空间，指定owner为普通用户
    7、系统管理员进行表空间删除
Expect      :
    1、创建系统管理员用户和普通用户成功
    2、创建表空间，未指定普通用户为owner，创建成功
    3、非表空间owner及系统管理员进行表空间删除，删除失败
    4、变更表空间所有者为普通用户成功
    5、表空间的owner进行表空间删除，删除成功
    6、创建表空间，指定owner为普通用户，创建成功
    7、系统管理员进行表空间删除，删除成功
History     :
"""

import os
import unittest

from testcase.utils.CommonSH import CommonSH
from testcase.utils.Constant import Constant
from testcase.utils.Logger import Logger
from yat.test import macro


class Tablespace(unittest.TestCase):
    def setUp(self):
        self.log = Logger()
        self.log.info(f'-----{os.path.basename(__file__)} start-----')
        self.pri_sh = CommonSH('PrimaryDbUser')
        self.constant = Constant()
        self.tbspc_name = 'tsp_tbspc0031'
        self.tbspc_location = 'tbspc0031'
        self.pwd = macro.PASSWD_INITIAL
        self.com_user = 'u_tbspc0031_com'
        self.sys_user = 'u_tbspc0031_sys'
        self.connect_sys = f'-U {self.sys_user} -W {self.pwd}'
        self.connect_com = f'-U {self.com_user} -W {self.pwd}'
        self.err_flag = 'ERROR:  permission denied for tablespace'

    def test_main(self):
        step_txt = '----step1:创建系统管理员用户和普通用户; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name}; " \
            f"drop user if exists {self.com_user} cascade; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.com_user} password '{self.pwd}';" \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)

        step_txt = '----step2:创建表空间，未指定普通用户为owner； expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name} " \
            f"relative location '{self.tbspc_location}';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_sys)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step3:非表空间owner及系统管理员进行表空间删除； expect:删除失败----'
        self.log.info(step_txt)
        drop_sql = f'drop tablespace {self.tbspc_name};'
        drop_result = self.pri_sh.execut_db_sql(drop_sql,
                                                sql_type=self.connect_com)
        self.log.info(drop_result)
        self.assertIn(self.err_flag, drop_result, "执行失败" + step_txt)

        step_txt = '----step4:变更表空间所有者为普通用户成功； expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter tablespace {self.tbspc_name} " \
            f"owner to {self.com_user};"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)

        step_txt = '----step5:表空间的owner进行表空间删除； expect:删除成功----'
        self.log.info(step_txt)
        drop_result = self.pri_sh.execut_db_sql(drop_sql,
                                                sql_type=self.connect_com)
        self.log.info(drop_result)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, drop_result,
                      "执行失败" + step_txt)

        step_txt = '----step6:创建表空间，指定owner为普通用户； expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name} " \
            f"owner {self.com_user} " \
            f"relative location '{self.tbspc_location}' ;"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_sys)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

        step_txt = '----step7:系统管理员进行表空间删除； expect:删除成功----'
        self.log.info(step_txt)
        drop_result = self.pri_sh.execut_db_sql(drop_sql,
                                                sql_type=self.connect_sys)
        self.log.info(drop_result)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, drop_result,
                      "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name}; " \
            f"drop user if exists {self.com_user} cascade; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(2, drop_user, "执行失败" + step1_txt)
        self.assertEqual(1, drop_tbspc, "执行失败" + step1_txt)

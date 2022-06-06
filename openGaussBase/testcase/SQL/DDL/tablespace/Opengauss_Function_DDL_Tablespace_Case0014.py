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
Case Name   : 表空间创建用户权限限制
Description :
    1、创建系统管理员用户和普通用户
    2、普通用户创建表空间
    3、普通用户赋权gs_role_tablespace
    4、普通用户具有gs_role_tablespace权限，再次创建表空间
    5、系统管理员创建表空间
Expect      :
    1、创建系统管理员用户和普通用户成功
    2、普通用户创建表空间失败
    3、普通用户赋权gs_role_tablespace成功
    4、普通用户具有gs_role_tablespace权限，再次创建表空间成功
    5、系统管理员创建表空间成功
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
        self.tbspc_name = 'tsp_tbspc0014'
        self.tbspc_location = 'tbspc0014_location'
        self.pwd = macro.PASSWD_INITIAL
        self.common_user = 'u_tsp_tbspc0014_1'
        self.sys_user = 'u_tsp_tbspc0014_2'
        self.comm_connect = f'-U {self.common_user} -W {self.pwd}'
        self.sys_connect = f'-U {self.sys_user} -W {self.pwd}'
        self.create_sql = f"create tablespace {self.tbspc_name} " \
            f"relative location '{self.tbspc_location}';"
        self.drop_sql = f"drop tablespace if exists {self.tbspc_name};"

    def test_main(self):
        step_txt = '----step1:创建系统管理员用户和普通用户; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name}; " \
            f"drop user if exists {self.common_user} cascade; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.common_user} password '{self.pwd}';" \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 2, "执行失败" + step_txt)

        step_txt = '----step2:普通用户创建表空间; expect:创建失败----'
        self.log.info(step_txt)
        create_result = self.pri_sh.execut_db_sql(self.create_sql,
                                                  sql_type=self.comm_connect)
        self.log.info(create_result)
        flag1 = "ERROR:  Permission denied to create tablespace "
        flag2 = "HINT:  Must be system admin or a member of the " \
                "gs_role_tablespace role to create a tablespace."
        self.assertTrue(flag1 in create_result and flag2 in create_result,
                        "执行失败" + step_txt)

        step_txt = '----step3:普通用户赋权gs_role_tablespace; expect:成功----'
        self.log.info(step_txt)
        grant_sql = f"grant gs_role_tablespace to {self.common_user};"
        grant_result1 = self.pri_sh.execut_db_sql(grant_sql)
        self.log.info(grant_result1)
        self.assertIn(self.constant.GRANT_SUCCESS_MSG, grant_result1,
                      "执行失败" + step_txt)

        step_txt = '----step4:普通用户具有gs_role_tablespace权限创建表空间; expect:成功----'
        self.log.info(step_txt)
        create_result = self.pri_sh.execut_db_sql(self.create_sql,
                                                  sql_type=self.comm_connect)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

        step_txt = '--删除表空间; expect:成功----'
        self.log.info(step_txt)
        drop_result = self.pri_sh.execut_db_sql(self.drop_sql,
                                                sql_type=self.comm_connect)
        self.log.info(drop_result)
        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, drop_result,
                      "执行失败" + step_txt)

        step_txt = '----step5:系统管理员用户创建tablespace; expect:成功----'
        self.log.info(step_txt)
        create_result = self.pri_sh.execut_db_sql(self.create_sql,
                                                  sql_type=self.sys_connect)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)

    def tearDown(self):
        self.log.info('----this is teardown----')
        step_txt = '----删除表空间; expect:成功----'
        self.log.info(step_txt)
        drop_result = self.pri_sh.execut_db_sql(self.drop_sql)
        self.log.info(drop_result)
        step_txt = '----删除用户; expect:成功----'
        self.log.info(step_txt)
        clean_sql = f"drop user if exists {self.common_user} cascade; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')

        self.assertIn(self.constant.TABLESPCE_DROP_SUCCESS, drop_result,
                      "执行失败" + step_txt)
        drop_count = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        self.assertEqual(drop_count, 2, "执行失败" + step_txt)

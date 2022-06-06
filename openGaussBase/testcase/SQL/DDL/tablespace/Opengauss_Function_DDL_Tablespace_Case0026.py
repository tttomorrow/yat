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
Case Name   : 设置表空间属性（set）random_page_cost随机读取page的开销
Description :
    1、修改表空间random_page_cost设定值为负数
    2、修改表空间random_page_cost设定值为字符串
    3、修改表空间random_page_cost不设置值
    4、修改表空间random_page_cost设定值为正整数
    5、修改表空间random_page_cost设定值为正浮点数
Expect      :
    1、修改表空间random_page_cost设定值为负数，修改失败
    2、修改表空间random_page_cost设定值为字符串，修改失败
    3、修改表空间random_page_cost不设置值，修改成功
    4、修改表空间random_page_cost设定值为正整数，修改成功
    5、修改表空间random_page_cost设定值为正浮点数，修改成功
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
        self.tbspc_name1 = 'tsp_tbspc0026'
        self.tbspc_location1 = 'tbspc0026'
        self.pwd = macro.PASSWD_INITIAL
        self.sys_user = 'u_tbspc0026_sys'
        self.connect_sys = f'-U {self.sys_user} -W {self.pwd}'
        self.err_flag1 = 'out of bounds for option "random_page_cost"'
        self.err_flag2 = 'ERROR:  invalid value for floating point ' \
                         'option "random_page_cost"'

    def test_main(self):
        step_txt = '----step0:创建系统管理员; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.sys_user} cascade; " \
            f"create user {self.sys_user} sysadmin password '{self.pwd}';"
        create_result = self.pri_sh.execut_db_sql(create_sql)
        self.log.info(create_result)
        assert_flag = create_result.splitlines().count(
            self.constant.CREATE_ROLE_SUCCESS_MSG)
        self.assertEqual(assert_flag, 1, "执行失败" + step_txt)

        step_txt = '----step0:缺省random_page_cost创建表空间; expect:创建成功----'
        self.log.info(step_txt)
        create_sql = f"create tablespace {self.tbspc_name1} " \
            f"relative location '{self.tbspc_location1}';"
        create_result = self.pri_sh.execut_db_sql(create_sql,
                                                  sql_type=self.connect_sys)
        self.log.info(create_result)
        self.assertIn(self.constant.TABLESPCE_CREATE_SUCCESS, create_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        check_sql = f"select spcoptions from pg_tablespace where " \
            f"spcname = '{self.tbspc_name1}';"
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertEqual(' ', spcoptions, "执行失败" + step_txt)

        step_txt = '----step1:修改表空间random_page_cost设定值为负数; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"set (random_page_cost='-6');"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag1, alter_result, "执行失败" + step_txt)

        step_txt = '----step2:修改表空间random_page_cost设定值为字符串; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"set (random_page_cost='abc');"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag2, alter_result, "执行失败" + step_txt)

        step_txt = '----step3:修改表空间random_page_cost不设置值; expect:修改失败----'
        self.log.info(step_txt)
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"set (random_page_cost);"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.err_flag2, alter_result, "执行失败" + step_txt)

        step_txt = '----step4:修改表空间random_page_cost设定值为正整数; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"set (random_page_cost='6');"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertIn('random_page_cost=6', spcoptions, "执行失败" + step_txt)

        step_txt = '----step5:修改表空间random_page_cost设定值为正浮点数; expect:修改成功----'
        self.log.info(step_txt)
        alter_sql = f"alter  tablespace {self.tbspc_name1} " \
            f"set (random_page_cost=9.333);"
        alter_result = self.pri_sh.execut_db_sql(alter_sql,
                                                 sql_type=self.connect_sys)
        self.log.info(alter_result)
        self.assertIn(self.constant.TABLESPCE_ALTER_SUCCESS, alter_result,
                      "执行失败" + step_txt)
        self.log.info('--检查tablespace设置--')
        spcoptions = self.pri_sh.execut_db_sql(check_sql).splitlines()[-2]
        self.log.info(spcoptions)
        self.assertIn('random_page_cost=9.333', spcoptions, "执行失败" + step_txt)

    def tearDown(self):
        step1_txt = '----清理表空间及用户; expect:成功----'
        self.log.info(step1_txt)
        clean_sql = f"drop tablespace if exists {self.tbspc_name1}; " \
            f"drop user if exists {self.sys_user} cascade; "
        clean_result = self.pri_sh.execut_db_sql(clean_sql)
        self.log.info(clean_result)

        self.log.info(f'-----{os.path.basename(__file__)} end-----')
        drop_user = clean_result.count(self.constant.DROP_ROLE_SUCCESS_MSG)
        drop_tbspc = clean_result.count(self.constant.TABLESPCE_DROP_SUCCESS)
        self.assertEqual(1, drop_user, "执行失败" + step1_txt)
        self.assertEqual(1, drop_tbspc, "执行失败" + step1_txt)
